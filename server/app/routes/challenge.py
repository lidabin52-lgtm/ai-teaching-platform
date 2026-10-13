"""
闯关模块API
处理关卡列表、详情、提交、历史记录等接口
"""
from flask import Blueprint, request, jsonify, current_app
import json
import hashlib
from datetime import datetime

from app.utils.auth import login_required
from app.utils.response import success, error, bad_request, not_found
from app.utils.db import query_one, query_all, execute, insert_and_get_id

# 创建蓝图
challenge_bp = Blueprint('challenge', __name__, url_prefix='/api/challenge')


@challenge_bp.route('/list', methods=['GET'])
@login_required
def get_challenge_list(current_user):
    """
    获取关卡列表（按段位分组，标记完成/未解锁状态）
    
    查询参数:
        difficulty: 段位筛选（可选，bronze/silver/gold/diamond/king）
    
    返回:
        {
            "code": 200,
            "data": {
                "bronze": [
                    {
                        "id": 1,
                        "title": "HTML基础",
                        "status": "completed",  // completed/unlocked/locked
                        "stars": 3,
                        ...
                    }
                ],
                ...
            }
        }
    """
    user_id = current_user['user_id']
    difficulty_filter = request.args.get('difficulty')
    
    # 查询所有关卡
    where_clause = "WHERE status = 1"
    params = []
    
    if difficulty_filter:
        where_clause += " AND difficulty = %s"
        params.append(difficulty_filter)
    
    challenges = query_all(
        f"""SELECT id, title, difficulty, order_num, category, tags, time_limit
            FROM challenges
            {where_clause}
            ORDER BY 
                FIELD(difficulty, 'bronze', 'silver', 'gold', 'diamond', 'king'),
                order_num""",
        tuple(params) if params else None
    )
    
    # 查询用户已完成的关卡
    completed = query_all(
        """SELECT challenge_id, MAX(stars) as stars, MAX(total_score) as score
           FROM submissions
           WHERE user_id = %s AND status = 'completed'
           GROUP BY challenge_id""",
        (user_id,)
    )
    
    completed_map = {c['challenge_id']: c for c in completed}
    
    # 查询用户进度
    progress = query_one(
        "SELECT * FROM student_progress WHERE user_id = %s",
        (user_id,)
    )
    
    # 按段位分组
    result = {
        'bronze': [],
        'silver': [],
        'gold': [],
        'diamond': [],
        'king': []
    }
    
    for c in challenges:
        challenge_data = {
            'id': c['id'],
            'title': c['title'],
            'difficulty': c['difficulty'],
            'category': c['category'],
            'tags': json.loads(c['tags']) if c['tags'] else [],
            'time_limit': c['time_limit'],
            'order_num': c['order_num']
        }
        
        # 判断状态
        if c['id'] in completed_map:
            challenge_data['status'] = 'completed'
            challenge_data['stars'] = completed_map[c['id']]['stars']
            challenge_data['best_score'] = completed_map[c['id']]['score']
        else:
            # 检查是否解锁
            challenge_data['status'] = 'unlocked'  # 默认解锁
            challenge_data['stars'] = 0
            
            # 查询关卡解锁条件
            challenge_detail = query_one(
                "SELECT unlock_requirement FROM challenges WHERE id = %s",
                (c['id'],)
            )
            
            if challenge_detail and challenge_detail['unlock_requirement']:
                unlock_req = json.loads(challenge_detail['unlock_requirement'])
                prev_id = unlock_req.get('prev_challenge_id')
                min_stars = unlock_req.get('min_stars', 1)
                
                if prev_id:
                    # 检查前置关卡是否完成且达到星级要求
                    prev_completed = completed_map.get(prev_id)
                    if not prev_completed or prev_completed['stars'] < min_stars:
                        challenge_data['status'] = 'locked'
                        challenge_data['locked_reason'] = f'需要先完成前置关卡并获得{min_stars}星以上'
        
        result[c['difficulty']].append(challenge_data)
    
    return success(result)


