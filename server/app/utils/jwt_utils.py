"""
JWT令牌工具模块
提供JWT令牌的生成和验证功能
"""
import jwt
import datetime
from flask import current_app


def generate_token(user_id, username, expires_hours=None):
    """
    生成JWT令牌

    参数:
        user_id: 用户ID
        username: 用户名
        expires_hours: 过期时间（小时），默认使用配置值

    返回:
        JWT令牌字符串
    """
    if expires_hours is None:
        expires_hours = current_app.config.get('JWT_EXPIRATION_HOURS', 24)

    secret = current_app.config.get('JWT_SECRET', 'jwt-secret-key')

    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def verify_token(token):
    """
    验证JWT令牌

    参数:
        token: JWT令牌字符串

    返回:
        验证成功: 载荷字典
        验证失败: None
    """
    secret = current_app.config.get('JWT_SECRET', 'jwt-secret-key')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("令牌已过期")
        return None
    except jwt.InvalidTokenError:
        print("无效令牌")
        return None
