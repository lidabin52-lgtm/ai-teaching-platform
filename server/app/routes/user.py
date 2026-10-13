"""
用户模块API
处理用户登录、信息获取、进度统计等接口
"""
from flask import Blueprint, request, current_app
import bcrypt
import json

from app.utils.auth import login_required, generate_token
from app.utils.response import success, error, bad_request, not_found
from app.utils.db import query_one, query_all, execute, insert_and_get_id

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    
    请求体:
        {
            "username": "用户名",
            "password": "密码"
        }
    
    返回:
        {
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": "JWT令牌",
                "user": {
                    "id": 1,
                    "username": "xxx",
                    "role": "student",
                    ...
                }
            }
        }
    """
    data = request.get_json()
    
    if not data:
        return bad_request('请求体不能为空')
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # 参数校验
    if not username or not password:
        return bad_request('用户名和密码不能为空')
    
    if len(username) > 50:
        return bad_request('用户名长度不能超过50个字符')
    
    # 查询用户
    user = query_one(
        "SELECT * FROM users WHERE username = %s AND status = 1",
        (username,)
    )
    
    if not user:
        return error('用户名或密码错误', code=401)
    
    # 验证密码（BCrypt）
    try:
        stored_password = user['password']
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        if not bcrypt.checkpw(password, stored_password):
            return error('用户名或密码错误', code=401)
    except Exception as e:
        # 如果BCrypt验证失败，尝试明文比较（仅用于开发环境）
        if user['password'] != data.get('password'):
            return error('用户名或密码错误', code=401)
    
    # 更新最后登录时间
    execute(
        "UPDATE users SET last_login_at = NOW() WHERE id = %s",
        (user['id'],)
    )
    
    # 生成JWT令牌
    token = generate_token(
        user_id=user['id'],
        username=user['username'],
        role=user['role']
    )
    
    # 构建返回的用户信息
    user_info = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'nickname': user['nickname'] or user['username'],
        'avatar': user['avatar'],
        'role': user['role'],
    }
    
    return success({
        'token': token,
        'user': user_info
    }, '登录成功')


@user_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    
    请求体:
        {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱",
            "nickname": "昵称（可选）"
        }
    """
    data = request.get_json()
    
    if not data:
        return bad_request('请求体不能为空')
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip() or username
    
    # 参数校验
    if not username or not password or not email:
        return bad_request('用户名、密码和邮箱不能为空')
    
    if len(username) < 3 or len(username) > 50:
        return bad_request('用户名长度应为3-50个字符')
    
    if len(password) < 6:
        return bad_request('密码长度不能少于6个字符')
    
    if '@' not in email:
        return bad_request('邮箱格式不正确')
    
    # 检查用户名是否已存在
    existing = query_one(
        "SELECT id FROM users WHERE username = %s OR email = %s",
        (username, email)
    )
    
    if existing:
        return error('用户名或邮箱已被注册', code=400)
    
    # 密码加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 插入用户
    user_id = insert_and_get_id(
        """INSERT INTO users (username, password, email, nickname, role, status)
           VALUES (%s, %s, %s, %s, 'student', 1)""",
        (username, hashed_password, email, nickname)
    )
    
    return success({
        'id': user_id,
        'username': username,
        'email': email
    }, '注册成功')


@user_bp.route('/info', methods=['GET'])
@login_required
def get_user_info(current_user):
    """
    获取当前用户信息
    
    返回:
        {
            "code": 200,
            "data": {
                "id": 1,
                "username": "xxx",
                "role": "student",
                "difficulty": "bronze",  // 当前段位
                ...
            }
        }
    """
    user_id = current_user['user_id']
    
    # 查询用户信息
    user = query_one(
        """SELECT id, username, email, nickname, avatar, role, created_at
           FROM users WHERE id = %s""",
        (user_id,)
    )
    
    if not user:
        return not_found('用户不存在')
    
    # 查询用户进度，计算当前段位
    progress = query_one(
        "SELECT * FROM student_progress WHERE user_id = %s",
        (user_id,)
    )
    
    # 计算当前段位（基于已完成的关卡）
    difficulty = 'bronze'
    if progress:
        if progress['king_completed'] > 0:
            difficulty = 'king'
        elif progress['diamond_completed'] > 0:
            difficulty = 'diamond'
        elif progress['gold_completed'] > 0:
            difficulty = 'gold'
        elif progress['silver_completed'] > 0:
            difficulty = 'silver'
    
    user_info = {
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'nickname': user['nickname'] or user['username'],
        'avatar': user['avatar'],
        'role': user['role'],
        'difficulty': difficulty,
        'created_at': user['created_at'].isoformat() if user['created_at'] else None
    }
    
    return success(user_info)