@challenge_bp.route('/<int:challenge_id>', methods=['GET'])
@login_required
def get_challenge_detail(current_user, challenge_id):
    """
    获取关卡详情（含需求描述和初始代码）
    
    返回:
        {
            "code": 200,
            "data": {
                "id": 1,
                "title": "HTML基础：创建第一个网页",
                "description": "## 任务目标...",
                "starter_code": "<!DOCTYPE html>...",
                "scoring_criteria": {...},
                "time_limit": 30,
                "hint_count": 3,
                ...
            }
        }
    """
    user_id = current_user['user_id']
    
    # 查询关卡详情
    challenge = query_one(
        """SELECT c.*, u.nickname as creator_name
           FROM challenges c
           LEFT JOIN users u ON c.created_by = u.id
           WHERE c.id = %s""",
        (challenge_id,)
    )
    
    if not challenge:
        return not_found('关卡不存在')
    
    if challenge['status'] != 1:
        return error('该关卡已下架', code=403)
    
    # 查询用户在该关卡的完成情况
    best_submission = query_one(
        """SELECT * FROM submissions
           WHERE user_id = %s AND challenge_id = %s AND status = 'completed'
           ORDER BY total_score DESC, created_at DESC
           LIMIT 1""",
        (user_id, challenge_id)
    )
    
    # 查询尝试次数
    attempt_count = query_one(
        "SELECT COUNT(*) as count FROM submissions WHERE user_id = %s AND challenge_id = %s",
        (user_id, challenge_id)
    )['count']
    
    result = {
        'id': challenge['id'],
        'title': challenge['title'],
        'description': challenge['description'],
        'difficulty': challenge['difficulty'],
        'order_num': challenge['order_num'],
        'category': challenge['category'],
        'tags': json.loads(challenge['tags']) if challenge['tags'] else [],
        'starter_code': challenge['starter_code'],
        'language': challenge['language'],
        'scoring_criteria': json.loads(challenge['scoring_criteria']) if challenge['scoring_criteria'] else {},
        'time_limit': challenge['time_limit'],
        'hint_count': challenge['hint_count'],
        'creator_name': challenge['creator_name'],
        'created_at': challenge['created_at'].isoformat() if challenge['created_at'] else None,
        # 用户相关
        'attempt_count': attempt_count,
        'best_score': best_submission['total_score'] if best_submission else None,
        'best_stars': best_submission['stars'] if best_submission else 0,
        'is_completed': best_submission is not None
    }
    
    return success(result)


@challenge_bp.route('/<int:challenge_id>/submit', methods=['POST'])
@login_required
def submit_code(current_user, challenge_id):
    """
    提交代码，调用AI审判，保存记录，返回审判结果
    
    请求体:
        {
            "code": "学生提交的代码",
            "time_spent": 120  // 耗时（秒）
        }
    
    返回:
        {
            "code": 200,
            "data": {
                "submission_id": 123,
                "function_score": 3,
                "standard_score": 2,
                "cool_score": 2,
                "total_stars": 3,
                "comment": "评语...",
                "hint": "提示..."
            }
        }
    """
    user_id = current_user['user_id']
    data = request.get_json()
    
    if not data:
        return bad_request('请求体不能为空')
    
    code = data.get('code', '')
    time_spent = data.get('time_spent', 0)
    
    if not code or not code.strip():
        return bad_request('代码不能为空')
    
    # 查询关卡信息
    challenge = query_one(
        "SELECT * FROM challenges WHERE id = %s AND status = 1",
        (challenge_id,)
    )
    
    if not challenge:
        return not_found('关卡不存在或已下架')
    
    # 查询之前的尝试次数
    attempt_number = query_one(
        "SELECT COUNT(*) as count FROM submissions WHERE user_id = %s AND challenge_id = %s",
        (user_id, challenge_id)
    )['count'] + 1
    
    # 计算代码哈希（用于查重）
    code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
    
    # 创建提交记录（状态为judging）
    submission_id = insert_and_get_id(
        """INSERT INTO submissions
           (user_id, challenge_id, code, code_hash, status, attempt_number, time_spent)
           VALUES (%s, %s, %s, %s, 'judging', %s, %s)""",
        (user_id, challenge_id, code, code_hash, attempt_number, time_spent)
    )
    
    try:
        # 调用AI审判服务
        from app.services.ai_service import CodeJudge
        
        api_key = current_app.config.get('DEEPSEEK_API_KEY', '')
        base_url = current_app.config.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        
        if not api_key:
            # 模拟审判结果（开发环境）
            result = _mock_judgment(code, challenge)
        else:
            judge = CodeJudge(api_key=api_key, base_url=base_url)
            result = judge.judge(
                description=challenge['description'],
                scoring_criteria=json.loads(challenge['scoring_criteria']) if challenge['scoring_criteria'] else {},
                code=code,
                difficulty=challenge['difficulty'],
                language=challenge['language'] or 'html'
            )
        
        # 更新提交记录
        execute(
            """UPDATE submissions SET
               status = 'completed',
               ai_feedback = %s,
               ai_summary = %s,
               total_score = %s,
               stars = %s,
               score_correctness = %s,
               score_code_quality = %s,
               score_best_practice = %s,
               score_creativity = %s,
               scoring_details = %s,
               judged_at = NOW()
               WHERE id = %s""",
            (result.comment,  # ai_feedback
             result.comment[:200] if result.comment else '',  # ai_summary
             (result.function_score + result.standard_score + result.cool_score) * 11,  # total_score (近似)
             result.total_stars,
             result.function_score * 33,  # score_correctness
             result.standard_score * 33,  # score_code_quality
             result.cool_score * 33,  # score_best_practice
             result.cool_score * 33,  # score_creativity
             json.dumps(result.to_dict()),  # scoring_details
             submission_id)
        )
        
        # 更新用户进度
        _update_user_progress(user_id, challenge_id, challenge['difficulty'], result.total_stars)
        
        return success({
            'submission_id': submission_id,
            'function_score': result.function_score,
            'standard_score': result.standard_score,
            'cool_score': result.cool_score,
            'total_stars': result.total_stars,
            'comment': result.comment,
            'hint': result.hint
        })
        
    except Exception as e:
        # 审判失败，更新状态
        execute(
            "UPDATE submissions SET status = 'failed' WHERE id = %s",
            (submission_id,)
        )
        return error(f'AI审判失败: {str(e)}', code=500)


