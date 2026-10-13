-- ===========================================
-- 基于大模型的Web前端智能教学与实战训练平台
-- MySQL 8.0 数据库建表脚本
-- 字符集: utf8mb4
-- ===========================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS frontend_edu
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE frontend_edu;

-- ===========================================
-- 1. 用户表 (users)
-- 存储学生和教师信息
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，主键自增',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名，唯一标识',
    password VARCHAR(255) NOT NULL COMMENT '密码，BCrypt加密存储',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱地址，唯一',
    nickname VARCHAR(50) DEFAULT '' COMMENT '昵称，显示名称',
    avatar VARCHAR(500) DEFAULT '' COMMENT '头像URL地址',
    role ENUM('student', 'teacher', 'admin') DEFAULT 'student' COMMENT '角色：student学生/teacher教师/admin管理员',
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0禁用',
    last_login_at DATETIME DEFAULT NULL COMMENT '最后登录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_role (role) COMMENT '按角色查询索引',
    INDEX idx_status (status) COMMENT '按状态查询索引',
    INDEX idx_created_at (created_at) COMMENT '按创建时间排序索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表，存储学生和教师信息';

-- ===========================================
-- 2. 关卡表 (challenges)
-- 技能闯关系统的核心关卡数据
-- ===========================================
CREATE TABLE IF NOT EXISTS challenges (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '关卡ID，主键自增',
    title VARCHAR(200) NOT NULL COMMENT '关卡标题',
    description TEXT NOT NULL COMMENT '关卡需求描述（Markdown格式）',
    difficulty ENUM('bronze', 'silver', 'gold', 'diamond', 'king') NOT NULL DEFAULT 'bronze' COMMENT '段位：bronze青铜/silver白银/gold黄金/diamond钻石/king王者',
    order_num INT UNSIGNED DEFAULT 0 COMMENT '同段位内的排序号，从小到大',
    category VARCHAR(50) NOT NULL COMMENT '分类：HTML/CSS/JavaScript/Vue/React等',
    tags JSON COMMENT '标签数组，如["基础", "布局"]',
    
    -- 代码相关
    starter_code TEXT COMMENT '初始代码模板',
    language VARCHAR(20) DEFAULT 'html' COMMENT '编程语言：html/css/javascript等',
    
    -- AI审判标准（JSON格式存储多维度评分标准）
    scoring_criteria JSON NOT NULL COMMENT '评分标准JSON：{"correctness":30,"code_quality":25,"best_practice":25,"creativity":20}',
    ai_prompt TEXT COMMENT 'AI审判时使用的系统提示词',
    expected_output TEXT COMMENT '期望输出结果描述（用于AI判断）',
    
    -- 关卡配置
    time_limit INT UNSIGNED DEFAULT 0 COMMENT '时间限制（分钟），0表示无限制',
    hint_count INT UNSIGNED DEFAULT 3 COMMENT '可用提示次数',
    unlock_requirement JSON COMMENT '解锁条件JSON：{"prev_challenge_id":1,"min_stars":2}',
    
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1上架/0下架',
    created_by INT UNSIGNED COMMENT '创建者ID（教师）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_difficulty_order (difficulty, order_num) COMMENT '按段位和排序查询',
    INDEX idx_category (category) COMMENT '按分类查询',
    INDEX idx_status (status) COMMENT '按状态查询',
    INDEX idx_created_by (created_by) COMMENT '按创建者查询',
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关卡表，存储技能闯关的所有关卡';

-- ===========================================
-- 3. 学生提交记录表 (submissions)
-- 存储学生闯关提交的代码和AI审判结果
-- ===========================================
CREATE TABLE IF NOT EXISTS submissions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '提交ID，主键自增',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
    challenge_id INT UNSIGNED NOT NULL COMMENT '关卡ID',
    
    -- 提交内容
    code TEXT NOT NULL COMMENT '学生提交的代码',
    code_hash VARCHAR(64) COMMENT '代码内容哈希（用于查重）',
    
    -- AI审判结果
    ai_feedback TEXT COMMENT 'AI评语（详细反馈）',
    ai_summary VARCHAR(500) COMMENT 'AI评语摘要（一句话总结）',
    total_score INT UNSIGNED COMMENT '总分（0-100）',
    stars TINYINT UNSIGNED COMMENT '获得星数（0-3星）',
    
    -- 四维度评分
    score_correctness TINYINT UNSIGNED COMMENT '正确性得分（0-100）',
    score_code_quality TINYINT UNSIGNED COMMENT '代码质量得分（0-100）',
    score_best_practice TINYINT UNSIGNED COMMENT '最佳实践得分（0-100）',
    score_creativity TINYINT UNSIGNED COMMENT '创新性得分（0-100）',
    
    -- 评分详情JSON
    scoring_details JSON COMMENT '评分详情JSON，含各维度评语',
    
    -- 提交状态
    status ENUM('pending', 'judging', 'completed', 'failed') DEFAULT 'pending' COMMENT '状态：pending待审判/judging审判中/completed已完成/failed失败',
    attempt_number INT UNSIGNED DEFAULT 1 COMMENT '第几次尝试',
    time_spent INT UNSIGNED COMMENT '耗时（秒）',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    judged_at DATETIME COMMENT 'AI审判完成时间',
    
    INDEX idx_user_challenge (user_id, challenge_id) COMMENT '按用户和关卡查询',
    INDEX idx_challenge_status (challenge_id, status) COMMENT '按关卡和状态查询',
    INDEX idx_user_status (user_id, status) COMMENT '按用户和状态查询',
    INDEX idx_score (total_score) COMMENT '按分数查询',
    INDEX idx_stars (stars) COMMENT '按星数查询',
    INDEX idx_created_at (created_at) COMMENT '按提交时间排序',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='提交记录表，存储学生代码和AI审判结果';

-- ===========================================
-- 4. AI对话记录表 (ai_conversations)
-- 学生与AI导师的对话历史
-- ===========================================
CREATE TABLE IF NOT EXISTS ai_conversations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '对话ID，主键自增',
    conversation_no VARCHAR(64) NOT NULL UNIQUE COMMENT '对话编号，对外展示用（如CONV202401010001）',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
    challenge_id INT UNSIGNED COMMENT '关联的关卡ID（可为空，表示通用对话）',
    
    title VARCHAR(200) DEFAULT '' COMMENT '对话标题（自动生成或用户设置）',
    message_count INT UNSIGNED DEFAULT 0 COMMENT '消息数量',
    
    -- 知识库引用记录
    knowledge_refs JSON COMMENT '引用的知识库文档ID列表',
    
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0已归档',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后消息时间',
    
    INDEX idx_user (user_id) COMMENT '按用户查询',
    INDEX idx_challenge (challenge_id) COMMENT '按关卡查询',
    INDEX idx_updated_at (updated_at) COMMENT '按更新时间排序',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话表，存储学生与AI导师的对话会话';

-- ===========================================
-- 5. AI消息记录表 (ai_messages)
-- 对话中的具体消息内容
-- ===========================================
CREATE TABLE IF NOT EXISTS ai_messages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID，主键自增',
    conversation_id INT UNSIGNED NOT NULL COMMENT '所属对话ID',
    role ENUM('user', 'assistant', 'system') NOT NULL COMMENT '角色：user学生/assistant AI导师/system系统',
    content TEXT NOT NULL COMMENT '消息内容',
    content_type ENUM('text', 'code', 'image') DEFAULT 'text' COMMENT '内容类型：text文本/code代码/image图片',
    
    -- 代码相关
    code_language VARCHAR(20) COMMENT '代码语言（当content_type=code时）',
    referenced_code TEXT COMMENT '引用的学生代码片段',
    
    -- 元数据
    tokens_used INT UNSIGNED COMMENT '消耗的token数（AI回复时）',
    response_time_ms INT UNSIGNED COMMENT 'AI响应耗时（毫秒）',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    
    INDEX idx_conversation (conversation_id) COMMENT '按对话查询',
    INDEX idx_role (role) COMMENT '按角色查询',
    INDEX idx_created_at (created_at) COMMENT '按时间排序',
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI消息表，存储对话中的具体消息';

-- ===========================================
-- 6. 知识库表 (knowledge_base)
-- AI导师的知识库文档
-- ===========================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '文档ID，主键自增',
    title VARCHAR(200) NOT NULL COMMENT '文档标题',
    content TEXT NOT NULL COMMENT '文档内容（Markdown格式）',
    summary VARCHAR(500) COMMENT '内容摘要',
    
    -- 分类标签
    category VARCHAR(50) NOT NULL COMMENT '分类：HTML/CSS/JavaScript/Vue/React/工具/最佳实践等',
    tags JSON COMMENT '标签数组',
    difficulty ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度：beginner入门/intermediate进阶/advanced高级',
    
    -- 向量检索相关（预留，用于后续RAG优化）
    embedding_vector BLOB COMMENT '文本嵌入向量（二进制存储）',
    
    -- 关联关卡
    related_challenges JSON COMMENT '关联的关卡ID列表',
    
    -- 使用统计
    view_count INT UNSIGNED DEFAULT 0 COMMENT '查看次数',
    reference_count INT UNSIGNED DEFAULT 0 COMMENT '被AI引用次数',
    
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0下架',
    created_by INT UNSIGNED COMMENT '创建者ID（教师）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_category (category) COMMENT '按分类查询',
    INDEX idx_difficulty (difficulty) COMMENT '按难度查询',
    INDEX idx_status (status) COMMENT '按状态查询',
    INDEX idx_created_by (created_by) COMMENT '按创建者查询',
    FULLTEXT INDEX ft_title_content (title, content) COMMENT '标题和内容全文检索',
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库表，存储AI导师的知识文档';

-- ===========================================
-- 7. 学生进度表 (student_progress)
-- 学情分析：记录学生的整体学习进度
-- ===========================================
CREATE TABLE IF NOT EXISTS student_progress (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '进度ID，主键自增',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
    
    -- 各段位进度统计
    bronze_completed INT UNSIGNED DEFAULT 0 COMMENT '青铜段位已完成关卡数',
    bronze_total INT UNSIGNED DEFAULT 0 COMMENT '青铜段位总关卡数',
    silver_completed INT UNSIGNED DEFAULT 0 COMMENT '白银段位已完成关卡数',
    silver_total INT UNSIGNED DEFAULT 0 COMMENT '白银段位总关卡数',
    gold_completed INT UNSIGNED DEFAULT 0 COMMENT '黄金段位已完成关卡数',
    gold_total INT UNSIGNED DEFAULT 0 COMMENT '黄金段位总关卡数',
    diamond_completed INT UNSIGNED DEFAULT 0 COMMENT '钻石段位已完成关卡数',
    diamond_total INT UNSIGNED DEFAULT 0 COMMENT '钻石段位总关卡数',
    king_completed INT UNSIGNED DEFAULT 0 COMMENT '王者段位已完成关卡数',
    king_total INT UNSIGNED DEFAULT 0 COMMENT '王者段位总关卡数',
    
    -- 综合统计
    total_submissions INT UNSIGNED DEFAULT 0 COMMENT '总提交次数',
    total_stars INT UNSIGNED DEFAULT 0 COMMENT '总获得星数',
    avg_score DECIMAL(5,2) DEFAULT 0 COMMENT '平均分',
    current_streak INT UNSIGNED DEFAULT 0 COMMENT '连续打卡天数',
    longest_streak INT UNSIGNED DEFAULT 0 COMMENT '最长连续打卡天数',
    
    last_submission_at DATETIME COMMENT '最后提交时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    UNIQUE KEY uk_user (user_id) COMMENT '每个用户只有一条进度记录',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生进度表，用于学情分析统计';

-- ===========================================
-- 8. 班级表 (classes)
-- 教师管理班级
-- ===========================================
CREATE TABLE IF NOT EXISTS classes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '班级ID，主键自增',
    name VARCHAR(100) NOT NULL COMMENT '班级名称',
    description VARCHAR(500) COMMENT '班级描述',
    invite_code VARCHAR(20) UNIQUE COMMENT '班级邀请码',
    teacher_id INT UNSIGNED NOT NULL COMMENT '班主任教师ID',
    
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0解散',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_teacher (teacher_id) COMMENT '按教师查询',
    INDEX idx_invite_code (invite_code) COMMENT '按邀请码查询',
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级表';

-- ===========================================
-- 9. 班级学生关联表 (class_students)
-- 多对多关系
-- ===========================================
CREATE TABLE IF NOT EXISTS class_students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    class_id INT UNSIGNED NOT NULL COMMENT '班级ID',
    student_id INT UNSIGNED NOT NULL COMMENT '学生ID',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    
    UNIQUE KEY uk_class_student (class_id, student_id) COMMENT '一个学生在同一个班级只能有一条记录',
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学生关联表';

-- ===========================================
-- 初始化：创建默认管理员账号
-- 密码: 123456（实际使用需BCrypt加密）
-- ===========================================
INSERT INTO users (username, password, email, nickname, role, status) VALUES
('admin', '$2b$12$oBSnNVS3/7q88ZWqtUUUE.CYBEkU3p7H7WHPUrLE0s6EC8BhS0Cv6', 'admin@example.com', '系统管理员', 'admin', 1)
ON DUPLICATE KEY UPDATE id=id;
