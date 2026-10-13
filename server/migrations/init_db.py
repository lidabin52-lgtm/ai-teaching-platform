"""
数据库初始化脚本
自动创建数据库表并插入3个青铜关卡示例数据

使用方法:
    python init_db.py

环境变量:
    MYSQL_HOST: 数据库主机 (默认: localhost)
    MYSQL_PORT: 数据库端口 (默认: 3306)
    MYSQL_USER: 数据库用户名 (默认: root)
    MYSQL_PASSWORD: 数据库密码 (默认: 123456)
    MYSQL_DATABASE: 数据库名 (默认: frontend_edu)
"""
import os
import sys
import pymysql
from datetime import datetime


# ========== 数据库配置 ==========
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', '123456'),
    'database': os.getenv('MYSQL_DATABASE', 'frontend_edu'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


# ========== 3个青铜关卡示例数据 ==========
BRONZE_CHALLENGES = [
    {
        'title': 'HTML基础：创建第一个网页',
        'description': '''## 🎯 任务目标
创建一个简单的HTML页面，展示个人简介。

## 📋 具体要求
1. 页面标题为"我的个人主页"
2. 包含一个一级标题`<h1>`，内容为你的名字
3. 包含一个段落`<p>`，介绍你自己（至少50字）
4. 包含一个无序列表`<ul>`，列出你的3个兴趣爱好
5. 添加一张图片`<img>`（可以使用任意图片URL）

## 💡 提示
- 记得使用正确的HTML文档结构`<!DOCTYPE html>`、`<html>`、`<head>`、`<body>`
- 图片需要设置`alt`属性
- 列表项使用`<li>`标签

## ✅ 验收标准
- 页面结构完整且符合HTML5规范
- 所有要求的元素都已包含
- 代码格式清晰，有适当的缩进''',
        'difficulty': 'bronze',
        'order_num': 1,
        'category': 'HTML',
        'tags': ['基础', 'HTML结构', '标签'],
        'starter_code': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的个人主页</title>
</head>
<body>
    <!-- 在这里编写你的代码 -->
    
</body>
</html>''',
        'language': 'html',
        'scoring_criteria': {
            'correctness': 40,      # 正确性：HTML结构是否正确
            'code_quality': 30,     # 代码质量：格式、语义化
            'best_practice': 20,    # 最佳实践：alt属性、meta标签
            'creativity': 10        # 创新性：内容创意
        },
        'ai_prompt': '''你是一个HTML教学专家。请评判学生的HTML代码，重点关注：
1. HTML文档结构是否完整（DOCTYPE、html、head、body）
2. 是否正确使用了h1、p、ul、li、img标签
3. 图片是否有alt属性
4. 代码格式是否规范
5. 内容是否满足要求

请给出总分（0-100）和四个维度的得分，以及详细的改进建议。''',
        'expected_output': '一个包含个人简介、兴趣爱好列表和图片的完整HTML页面',
        'time_limit': 30,
        'hint_count': 3,
    },
    {
        'title': 'CSS选择器：美化个人主页',
        'description': '''## 🎯 任务目标
为上一关创建的HTML页面添加CSS样式，让它更加美观。

## 📋 具体要求
1. 为整个页面设置背景颜色（建议使用柔和的颜色如`#f5f5f5`）
2. 将一级标题`<h1>`设置为居中显示，颜色改为深蓝色（`#2c3e50`）
3. 为段落`<p>`设置字体大小为16px，行高为1.6
4. 为无序列表`<ul>`添加自定义的项目符号（使用`list-style-type`）
5. 为图片`<img>`添加圆角边框（`border-radius: 8px`）和阴影效果
6. 添加一个类名为`.highlight`的样式，使文字背景变为黄色

## 💡 提示
- 可以使用内联样式、内部样式表或外部样式表
- 建议使用内部样式表（`<style>`标签放在`<head>`中）
- 使用类选择器和元素选择器

## ✅ 验收标准
- 所有样式要求都已实现
- 选择器使用正确
- 页面视觉效果美观''',
        'difficulty': 'bronze',
        'order_num': 2,
        'category': 'CSS',
        'tags': ['基础', '选择器', '样式美化'],
        'starter_code': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的个人主页</title>
    <style>
        /* 在这里编写你的CSS代码 */
        
    </style>
</head>
<body>
    <h1>张三</h1>
    <p>我是一名热爱前端开发的学生，喜欢探索新技术...</p>
    <ul>
        <li>编程</li>
        <li>阅读</li>
        <li>旅行</li>
    </ul>
    <img src="https://via.placeholder.com/200" alt="个人照片">
</body>
</html>''',
        'language': 'html',
        'scoring_criteria': {
            'correctness': 35,
            'code_quality': 35,
            'best_practice': 20,
            'creativity': 10
        },
        'ai_prompt': '''你是一个CSS教学专家。请评判学生的CSS代码，重点关注：
1. 选择器使用是否正确（元素选择器、类选择器）
2. 样式属性是否有效（background-color、text-align、font-size等）
3. 是否实现了所有要求的样式效果
4. 代码组织是否清晰
5. 视觉效果是否美观

请给出总分（0-100）和四个维度的得分，以及详细的改进建议。''',
        'expected_output': '一个样式美观的个人主页，包含背景色、居中标题、自定义列表样式、圆角图片等',
        'time_limit': 30,
        'hint_count': 3,
        'unlock_requirement': {'prev_challenge_id': 1, 'min_stars': 1},
    },
    {
        'title': 'Flex布局：创建响应式卡片',
        'description': '''## 🎯 任务目标
使用Flexbox布局创建一个响应式的卡片布局，展示3个技能卡片。

## 📋 具体要求
1. 创建一个容器`<div class="skills-container">`，使用Flex布局
2. 在容器内创建3个卡片`<div class="skill-card">`
3. 每个卡片包含：
   - 一个图标（使用emoji或文字表示，如💻 📱 🎨）
   - 一个标题`<h3>`（技能名称）
   - 一段描述`<p>`（技能介绍）
4. 设置卡片样式：
   - 宽度为200px，高度自适应
   - 背景色为白色，边框为1px solid #ddd
   - 内边距为20px，外边距为10px
   - 圆角为8px
5. 使用Flex布局让3个卡片水平排列，并且在容器内居中对齐
6. 添加`flex-wrap: wrap`，使卡片在小屏幕时自动换行

## 💡 提示
- Flex容器属性：`display: flex`、`justify-content`、`flex-wrap`
- 卡片样式建议添加阴影效果提升视觉效果
- 可以使用`gap`属性设置卡片间距

## ✅ 验收标准
- 正确使用Flexbox布局
- 3个卡片水平排列且居中对齐
- 卡片样式符合要求
- 响应式效果正常（缩小窗口时卡片换行）''',
        'difficulty': 'bronze',
        'order_num': 3,
        'category': 'CSS',
        'tags': ['基础', 'Flexbox', '响应式', '布局'],
        'starter_code': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的技能展示</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f5f5f5;
            padding: 40px;
        }
        
        .skills-container {
            /* 在这里编写Flex布局代码 */
            
        }
        
        .skill-card {
            /* 在这里编写卡片样式 */
            
        }
        
        .skill-icon {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .skill-card h3 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .skill-card p {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="skills-container">
        <!-- 第一个技能卡片 -->
        <div class="skill-card">
            <div class="skill-icon">💻</div>
            <h3>前端开发</h3>
            <p>熟练掌握HTML、CSS、JavaScript，能够构建响应式网页应用。</p>
        </div>
        
        <!-- 第二个技能卡片 -->
        <div class="skill-card">
            <div class="skill-icon">📱</div>
            <h3>移动开发</h3>
            <p>了解移动端适配方案，能够开发适配各种屏幕的网页。</p>
        </div>
        
        <!-- 第三个技能卡片 -->
        <div class="skill-card">
            <div class="skill-icon">🎨</div>
            <h3>UI设计</h3>
            <p>具备良好的审美能力，能够设计简洁美观的用户界面。</p>
        </div>
    </div>
</body>
</html>''',
        'language': 'html',
        'scoring_criteria': {
            'correctness': 40,
            'code_quality': 30,
            'best_practice': 20,
            'creativity': 10
        },
        'ai_prompt': '''你是一个CSS Flexbox教学专家。请评判学生的Flexbox布局代码，重点关注：
1. 是否正确设置了`display: flex`
2. `justify-content`属性是否正确使用（实现居中对齐）
3. `flex-wrap`是否正确设置（实现响应式换行）
4. 卡片样式是否符合要求（宽度、边框、圆角等）
5. 是否使用了`gap`或其他方式设置间距
6. 响应式效果是否正常

请给出总分（0-100）和四个维度的得分，以及详细的改进建议。''',
        'expected_output': '一个使用Flexbox布局的响应式卡片展示，3个卡片水平排列，小屏幕时自动换行',
        'time_limit': 40,
        'hint_count': 3,
        'unlock_requirement': {'prev_challenge_id': 2, 'min_stars': 1},
    },
]


# ========== 知识库示例数据 ==========
KNOWLEDGE_BASE_DOCS = [
    {
        'title': 'HTML基础入门指南',
        'content': '''# HTML基础入门指南

## 什么是HTML？
HTML（HyperText Markup Language）是构建网页的标准标记语言。

## 基本结构
```html
<!DOCTYPE html>
<html>
<head>
    <title>页面标题</title>
</head>
<body>
    <h1>这是一个标题</h1>
    <p>这是一个段落。</p>
</body>
</html>
```

## 常用标签
- `<h1>` ~ `<h6>`：标题
- `<p>`：段落
- `<a>`：链接
- `<img>`：图片
- `<ul>` / `<ol>`：列表
- `<div>`：容器

## 最佳实践
1. 始终使用正确的文档类型声明
2. 为图片添加alt属性
3. 使用语义化标签''',
        'summary': 'HTML基础入门，包含基本结构和常用标签介绍',
        'category': 'HTML',
        'tags': ['基础', 'HTML', '入门'],
        'difficulty': 'beginner',
    },
    {
        'title': 'CSS选择器完全指南',
        'content': '''# CSS选择器完全指南

## 基本选择器

### 元素选择器
```css
p {
    color: blue;
}
```

### 类选择器
```css
.highlight {
    background-color: yellow;
}
```

### ID选择器
```css
#header {
    font-size: 24px;
}
```

## 组合选择器
- `A B`：后代选择器
- `A > B`：子元素选择器
- `A + B`：相邻兄弟选择器
- `A ~ B`：通用兄弟选择器

## 伪类选择器
- `:hover`：鼠标悬停
- `:nth-child()`：第n个子元素
- `:first-child`：第一个子元素''',
        'summary': 'CSS选择器详解，包括基本选择器、组合选择器和伪类选择器',
        'category': 'CSS',
        'tags': ['基础', 'CSS', '选择器'],
        'difficulty': 'beginner',
    },
    {
        'title': 'Flexbox布局详解',
        'content': '''# Flexbox布局详解

## 什么是Flexbox？
Flexbox是一种一维布局模型，用于在容器内排列元素。

## 容器属性

### display
```css
.container {
    display: flex;  /* 或 inline-flex */
}
```

### justify-content（主轴对齐）
- `flex-start`：左对齐
- `center`：居中
- `flex-end`：右对齐
- `space-between`：两端对齐
- `space-around`：均匀分布

### align-items（交叉轴对齐）
- `stretch`：拉伸
- `center`：居中
- `flex-start`：顶部对齐
- `flex-end`：底部对齐

### flex-wrap
- `nowrap`：不换行（默认）
- `wrap`：换行
- `wrap-reverse`：反向换行

## 项目属性
- `flex-grow`：放大比例
- `flex-shrink`：缩小比例
- `flex-basis`：基础大小
- `flex`：简写属性''',
        'summary': 'Flexbox布局完全指南，包含容器属性和项目属性详解',
        'category': 'CSS',
        'tags': ['基础', 'CSS', 'Flexbox', '布局'],
        'difficulty': 'beginner',
    },
]


def create_database():
    """创建数据库（如果不存在）"""
    config = DB_CONFIG.copy()
    database = config.pop('database')
    
    try:
        conn = pymysql.connect(**config)
        with conn.cursor() as cursor:
            cursor.execute(f"""
                CREATE DATABASE IF NOT EXISTS {database}
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci
            """)
            print(f"✅ 数据库 '{database}' 创建成功或已存在")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False


def execute_sql_file(cursor, filepath):
    """执行SQL文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
            # 先去掉以 -- 开头的整行注释，再按分号分割语句
            # （原逻辑按 ';' 块跳过 startswith('--') 的语句，
            #   导致每条前面带注释的 CREATE TABLE 都被整块跳过）
            lines = [line for line in sql.splitlines()
                     if not line.strip().startswith('--')]
            statements = [s.strip() for s in '\n'.join(lines).split(';')
                          if s.strip()]
            for statement in statements:
                cursor.execute(statement)
        return True
    except Exception as e:
        print(f"❌ 执行SQL文件失败: {e}")
        return False


def init_tables():
    """初始化数据表"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_file = os.path.join(current_dir, 'schema.sql')
            
            if os.path.exists(schema_file):
                execute_sql_file(cursor, schema_file)
                print("✅ 数据表创建成功")
            else:
                print(f"❌ 找不到schema.sql文件: {schema_file}")
                return False
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 创建数据表失败: {e}")
        return False


def insert_sample_data():
    """插入示例数据"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # ========== 插入管理员用户 ==========
            cursor.execute("""
                INSERT IGNORE INTO users (id, username, password, email, nickname, role, status)
                VALUES (1, 'admin', '$2b$12$oBSnNVS3/7q88ZWqtUUUE.CYBEkU3p7H7WHPUrLE0s6EC8BhS0Cv6', 
                        'admin@example.com', '系统管理员', 'admin', 1)
            """)
            print("✅ 管理员用户创建成功")
            
            # ========== 插入示例教师 ==========
            cursor.execute("""
                INSERT IGNORE INTO users (id, username, password, email, nickname, role, status)
                VALUES (2, 'teacher1', '$2b$12$oBSnNVS3/7q88ZWqtUUUE.CYBEkU3p7H7WHPUrLE0s6EC8BhS0Cv6', 
                        'teacher1@example.com', '张老师', 'teacher', 1)
            """)
            print("✅ 示例教师创建成功")
            
            # ========== 插入青铜关卡 ==========
            for i, challenge in enumerate(BRONZE_CHALLENGES, 1):
                cursor.execute("""
                    INSERT INTO challenges (
                        id, title, description, difficulty, order_num, category, tags,
                        starter_code, language, scoring_criteria, ai_prompt, expected_output,
                        time_limit, hint_count, unlock_requirement, status, created_by
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 2
                    ) ON DUPLICATE KEY UPDATE
                        title = VALUES(title),
                        description = VALUES(description),
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    i,
                    challenge['title'],
                    challenge['description'],
                    challenge['difficulty'],
                    challenge['order_num'],
                    challenge['category'],
                    json.dumps(challenge['tags']) if 'tags' in challenge else None,
                    challenge['starter_code'],
                    challenge['language'],
                    json.dumps(challenge['scoring_criteria']),
                    challenge['ai_prompt'],
                    challenge['expected_output'],
                    challenge['time_limit'],
                    challenge['hint_count'],
                    json.dumps(challenge['unlock_requirement']) if challenge.get('unlock_requirement') else None,
                ))
            print(f"✅ 插入 {len(BRONZE_CHALLENGES)} 个青铜关卡")
            
            # ========== 插入知识库文档 ==========
            for i, doc in enumerate(KNOWLEDGE_BASE_DOCS, 1):
                cursor.execute("""
                    INSERT INTO knowledge_base (
                        id, title, content, summary, category, tags, difficulty, status, created_by
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, 1, 2
                    ) ON DUPLICATE KEY UPDATE
                        title = VALUES(title),
                        content = VALUES(content),
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    i,
                    doc['title'],
                    doc['content'],
                    doc['summary'],
                    doc['category'],
                    json.dumps(doc['tags']),
                    doc['difficulty'],
                ))
            print(f"✅ 插入 {len(KNOWLEDGE_BASE_DOCS)} 个知识库文档")
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 插入示例数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_data():
    """验证数据插入结果"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 查询关卡数量
            cursor.execute("SELECT COUNT(*) as count FROM challenges WHERE difficulty = 'bronze'")
            challenge_count = cursor.fetchone()['count']
            
            # 查询知识库数量
            cursor.execute("SELECT COUNT(*) as count FROM knowledge_base")
            kb_count = cursor.fetchone()['count']
            
            # 查询用户数量
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            print("\n" + "="*50)
            print("📊 数据验证结果:")
            print(f"   用户数量: {user_count}")
            print(f"   青铜关卡: {challenge_count}")
            print(f"   知识库文档: {kb_count}")
            print("="*50)
            
            # 显示关卡列表
            cursor.execute("""
                SELECT id, title, difficulty, category 
                FROM challenges 
                ORDER BY difficulty, order_num
            """)
            challenges = cursor.fetchall()
            print("\n📋 关卡列表:")
            for c in challenges:
                print(f"   [{c['id']}] {c['title']} ({c['difficulty']})")
            
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 验证数据失败: {e}")
        return False


def main():
    """主函数"""
    print("="*60)
    print("🚀 AI前端智能教学平台 - 数据库初始化脚本")
    print("="*60)
    print(f"\n数据库配置:")
    print(f"   主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"   数据库: {DB_CONFIG['database']}")
    print(f"   用户: {DB_CONFIG['user']}")
    print()
    
    # 步骤1: 创建数据库
    print("📌 步骤 1/4: 创建数据库...")
    if not create_database():
        sys.exit(1)
    
    # 步骤2: 创建数据表
    print("\n📌 步骤 2/4: 创建数据表...")
    if not init_tables():
        sys.exit(1)
    
    # 步骤3: 插入示例数据
    print("\n📌 步骤 3/4: 插入示例数据...")
    if not insert_sample_data():
        sys.exit(1)
    
    # 步骤4: 验证数据
    print("\n📌 步骤 4/4: 验证数据...")
    if not verify_data():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ 数据库初始化完成！")
    print("="*60)
    print("\n📝 提示:")
    print("   - 管理员账号: admin / 123456")
    print("   - 教师账号: teacher1 / 123456")
    print("   - 已创建 3 个青铜关卡示例数据")
    print("   - 已创建 3 个知识库文档")
    print()


if __name__ == '__main__':
    import json
    main()