@user_bp.route('/progress', methods=['GET'])
@login_required
def get_user_progress(current_user):
    """
    获取用户闯关进度统计
    
    返回:
        {
            "code": 200,
            "data": {
                "progress": {
                    "bronze": {"completed": 3, "total": 10},
                    "silver": {"completed": 0, "total": 10},
                    ...
                },
                "total_submissions": 15,
                "total_stars": 25,
                "avg_score": 78.5,
                "current_streak": 5,
                "longest_streak": 10
            }
        }
    """
    user_id = current_user['user_id']
    
    # 查询用户进度
    progress = query_one(
        "SELECT * FROM student_progress WHERE user_id = %s",
        (user_id,)
    )
    
    # 如果没有进度记录，创建一个
    if not progress:
        # 先统计各段位的关卡总数
        totals = query_all(
            """SELECT difficulty, COUNT(*) as count 
               FROM challenges WHERE status = 1 
               GROUP BY difficulty"""
        )
        
        total_map = {t['difficulty']: t['count'] for t in totals}
        
        # 创建进度记录
        execute(
            """INSERT INTO student_progress 
               (user_id, bronze_total, silver_total, gold_total, diamond_total, king_total)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id,
             total_map.get('bronze', 0),
             total_map.get('silver', 0),
             total_map.get('gold', 0),
             total_map.get('diamond', 0),
             total_map.get('king', 0))
        )
        
        progress = query_one(
            "SELECT * FROM student_progress WHERE user_id = %s",
            (user_id,)
        )
    
    # 构建进度数据
    progress_data = {
        'bronze': {
            'completed': progress['bronze_completed'] or 0,
            'total': progress['bronze_total'] or 0
        },
        'silver': {
            'completed': progress['silver_completed'] or 0,
            'total': progress['silver_total'] or 0
        },
        'gold': {
            'completed': progress['gold_completed'] or 0,
            'total': progress['gold_total'] or 0
        },
        'diamond': {
            'completed': progress['diamond_completed'] or 0,
            'total': progress['diamond_total'] or 0
        },
        'king': {
            'completed': progress['king_completed'] or 0,
            'total': progress['king_total'] or 0
        }
    }
    
    result = {
        'progress': progress_data,
        'total_submissions': progress['total_submissions'] or 0,
        'total_stars': progress['total_stars'] or 0,
        'avg_score': float(progress['avg_score']) if progress['avg_score'] else 0,
        'current_streak': progress['current_streak'] or 0,
        'longest_streak': progress['longest_streak'] or 0,
        'last_submission_at': progress['last_submission_at'].isoformat() if progress['last_submission_at'] else None
    }
    
    return success(result)


@user_bp.route('/submissions', methods=['GET'])
@login_required
def get_user_submissions(current_user):
    """
    获取用户的所有提交记录
    
    查询参数:
        page: 页码（默认1）
        page_size: 每页数量（默认10）
        challenge_id: 关卡ID（可选，筛选特定关卡）
    """
    user_id = current_user['user_id']
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    challenge_id = request.args.get('challenge_id', type=int)
    
    # 构建查询条件
    where_clause = "WHERE s.user_id = %s"
    params = [user_id]
    
    if challenge_id:
        where_clause += " AND s.challenge_id = %s"
        params.append(challenge_id)
    
    # 查询总数
    count_sql = f"SELECT COUNT(*) as total FROM submissions s {where_clause}"
    total = query_one(count_sql, tuple(params))['total']
    
    # 查询列表
    offset = (page - 1) * page_size
    params.extend([page_size, offset])
    
    submissions = query_all(
        f"""SELECT s.*, c.title as challenge_title, c.difficulty, c.category
            FROM submissions s
            LEFT JOIN challenges c ON s.challenge_id = c.id
            {where_clause}
            ORDER BY s.created_at DESC
            LIMIT %s OFFSET %s""",
        tuple(params)
    )
    
    # 格式化数据
    items = []
    for s in submissions:
        items.append({
            'id': s['id'],
            'challenge_id': s['challenge_id'],
            'challenge_title': s['challenge_title'],
            'difficulty': s['difficulty'],
            'category': s['category'],
            'total_score': s['total_score'],
            'stars': s['stars'],
            'status': s['status'],
            'ai_summary': s['ai_summary'],
            'created_at': s['created_at'].isoformat() if s['created_at'] else None
        })
    
    from app.utils.response import paginate
    return jsonify(paginate(items, total, page, page_size))