def _mock_judgment(code, challenge):
    """模拟审判结果（开发环境使用）"""
    from app.services.ai_service import JudgmentResult
    
    # 简单的规则判断
    code_length = len(code.strip())
    
    if code_length < 50:
        return JudgmentResult(
            function_score=1,
            standard_score=1,
            cool_score=1,
            total_stars=1,
            comment='代码内容较少，请补充完整。',
            hint='建议按照关卡要求完成所有功能点。'
        )
    elif code_length < 200:
        return JudgmentResult(
            function_score=2,
            standard_score=2,
            cool_score=1,
            total_stars=2,
            comment='代码基本完成，结构清晰。可以进一步优化代码规范。',
            hint=''
        )
    else:
        return JudgmentResult(
            function_score=3,
            standard_score=2,
            cool_score=2,
            total_stars=3,
            comment='代码完成度很好！功能完整，结构清晰。继续保持！',
            hint=''
        )


def _update_user_progress(user_id, challenge_id, difficulty, stars):
    """更新用户进度"""
    # 检查是否是该关卡的最佳成绩
    best = query_one(
        """SELECT MAX(stars) as max_stars FROM submissions
           WHERE user_id = %s AND challenge_id = %s AND status = 'completed'""",
        (user_id, challenge_id)
    )
    
    # 只有当这次是最佳成绩时才更新进度
    if best and best['max_stars'] == stars:
        # 检查是否是首次完成该关卡
        prev_completions = query_one(
            """SELECT COUNT(*) as count FROM submissions
               WHERE user_id = %s AND challenge_id = %s AND status = 'completed' AND stars > 0""",
            (user_id, challenge_id)
        )
        
        if prev_completions['count'] == 1:  # 首次完成
            # 更新对应段位的完成数
            column = f"{difficulty}_completed"
            execute(
                f"UPDATE student_progress SET {column} = {column} + 1 WHERE user_id = %s",
                (user_id,)
            )
    
    # 更新总提交次数和总星数
    execute(
        """UPDATE student_progress SET
           total_submissions = total_submissions + 1,
           total_stars = (SELECT COALESCE(SUM(stars), 0) FROM submissions WHERE user_id = %s AND status = 'completed'),
           last_submission_at = NOW()
           WHERE user_id = %s""",
        (user_id, user_id)
    )


@challenge_bp.route('/<int:challenge_id>/submissions', methods=['GET'])
@login_required
def get_challenge_submissions(current_user, challenge_id):
    """
    获取该关卡自己的历史提交记录
    
    查询参数:
        page: 页码
        page_size: 每页数量
    """
    user_id = current_user['user_id']
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    # 检查关卡是否存在
    challenge = query_one(
        "SELECT id, title FROM challenges WHERE id = %s",
        (challenge_id,)
    )
    
    if not challenge:
        return not_found('关卡不存在')
    
    # 查询总数
    total = query_one(
        "SELECT COUNT(*) as count FROM submissions WHERE user_id = %s AND challenge_id = %s",
        (user_id, challenge_id)
    )['count']
    
    # 查询列表
    offset = (page - 1) * page_size
    submissions = query_all(
        """SELECT id, code, ai_feedback, ai_summary, total_score, stars,
                  score_correctness, score_code_quality, score_best_practice, score_creativity,
                  status, attempt_number, time_spent, created_at, judged_at
           FROM submissions
           WHERE user_id = %s AND challenge_id = %s
           ORDER BY created_at DESC
           LIMIT %s OFFSET %s""",
        (user_id, challenge_id, page_size, offset)
    )
    
    items = []
    for s in submissions:
        items.append({
            'id': s['id'],
            'code': s['code'],
            'ai_feedback': s['ai_feedback'],
            'ai_summary': s['ai_summary'],
            'total_score': s['total_score'],
            'stars': s['stars'],
            'scores': {
                'correctness': s['score_correctness'],
                'code_quality': s['score_code_quality'],
                'best_practice': s['score_best_practice'],
                'creativity': s['score_creativity']
            },
            'status': s['status'],
            'attempt_number': s['attempt_number'],
            'time_spent': s['time_spent'],
            'created_at': s['created_at'].isoformat() if s['created_at'] else None,
            'judged_at': s['judged_at'].isoformat() if s['judged_at'] else None
        })
    
    from app.utils.response import paginate
    return jsonify(paginate(items, total, page, page_size))
