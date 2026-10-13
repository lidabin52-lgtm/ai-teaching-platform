"""
学情分析模块API
提供班级整体数据、热力图、个体分析、错误统计等接口
需要教师角色权限
"""
from flask import Blueprint, request, jsonify
import json
from collections import Counter

from app.utils.auth import login_required, teacher_required
from app.utils.response import success, error, bad_request, not_found
from app.utils.db import query_one, query_all

# 创建蓝图
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/overview', methods=['GET'])
@login_required
@teacher_required
def get_overview(current_user):
    """
    获取班级整体数据
    
    查询参数:
        class_id: 班级ID（可选，不传则返回所有学生）
    
    返回:
        {
            "code": 200,
            "data": {
                "total_students": 50,
                "total_challenges": 30,
                "completion_rate": 68.5,
                "avg_stars": 2.3,
                "stuck_top5": [
                    {"challenge_id": 1, "title": "xxx", "stuck_count": 15}
                ]
            }
        }
    """
    teacher_id = current_user['user_id']
    class_id = request.args.get('class_id', type=int)
    
    # 构建学生筛选条件
    student_filter = ""
    params = []
    
    if class_id:
        # 验证班级归属
        class_info = query_one(
            "SELECT id FROM classes WHERE id = %s AND teacher_id = %s",
            (class_id, teacher_id)
        )
        if not class_info:
            return error('班级不存在或无权限访问', code=403)
        
        student_filter = """
            WHERE u.id IN (
                SELECT student_id FROM class_students WHERE class_id = %s
            )
        """
        params = [class_id]
    
    # 统计学生总数
    total_students = query_one(
        f"SELECT COUNT(DISTINCT u.id) as count FROM users u {student_filter}",
        tuple(params) if params else None
    )['count']
    
    # 统计关卡总数
    total_challenges = query_one(
        "SELECT COUNT(*) as count FROM challenges WHERE status = 1"
    )['count']
    
    # 统计完成率（至少完成一个关卡的学生比例）
    if student_filter:
        completed_students = query_one(
            f"""SELECT COUNT(DISTINCT s.user_id) as count
                FROM submissions s
                JOIN users u ON s.user_id = u.id
                {student_filter.replace('WHERE u.id', "WHERE s.status = 'completed' AND u.id")}
             """,
            tuple(params) if params else None
        )['count']
    else:
        completed_students = query_one(
            "SELECT COUNT(DISTINCT user_id) as count FROM submissions WHERE status = 'completed'"
        )['count']
    
    completion_rate = round(completed_students / total_students * 100, 1) if total_students > 0 else 0
    
    # 统计平均星数
    if student_filter:
        avg_stars_result = query_one(
            f"""SELECT AVG(stars) as avg_stars
                FROM submissions s
                JOIN users u ON s.user_id = u.id
                {student_filter.replace('WHERE u.id', "WHERE s.status = 'completed' AND u.id")}
            """,
            tuple(params) if params else None
        )
    else:
        avg_stars_result = query_one(
            "SELECT AVG(stars) as avg_stars FROM submissions WHERE status = 'completed'"
        )
    avg_stars = round(float(avg_stars_result['avg_stars'] or 0), 1)
    
    # 统计卡关Top5（提交次数多但未通过的关卡）
    stuck_top5 = query_all(
        f"""SELECT c.id, c.title, c.difficulty, COUNT(DISTINCT s.user_id) as stuck_count
            FROM submissions s
            JOIN challenges c ON s.challenge_id = c.id
            JOIN users u ON s.user_id = u.id
            WHERE s.status != 'completed' 
            {'AND u.id IN (SELECT student_id FROM class_students WHERE class_id = %s)' if class_id else ''}
            GROUP BY c.id
            ORDER BY stuck_count DESC
            LIMIT 5
        """,
        tuple(params) if params else None
    )
    
    stuck_list = [{
        'challenge_id': s['id'],
        'title': s['title'],
        'difficulty': s['difficulty'],
        'stuck_count': s['stuck_count']
    } for s in stuck_top5]
    
    return success({
        'total_students': total_students,
        'total_challenges': total_challenges,
        'completion_rate': completion_rate,
        'avg_stars': avg_stars,
        'stuck_top5': stuck_list
    })


