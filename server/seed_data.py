#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================
数据库初始数据填充脚本
自动创建：教师账号、学生账号、15个关卡、知识库文档
==========================================
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql
from pymysql.cursors import DictCursor
import bcrypt


def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=os.getenv('DB_HOST', os.getenv('MYSQL_HOST', 'localhost')),
        port=int(os.getenv('DB_PORT', os.getenv('MYSQL_PORT', '3306'))),
        user=os.getenv('DB_USER', os.getenv('MYSQL_USER', 'root')),
        password=os.getenv('DB_PASSWORD', os.getenv('MYSQL_PASSWORD', '123456')),
        database=os.getenv('DB_NAME', os.getenv('MYSQL_DATABASE', 'frontend_edu')),
        charset='utf8mb4',
        cursorclass=DictCursor
    )


def hash_password(password):
    """生成密码哈希"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_tables(conn):
    """创建数据库表"""
    print("📋 正在创建数据库表...")
    
    with conn.cursor() as cursor:
        # 用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                nickname VARCHAR(50),
                avatar VARCHAR(255),
                role ENUM('student', 'teacher') DEFAULT 'student',
                status TINYINT DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login_at DATETIME
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 关卡表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                difficulty ENUM('bronze', 'silver', 'gold', 'diamond', 'king') DEFAULT 'bronze',
                order_num INT DEFAULT 1,
                category VARCHAR(50),
                tags JSON,
                starter_code TEXT,
                language VARCHAR(20) DEFAULT 'html',
                scoring_criteria JSON,
                time_limit INT DEFAULT 30,
                hint_count INT DEFAULT 3,
                status TINYINT DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 知识库表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                content TEXT,
                summary TEXT,
                category VARCHAR(50),
                tags JSON,
                status TINYINT DEFAULT 1,
                view_count INT DEFAULT 0,
                reference_count INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 提交记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                challenge_id INT NOT NULL,
                code TEXT,
                code_hash VARCHAR(64),
                status VARCHAR(20) DEFAULT 'pending',
                attempt_number INT DEFAULT 1,
                time_spent INT DEFAULT 0,
                ai_feedback TEXT,
                ai_summary TEXT,
                total_score INT DEFAULT 0,
                stars INT DEFAULT 0,
                score_correctness INT DEFAULT 0,
                score_code_quality INT DEFAULT 0,
                score_best_practice INT DEFAULT 0,
                score_creativity INT DEFAULT 0,
                scoring_details JSON,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                judged_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 学生进度表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                bronze_completed INT DEFAULT 0,
                bronze_total INT DEFAULT 0,
                silver_completed INT DEFAULT 0,
                silver_total INT DEFAULT 0,
                gold_completed INT DEFAULT 0,
                gold_total INT DEFAULT 0,
                diamond_completed INT DEFAULT 0,
                diamond_total INT DEFAULT 0,
                king_completed INT DEFAULT 0,
                king_total INT DEFAULT 0,
                total_submissions INT DEFAULT 0,
                total_stars INT DEFAULT 0,
                avg_score DECIMAL(5,2) DEFAULT 0,
                current_streak INT DEFAULT 0,
                longest_streak INT DEFAULT 0,
                last_submission_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # AI对话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_conversations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                conversation_no VARCHAR(50) NOT NULL UNIQUE,
                user_id INT NOT NULL,
                challenge_id INT,
                title VARCHAR(100),
                message_count INT DEFAULT 0,
                status TINYINT DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # AI消息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                conversation_id INT NOT NULL,
                role ENUM('user', 'assistant', 'system') NOT NULL,
                content TEXT,
                content_type VARCHAR(20) DEFAULT 'text',
                tokens_used INT DEFAULT 0,
                response_time_ms INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
    print("   ✓ 数据库表创建完成\n")


def create_users(conn):
    """创建用户账号"""
    print("📝 正在创建用户账号...")
    
    users_data = []
    
    # 教师账号
    users_data.append({
        'username': 'admin',
        'password': hash_password('123456'),
        'email': 'admin@example.com',
        'nickname': '管理员老师',
        'avatar': 'https://api.dicebear.com/7.x/avataaars/svg?seed=teacher',
        'role': 'teacher'
    })
    print("   ✓ 教师账号: admin / 123456")
    
    # 5个学生账号
    for i in range(1, 6):
        users_data.append({
            'username': f'student{i}',
            'password': hash_password('123456'),
            'email': f'student{i}@example.com',
            'nickname': f'学生{i}号',
            'avatar': f'https://api.dicebear.com/7.x/avataaars/svg?seed=student{i}',
            'role': 'student'
        })
        print(f"   ✓ 学生账号: student{i} / 123456")
    
    with conn.cursor() as cursor:
        for user in users_data:
            cursor.execute("""
                INSERT INTO users (username, password, email, nickname, avatar, role, status)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """, (user['username'], user['password'], user['email'], 
                  user['nickname'], user['avatar'], user['role']))
        
        # 为每个学生创建进度记录
        cursor.execute("SELECT id FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        for student in students:
            cursor.execute("""
                INSERT INTO student_progress (user_id, bronze_total, silver_total, gold_total, diamond_total, king_total)
                VALUES (%s, 5, 4, 3, 2, 1)
            """, (student['id'],))
        
        conn.commit()
    
    print(f"✅ 共创建 {len(users_data)} 个用户账号\n")


def create_challenges(conn):
    """创建15个关卡"""
    print("🎮 正在创建闯关关卡...")
    
    challenges = [
        # 青铜段位（5关）
        {'difficulty': 'bronze', 'order': 1, 'title': 'HTML基础结构', 
         'description': '创建一个标准的HTML5页面结构', 'category': 'HTML'},
        {'difficulty': 'bronze', 'order': 2, 'title': '常用文本标签', 
         'description': '掌握HTML中常用的文本格式化标签', 'category': 'HTML'},
        {'difficulty': 'bronze', 'order': 3, 'title': '链接与图片', 
         'description': '学会在网页中添加超链接和图片', 'category': 'HTML'},
        {'difficulty': 'bronze', 'order': 4, 'title': '表格基础', 
         'description': '创建一个简单的数据表格', 'category': 'HTML'},
        {'difficulty': 'bronze', 'order': 5, 'title': '表单元素', 
         'description': '创建一个用户注册表单', 'category': 'HTML'},
        # 白银段位（4关）
        {'difficulty': 'silver', 'order': 6, 'title': 'CSS选择器', 
         'description': '掌握CSS的各种选择器用法', 'category': 'CSS'},
        {'difficulty': 'silver', 'order': 7, 'title': '盒模型基础', 
         'description': '理解CSS盒模型的各个组成部分', 'category': 'CSS'},
        {'difficulty': 'silver', 'order': 8, 'title': 'Flex布局入门', 
         'description': '掌握Flex布局的基本用法', 'category': 'CSS'},
        {'difficulty': 'silver', 'order': 9, 'title': '定位与层叠', 
         'description': '掌握CSS定位属性', 'category': 'CSS'},
        # 黄金段位（3关）
        {'difficulty': 'gold', 'order': 10, 'title': 'DOM操作基础', 
         'description': '掌握JavaScript DOM操作', 'category': 'JavaScript'},
        {'difficulty': 'gold', 'order': 11, 'title': '事件处理与表单验证', 
         'description': '实现表单验证功能', 'category': 'JavaScript'},
        {'difficulty': 'gold', 'order': 12, 'title': '数组与循环', 
         'description': '掌握JavaScript数组操作和循环', 'category': 'JavaScript'},
        # 钻石段位（2关）
        {'difficulty': 'diamond', 'order': 13, 'title': '待办事项应用', 
         'description': '创建一个功能完整的待办事项应用', 'category': '综合'},
        {'difficulty': 'diamond', 'order': 14, 'title': '图片轮播组件', 
         'description': '创建一个自动轮播的图片组件', 'category': '综合'},
        # 王者段位（1关）
        {'difficulty': 'king', 'order': 15, 'title': '综合实战：个人作品集网站', 
         'description': '运用所学知识创建一个完整的个人作品集网站', 'category': '综合'},
    ]
    
    with conn.cursor() as cursor:
        for c in challenges:
            cursor.execute("""
                INSERT INTO challenges (title, description, difficulty, order_num, category, status, starter_code, scoring_criteria)
                VALUES (%s, %s, %s, %s, %s, 1, '', '{}')
            """, (c['title'], c['description'], c['difficulty'], c['order'], c['category']))
        
        conn.commit()
    
    print(f"✅ 共创建 {len(challenges)} 个关卡\n")


def create_knowledge_base(conn):
    """创建知识库文档"""
    print("📚 正在创建知识库文档...")
    
    docs = [
        {'title': 'HTML基础入门', 'category': 'HTML', 
         'content': 'HTML（HyperText Markup Language）是构建网页的标准标记语言...'},
        {'title': 'CSS选择器详解', 'category': 'CSS', 
         'content': 'CSS选择器用于选择HTML元素并应用样式...'},
        {'title': 'Flexbox布局指南', 'category': 'CSS', 
         'content': 'Flexbox是一种一维布局模型，用于在容器内分配空间...'},
        {'title': 'JavaScript基础语法', 'category': 'JavaScript', 
         'content': 'JavaScript是一种动态编程语言，用于网页交互...'},
        {'title': 'DOM操作完全指南', 'category': 'JavaScript', 
         'content': 'DOM（文档对象模型）是HTML文档的编程接口...'},
        {'title': '响应式设计与媒体查询', 'category': 'CSS', 
         'content': '响应式设计使网页能够适应不同屏幕尺寸...'},
    ]
    
    with conn.cursor() as cursor:
        for doc in docs:
            cursor.execute("""
                INSERT INTO knowledge_base (title, content, category, status)
                VALUES (%s, %s, %s, 1)
            """, (doc['title'], doc['content'], doc['category']))
        
        conn.commit()
    
    print(f"✅ 共创建 {len(docs)} 篇知识库文档\n")


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 数据库初始数据填充脚本")
    print("=" * 50)
    print()
    
    try:
        conn = get_db_connection()
        
        # 创建表
        create_tables(conn)
        
        # 检查是否已有数据
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()['count']
            
            if count > 0:
                print("⚠️  数据库中已存在用户数据，跳过初始化")
                print(f"   现有用户数: {count}")
                conn.close()
                return
        
        # 创建数据
        create_users(conn)
        create_challenges(conn)
        create_knowledge_base(conn)
        
        conn.close()
        
        print("=" * 50)
        print("✨ 数据初始化完成！")
        print("=" * 50)
        print()
        print("📋 账号信息：")
        print("   教师: admin / 123456")
        print("   学生: student1-5 / 123456")
        print()
        print("🎮 关卡数量：15个（青铜5/白银4/黄金3/钻石2/王者1）")
        print("📚 知识库文档：6篇")
        print()
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        raise


if __name__ == "__main__":
    main()
