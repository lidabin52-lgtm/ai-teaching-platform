"""
认证工具模块
提供JWT令牌验证装饰器和用户角色校验
"""
import functools
from flask import request, jsonify, current_app
import jwt
from datetime import datetime


def login_required(f):
    """
    JWT登录验证装饰器
    
    使用方式:
        @app.route('/protected')
        @login_required
        def protected(current_user):
            return jsonify({'user': current_user.username})
    
    验证成功后，current_user参数会注入到视图函数中
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取Token
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header:
            return jsonify({
                'code': 401,
                'message': '未提供认证令牌，请先登录',
                'data': None
            }), 401
        
        # 解析Bearer Token
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'code': 401,
                'message': '令牌格式错误，应为: Bearer <token>',
                'data': None
            }), 401
        
        token = parts[1]
        
        try:
            # 解码JWT令牌
            secret = current_app.config.get('JWT_SECRET', 'jwt-secret-key')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            
            # 检查令牌是否过期
            if payload.get('exp') and datetime.utcnow().timestamp() > payload['exp']:
                return jsonify({
                    'code': 401,
                    'message': '令牌已过期，请重新登录',
                    'data': None
                }), 401
            
            # 将用户信息注入到视图函数参数
            return f(current_user=payload, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'code': 401,
                'message': '令牌已过期，请重新登录',
                'data': None
            }), 401
        except jwt.InvalidTokenError as e:
            return jsonify({
                'code': 401,
                'message': f'无效的令牌: {str(e)}',
                'data': None
            }), 401
        except Exception as e:
            return jsonify({
                'code': 500,
                'message': f'认证过程发生错误: {str(e)}',
                'data': None
            }), 500
    
    return decorated_function


def teacher_required(f):
    """
    教师角色校验装饰器
    
    使用方式:
        @app.route('/teacher-only')
        @login_required
        @teacher_required
        def teacher_only(current_user):
            return jsonify({'message': '教师专属接口'})
    
    注意：需要配合@login_required使用，且放在其后
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # 从参数中获取current_user（由@login_required注入）
        current_user = kwargs.get('current_user')
        
        if not current_user:
            return jsonify({
                'code': 401,
                'message': '未认证的用户',
                'data': None
            }), 401
        
        # 检查角色
        role = current_user.get('role', '')
        if role not in ['teacher', 'admin']:
            return jsonify({
                'code': 403,
                'message': '权限不足，此接口仅限教师访问',
                'data': None
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    管理员角色校验装饰器
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = kwargs.get('current_user')
        
        if not current_user:
            return jsonify({
                'code': 401,
                'message': '未认证的用户',
                'data': None
            }), 401
        
        if current_user.get('role') != 'admin':
            return jsonify({
                'code': 403,
                'message': '权限不足，此接口仅限管理员访问',
                'data': None
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def generate_token(user_id: int, username: str, role: str, expires_hours: int = 24) -> str:
    """
    生成JWT令牌
    
    参数:
        user_id: 用户ID
        username: 用户名
        role: 用户角色
        expires_hours: 过期时间（小时）
    
    返回:
        JWT令牌字符串
    """
    from datetime import datetime, timedelta
    
    secret = current_app.config.get('JWT_SECRET', 'jwt-secret-key')
    
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=expires_hours)
    }
    
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token
