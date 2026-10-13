"""
数据库操作工具模块
提供PyMySQL数据库连接和基础CRUD操作
"""
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from flask import current_app
from typing import Optional, List, Dict, Any


def get_db_config() -> dict:
    """
    获取数据库配置
    从Flask应用配置中读取
    """
    return {
        'host': current_app.config.get('MYSQL_HOST', 'localhost'),
        'port': current_app.config.get('MYSQL_PORT', 3306),
        'user': current_app.config.get('MYSQL_USER', 'root'),
        'password': current_app.config.get('MYSQL_PASSWORD', '123456'),
        'database': current_app.config.get('MYSQL_DATABASE', 'frontend_edu'),
        'charset': 'utf8mb4',
        'cursorclass': DictCursor,
    }


@contextmanager
def get_db():
    """
    获取数据库连接的上下文管理器
    
    使用方式:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
    """
    conn = None
    try:
        conn = pymysql.connect(**get_db_config())
        yield conn
    except pymysql.Error as e:
        print(f"数据库连接错误: {e}")
        raise
    finally:
        if conn:
            conn.close()


def query_one(sql: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """
    查询单条记录
    
    参数:
        sql: SQL语句
        params: 参数元组
    
    返回:
        单条记录字典或None
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()


def query_all(sql: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    查询多条记录
    
    参数:
        sql: SQL语句
        params: 参数元组
    
    返回:
        记录列表
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


def execute(sql: str, params: tuple = None) -> int:
    """
    执行SQL语句（INSERT/UPDATE/DELETE）
    
    参数:
        sql: SQL语句
        params: 参数元组
    
    返回:
        受影响的行数
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            affected = cursor.execute(sql, params)
            conn.commit()
            return affected


def insert_and_get_id(sql: str, params: tuple = None) -> int:
    """
    插入记录并返回自增ID
    
    参数:
        sql: INSERT语句
        params: 参数元组
    
    返回:
        新记录的ID
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
