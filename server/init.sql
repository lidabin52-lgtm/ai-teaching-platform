-- ===========================================
-- 基于大模型的Web前端智能教学与实战训练平台
-- MySQL 8.0 数据库初始化脚本（Docker 首次启动执行）
-- 数据库: frontend_edu（与 docker-compose.yml 中 MYSQL_DATABASE 保持一致）
-- 字符集: utf8mb4
-- ===========================================

CREATE DATABASE IF NOT EXISTS frontend_edu
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE frontend_edu;

-- ===========================================
-- 1. 用户表 (users)
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
    INDEX idx_role (role),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表，存储学生和教师信息';

-- ===========================================
-- 2. 关卡表 (challenges)
-- ===========================================
CREATE TABLE IF NOT EXISTS challenges (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '关卡ID，主键自增',
    title VARCHAR(200) NOT NULL COMMENT '关卡标题',
    description TEXT NOT NULL COMMENT '关卡需求描述（Markdown格式）',
    difficulty ENUM('bronze', 'silver', 'gold', 'diamond', 'king') NOT NULL DEFAULT 'bronze' COMMENT '段位',
    order_num INT UNSIGNED DEFAULT 0 COMMENT '同段位内的排序号',
    category VARCHAR(50) NOT NULL COMMENT '分类：HTML/CSS/JavaScript/Vue/React等',
    tags JSON COMMENT '标签数组',
    starter_code TEXT COMMENT '初始代码模板',
    language VARCHAR(20) DEFAULT 'html' COMMENT '编程语言',
    scoring_criteria JSON NOT NULL COMMENT '评分标准JSON',
    ai_prompt TEXT COMMENT 'AI审判时使用的系统提示词',
    expected_output TEXT COMMENT '期望输出结果描述',
    time_limit INT UNSIGNED DEFAULT 0 COMMENT '时间限制（分钟），0表示无限制',
    hint_count INT UNSIGNED DEFAULT 3 COMMENT '可用提示次数',
    unlock_requirement JSON COMMENT '解锁条件JSON',
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1上架/0下架',
    created_by INT UNSIGNED COMMENT '创建者ID（教师）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_difficulty_order (difficulty, order_num),
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_created_by (created_by),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关卡表，存储技能闯关的所有关卡';

-- ===========================================
-- 3. 学生提交记录表 (submissions)
-- ===========================================
CREATE TABLE IF NOT EXISTS submissions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '提交ID，主键自增',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
    challenge_id INT UNSIGNED NOT NULL COMMENT '关卡ID',
    code TEXT NOT NULL COMMENT '学生提交的代码',
    code_hash VARCHAR(64) COMMENT '代码内容哈希（用于查重）',
    ai_feedback TEXT COMMENT 'AI评语（详细反馈）',
    ai_summary VARCHAR(500) COMMENT 'AI评语摘要',
    total_score INT UNSIGNED COMMENT '总分（0-100）',
    stars TINYINT UNSIGNED COMMENT '获得星数（0-3星）',
    score_correctness TINYINT UNSIGNED COMMENT '正确性得分（0-100）',
    score_code_quality TINYINT UNSIGNED COMMENT '代码质量得分（0-100）',
    score_best_practice TINYINT UNSIGNED COMMENT '最佳实践得分（0-100）',
    score_creativity TINYINT UNSIGNED COMMENT '创新性得分（0-100）',
    scoring_details JSON COMMENT '评分详情JSON',
    status ENUM('pending', 'judging', 'completed', 'failed') DEFAULT 'pending' COMMENT '状态',
    attempt_number INT UNSIGNED DEFAULT 1 COMMENT '第几次尝试',
    time_spent INT UNSIGNED COMMENT '耗时（秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    judged_at DATETIME COMMENT 'AI审判完成时间',
    INDEX idx_user_challenge (user_id, challenge_id),
    INDEX idx_challenge_status (challenge_id, status),
    INDEX idx_user_status (user_id, status),
    INDEX idx_score (total_score),
    INDEX idx_stars (stars),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='提交记录表，存储学生代码和AI审判结果';

-- ===========================================
-- 4. AI对话记录表 (ai_conversations)
-- ===========================================
CREATE TABLE IF NOT EXISTS ai_conversations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '对话ID，主键自增',
    conversation_no VARCHAR(64) NOT NULL UNIQUE COMMENT '对话编号',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
    challenge_id INT UNSIGNED COMMENT '关联的关卡ID（可为空）',
    title VARCHAR(200) DEFAULT '' COMMENT '对话标题',
    message_count INT UNSIGNED DEFAULT 0 COMMENT '消息数量',
    knowledge_refs JSON COMMENT '引用的知识库文档ID列表',
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0已归档',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后消息时间',
    INDEX idx_user (user_id),
    INDEX idx_challenge (challenge_id),
    INDEX idx_updated_at (updated_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话表，存储学生与AI导师的对话会话';

-- ===========================================
-- 5. AI消息记录表 (ai_messages)
-- ===========================================
CREATE TABLE IF NOT EXISTS ai_messages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID，主键自增',
    conversation_id INT UNSIGNED NOT NULL COMMENT '所属对话ID',
    role ENUM('user', 'assistant', 'system') NOT NULL COMMENT '角色',
    content TEXT NOT NULL COMMENT '消息内容',
    content_type ENUM('text', 'code', 'image') DEFAULT 'text' COMMENT '内容类型',
    code_language VARCHAR(20) COMMENT '代码语言',
    referenced_code TEXT COMMENT '引用的学生代码片段',
    tokens_used INT UNSIGNED COMMENT '消耗的token数',
    response_time_ms INT UNSIGNED COMMENT 'AI响应耗时（毫秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    INDEX idx_conversation (conversation_id),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI消息表，存储对话中的具体消息';

-- ===========================================
-- 6. 知识库表 (knowledge_base)
-- ===========================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '文档ID，主键自增',
    title VARCHAR(200) NOT NULL COMMENT '文档标题',
    content TEXT NOT NULL COMMENT '文档内容（Markdown格式）',
    summary VARCHAR(500) COMMENT '内容摘要',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    tags JSON COMMENT '标签数组',
    difficulty ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度',
    embedding_vector BLOB COMMENT '文本嵌入向量',
    related_challenges JSON COMMENT '关联的关卡ID列表',
    view_count INT UNSIGNED DEFAULT 0 COMMENT '查看次数',
    reference_count INT UNSIGNED DEFAULT 0 COMMENT '被AI引用次数',
    status TINYINT UNSIGNED DEFAULT 1 COMMENT '状态：1正常/0下架',
    created_by INT UNSIGNED COMMENT '创建者ID（教师）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    INDEX idx_status (status),
    INDEX idx_created_by (created_by),
    FULLTEXT INDEX ft_title_content (title, content),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库表，存储AI导师的知识文档';

-- ===========================================
-- 7. 学生进度表 (student_progress)
-- ===========================================
CREATE TABLE IF NOT EXISTS student_progress (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '进度ID，主键自增',
    user_id INT UNSIGNED NOT NULL COMMENT '学生用户ID',
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
    total_submissions INT UNSIGNED DEFAULT 0 COMMENT '总提交次数',
    total_stars INT UNSIGNED DEFAULT 0 COMMENT '总获得星数',
    avg_score DECIMAL(5,2) DEFAULT 0 COMMENT '平均分',
    current_streak INT UNSIGNED DEFAULT 0 COMMENT '连续打卡天数',
    longest_streak INT UNSIGNED DEFAULT 0 COMMENT '最长连续打卡天数',
    last_submission_at DATETIME COMMENT '最后提交时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生进度表，用于学情分析统计';

-- ===========================================
-- 8. 班级表 (classes)
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
    INDEX idx_teacher (teacher_id),
    INDEX idx_invite_code (invite_code),
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级表';

-- ===========================================
-- 9. 班级学生关联表 (class_students)
-- ===========================================
CREATE TABLE IF NOT EXISTS class_students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    class_id INT UNSIGNED NOT NULL COMMENT '班级ID',
    student_id INT UNSIGNED NOT NULL COMMENT '学生ID',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    UNIQUE KEY uk_class_student (class_id, student_id),
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学生关联表';

-- ===========================================
-- 初始化默认管理员账号（密码: 123456，BCrypt加密）
-- ===========================================
INSERT INTO users (username, password, email, nickname, role, status) VALUES
('admin', '$2b$12$oBSnNVS3/7q88ZWqtUUUE.CYBEkU3p7H7WHPUrLE0s6EC8BhS0Cv6', 'admin@example.com', '系统管理员', 'admin', 1)
ON DUPLICATE KEY UPDATE id=id;