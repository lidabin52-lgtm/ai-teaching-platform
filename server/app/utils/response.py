"""
统一响应工具模块
提供标准化的API响应格式
"""
from flask import jsonify
from typing import Any, Optional


def success(data: Any = None, message: str = '操作成功', code: int = 200):
    """
    成功响应
    
    参数:
        data: 响应数据
        message: 响应消息
        code: 业务状态码
    
    返回:
        Flask响应对象
    """
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return jsonify(response), 200


def error(message: str = '操作失败', code: int = 500, data: Any = None):
    """
    错误响应
    
    参数:
        message: 错误消息
        code: 错误状态码
        data: 附加数据
    
    返回:
        Flask响应对象
    """
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return jsonify(response), 200


def bad_request(message: str = '请求参数错误', data: Any = None):
    """400 Bad Request"""
    return error(message=message, code=400, data=data)


def unauthorized(message: str = '未授权，请先登录', data: Any = None):
    """401 Unauthorized"""
    return error(message=message, code=401, data=data)


def forbidden(message: str = '权限不足', data: Any = None):
    """403 Forbidden"""
    return error(message=message, code=403, data=data)


def not_found(message: str = '资源不存在', data: Any = None):
    """404 Not Found"""
    return error(message=message, code=404, data=data)


def paginate(items: list, total: int, page: int, page_size: int, 
             message: str = '获取成功') -> dict:
    """
    分页数据格式化
    
    参数:
        items: 数据列表
        total: 总数量
        page: 当前页码
        page_size: 每页数量
        message: 响应消息
    
    返回:
        分页数据字典
    """
    return {
        'code': 200,
        'message': message,
        'data': {
            'list': items,
            'pagination': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if page_size > 0 else 0
            }
        }
    }