@analytics_bp.route('/heatmap', methods=['GET'])
@login_required
@teacher_required
def get_heatmap(current_user):
    """
    获取知识掌握热力图数据
    
    返回:
        {
            "code": 200,
            "data": {
                "categories": ["HTML", "CSS", "JavaScript", "Vue", "React"],
                "series": [
                    {"name": "bronze", "data": [85, 70, 60, 30, 20]},
                    {"name": "silver", "data": [60, 50, 40, 20, 10]},
                    ...
                ]
            }
        }
    """
    teacher_id = current_user['user_id']
    class_id = request.args.get('class_id', type=int)
    
    # 获取所有分类
    categories = query_all(
        """SELECT DISTINCT category FROM challenges 
           WHERE status = 1 AND category IS NOT NULL AND category != ''
           ORDER BY category"""
    )
    category_list = [c['category'] for c in categories]
    
    # 获取各段位
    difficulties = ['bronze', 'silver', 'gold', 'diamond', 'king']
    
    # 构建学生筛选
    student_join = ""
    student_where = ""
    params = []
    
    if class_id:
        student_join = "JOIN class_students cs ON s.user_id = cs.student_id"
        student_where = "AND cs.class_id = %s"
        params = [class_id]
    
    series = []
    for diff in difficulties:
        data = []
        for cat in category_list:
            # 计算该分类该段位的平均完成率
            result = query_one(
                f"""SELECT 
                       COUNT(DISTINCT c.id) as total,
                       COUNT(DISTINCT CASE WHEN s.status = 'completed' THEN c.id END) as completed
                    FROM challenges c
                    LEFT JOIN submissions s ON c.id = s.challenge_id {student_join}
                    WHERE c.category = %s 
                    AND c.difficulty = %s 
                    AND c.status = 1
                    {student_where}
                """,
                tuple([cat, diff] + params) if params else [cat, diff]
            )
            
            total = result['total'] or 0
            completed = result['completed'] or 0
            rate = round(completed / total * 100, 1) if total > 0 else 0
            data.append(rate)
        
        series.append({
            'name': _get_difficulty_label(diff),
            'data': data
        })
    
    return success({
        'categories': category_list,
        'series': series
    })


@analytics_bp.route('/student/<int:student_id>', methods=['GET'])
@login_required
@teacher_required
def get_student_analysis(current_user, student_id):
    """
    获取个体能力雷达图数据
    
    返回:
        {
            "code": 200,
            "data": {
                "student_info": {...},
                "radar_data": {
                    "dimensions": ["HTML", "CSS", "JavaScript", "Vue", "React"],
                    "values": [85, 70, 60, 30, 20]
                },
                "recent_submissions": [...]
            }
        }
    """
    teacher_id = current_user['user_id']
    
    # 查询学生信息
    student = query_one(
        "SELECT id, username, nickname, email, created_at FROM users WHERE id = %s AND role = 'student'",
        (student_id,)
    )
    
    if not student:
        return not_found('学生不存在')
    
    # 获取各分类的平均得分
    category_scores = query_all(
        """SELECT c.category, AVG(s.total_score) as avg_score
           FROM submissions s
           JOIN challenges c ON s.challenge_id = c.id
           WHERE s.user_id = %s AND s.status = 'completed'
           GROUP BY c.category
           ORDER BY avg_score DESC""",
        (student_id,)
    )
    
    # 获取所有分类
    all_categories = query_all(
        """SELECT DISTINCT category FROM challenges 
           WHERE status = 1 AND category IS NOT NULL AND category != ''
           ORDER BY category"""
    )
    category_list = [c['category'] for c in all_categories]
    
    # 构建雷达图数据
    score_map = {cs['category']: round(float(cs['avg_score'] or 0), 1) for cs in category_scores}
    radar_values = [score_map.get(cat, 0) for cat in category_list]
    
    # 获取最近提交记录
    recent_submissions = query_all(
        """SELECT s.id, s.challenge_id, c.title, c.category, c.difficulty,
                  s.total_score, s.stars, s.created_at
           FROM submissions s
           JOIN challenges c ON s.challenge_id = c.id
           WHERE s.user_id = %s
           ORDER BY s.created_at DESC
           LIMIT 10""",
        (student_id,)
    )
    
    recent_list = [{
        'id': s['id'],
        'challenge_id': s['challenge_id'],
        'title': s['title'],
        'category': s['category'],
        'difficulty': s['difficulty'],
        'score': s['total_score'],
        'stars': s['stars'],
        'created_at': s['created_at'].isoformat() if s['created_at'] else None
    } for s in recent_submissions]
    
    return success({
        'student_info': {
            'id': student['id'],
            'username': student['username'],
            'nickname': student['nickname'] or student['username'],
            'email': student['email'],
            'created_at': student['created_at'].isoformat() if student['created_at'] else None
        },
        'radar_data': {
            'dimensions': category_list,
            'values': radar_values
        },
        'recent_submissions': recent_list
    })


@analytics_bp.route('/errors', methods=['GET'])
@login_required
@teacher_required
def get_error_analysis(current_user):
    """
    获取AI聚类分析后的高频错误
    
    查询参数:
        class_id: 班级ID（可选）
        limit: 返回数量（默认10）
    
    返回:
        {
            "code": 200,
            "data": {
                "error_types": [
                    {
                        "type": "语法错误",
                        "count": 25,
                        "examples": ["缺少闭合标签", "属性值未加引号"]
                    },
                    ...
                ]
            }
        }
    """
    teacher_id = current_user['user_id']
    class_id = request.args.get('class_id', type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # 构建学生筛选
    student_filter = ""
    params = []
    
    if class_id:
        student_filter = "AND s.user_id IN (SELECT student_id FROM class_students WHERE class_id = %s)"
        params = [class_id]
    
    # 获取低分提交的AI反馈
    low_score_submissions = query_all(
        f"""SELECT s.ai_feedback, s.ai_summary, c.title, c.category
            FROM submissions s
            JOIN challenges c ON s.challenge_id = c.id
            WHERE s.status = 'completed' 
            AND s.total_score < 60
            AND s.ai_feedback IS NOT NULL
            {student_filter}
            ORDER BY s.created_at DESC
            LIMIT 100
        """,
        tuple(params) if params else None
    )
    
    # 简单的错误类型统计（实际项目中可使用NLP聚类）
    error_keywords = {
        '语法错误': ['语法', '标签', '闭合', '引号', '括号', '缺少'],
        '样式问题': ['样式', 'CSS', '选择器', '布局', '居中', '对齐'],
        '逻辑错误': ['逻辑', '条件', '循环', '判断', '错误'],
        '性能问题': ['性能', '优化', '加载', '渲染'],
        '兼容性问题': ['兼容', '浏览器', '适配']
    }
    
    error_counts = {k: 0 for k in error_keywords}
    error_examples = {k: [] for k in error_keywords}
    
    for s in low_score_submissions:
        feedback = s['ai_feedback'] or ''
        for error_type, keywords in error_keywords.items():
            for keyword in keywords:
                if keyword in feedback:
                    error_counts[error_type] += 1
                    if len(error_examples[error_type]) < 3:
                        error_examples[error_type].append(feedback[:100] + '...')
                    break
    
    # 排序并构建结果
    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    
    error_types = []
    for error_type, count in sorted_errors[:limit]:
        if count > 0:
            error_types.append({
                'type': error_type,
                'count': count,
                'examples': error_examples[error_type][:3]
            })
    
    return success({
        'error_types': error_types,
        'total_analyzed': len(low_score_submissions)
    })


def _get_difficulty_label(difficulty):
    """获取段位中文标签"""
    labels = {
        'bronze': '青铜',
        'silver': '白银',
        'gold': '黄金',
        'diamond': '钻石',
        'king': '王者'
    }
    return labels.get(difficulty, difficulty)
