"""
Flask-SQLAlchemy 数据模型定义
对应数据库schema.sql中的所有表结构
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

# 创建SQLAlchemy实例（在应用工厂中初始化）
db = SQLAlchemy()


# ========== 枚举类型定义 ==========

class UserRole(Enum):
    """用户角色枚举"""
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class ChallengeDifficulty(Enum):
    """关卡段位枚举"""
    BRONZE = 'bronze'      # 青铜
    SILVER = 'silver'      # 白银
    GOLD = 'gold'          # 黄金
    DIAMOND = 'diamond'    # 钻石
    KING = 'king'          # 王者


class SubmissionStatus(Enum):
    """提交状态枚举"""
    PENDING = 'pending'      # 待审判
    JUDGING = 'judging'      # 审判中
    COMPLETED = 'completed'  # 已完成
    FAILED = 'failed'        # 失败


class MessageRole(Enum):
    """消息角色枚举"""
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'


class ContentType(Enum):
    """内容类型枚举"""
    TEXT = 'text'
    CODE = 'code'
    IMAGE = 'image'


class KnowledgeDifficulty(Enum):
    """知识库难度枚举"""
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'


# ========== 数据模型类 ==========

class User(db.Model):
    """
    用户表
    存储学生和教师信息
    """
    __tablename__ = 'users'
    __table_args__ = {
        'comment': '用户表，存储学生和教师信息',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码，BCrypt加密')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='邮箱')
    nickname = db.Column(db.String(50), default='', comment='昵称')
    avatar = db.Column(db.String(500), default='', comment='头像URL')
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, comment='角色')
    status = db.Column(db.SmallInteger, default=1, comment='状态：1正常/0禁用')
    last_login_at = db.Column(db.DateTime, nullable=True, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关系定义
    created_challenges = db.relationship('Challenge', backref='creator', lazy='dynamic')
    submissions = db.relationship('Submission', backref='student', lazy='dynamic')
    conversations = db.relationship('AIConversation', backref='student', lazy='dynamic')
    progress = db.relationship('StudentProgress', backref='student', uselist=False)
    taught_classes = db.relationship('Class', backref='teacher', lazy='dynamic')
    knowledge_docs = db.relationship('KnowledgeBase', backref='creator', lazy='dynamic')

    def to_dict(self):
        """转换为字典（敏感字段排除）"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'role': self.role.value,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Challenge(db.Model):
    """
    关卡表
    技能闯关系统的核心关卡数据
    """
    __tablename__ = 'challenges'
    __table_args__ = (
        db.Index('idx_difficulty_order', 'difficulty', 'order_num'),
        db.Index('idx_category', 'category'),
        {
            'comment': '关卡表，存储技能闯关的所有关卡',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关卡ID')
    title = db.Column(db.String(200), nullable=False, comment='关卡标题')
    description = db.Column(db.Text, nullable=False, comment='需求描述（Markdown）')
    difficulty = db.Column(db.Enum(ChallengeDifficulty), nullable=False, 
                          default=ChallengeDifficulty.BRONZE, comment='段位')
    order_num = db.Column(db.Integer, default=0, comment='同段位排序号')
    category = db.Column(db.String(50), nullable=False, comment='分类')
    tags = db.Column(db.JSON, comment='标签数组')

    # 代码相关
    starter_code = db.Column(db.Text, comment='初始代码模板')
    language = db.Column(db.String(20), default='html', comment='编程语言')

    # AI审判标准
    scoring_criteria = db.Column(db.JSON, nullable=False, 
                                 comment='评分标准JSON：{"correctness":30,...}')
    ai_prompt = db.Column(db.Text, comment='AI审判系统提示词')
    expected_output = db.Column(db.Text, comment='期望输出描述')

    # 关卡配置
    time_limit = db.Column(db.Integer, default=0, comment='时间限制（分钟）')
    hint_count = db.Column(db.Integer, default=3, comment='可用提示次数')
    unlock_requirement = db.Column(db.JSON, 
                                   comment='解锁条件JSON：{"prev_challenge_id":1,...}')

    status = db.Column(db.SmallInteger, default=1, comment='状态：1上架/0下架')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建者ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          comment='更新时间')

    # 关系
    submissions = db.relationship('Submission', backref='challenge', lazy='dynamic')
    conversations = db.relationship('AIConversation', backref='challenge', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty.value,
            'difficulty_label': self.get_difficulty_label(),
            'order_num': self.order_num,
            'category': self.category,
            'tags': self.tags or [],
            'starter_code': self.starter_code,
            'language': self.language,
            'scoring_criteria': self.scoring_criteria,
            'time_limit': self.time_limit,
            'hint_count': self.hint_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def get_difficulty_label(self):
        """获取段位中文标签"""
        labels = {
            'bronze': '青铜',
            'silver': '白银',
            'gold': '黄金',
            'diamond': '钻石',
            'king': '王者'
        }
        return labels.get(self.difficulty.value, '未知')


class Submission(db.Model):
    """
    学生提交记录表
    存储学生闯关提交的代码和AI审判结果
    """
    __tablename__ = 'submissions'
    __table_args__ = (
        db.Index('idx_user_challenge', 'user_id', 'challenge_id'),
        db.Index('idx_challenge_status', 'challenge_id', 'status'),
        {
            'comment': '提交记录表，存储学生代码和AI审判结果',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='提交ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False, 
                             comment='关卡ID')

    # 提交内容
    code = db.Column(db.Text, nullable=False, comment='提交的代码')
    code_hash = db.Column(db.String(64), comment='代码哈希（查重用）')

    # AI审判结果
    ai_feedback = db.Column(db.Text, comment='AI评语（详细）')
    ai_summary = db.Column(db.String(500), comment='AI评语摘要')
    total_score = db.Column(db.Integer, comment='总分（0-100）')
    stars = db.Column(db.SmallInteger, comment='获得星数（0-3）')

    # 四维度评分
    score_correctness = db.Column(db.SmallInteger, comment='正确性得分')
    score_code_quality = db.Column(db.SmallInteger, comment='代码质量得分')
    score_best_practice = db.Column(db.SmallInteger, comment='最佳实践得分')
    score_creativity = db.Column(db.SmallInteger, comment='创新性得分')

    # 评分详情
    scoring_details = db.Column(db.JSON, comment='评分详情JSON')

    # 提交状态
    status = db.Column(db.Enum(SubmissionStatus), default=SubmissionStatus.PENDING, 
                       comment='状态')
    attempt_number = db.Column(db.Integer, default=1, comment='第几次尝试')
    time_spent = db.Column(db.Integer, comment='耗时（秒）')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='提交时间')
    judged_at = db.Column(db.DateTime, comment='AI审判完成时间')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'code': self.code,
            'ai_feedback': self.ai_feedback,
            'ai_summary': self.ai_summary,
            'total_score': self.total_score,
            'stars': self.stars,
            'scores': {
                'correctness': self.score_correctness,
                'code_quality': self.score_code_quality,
                'best_practice': self.score_best_practice,
                'creativity': self.score_creativity,
            },
            'scoring_details': self.scoring_details,
            'status': self.status.value,
            'attempt_number': self.attempt_number,
            'time_spent': self.time_spent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'judged_at': self.judged_at.isoformat() if self.judged_at else None,
        }


class AIConversation(db.Model):
    """
    AI对话记录表
    学生与AI导师的对话历史
    """
    __tablename__ = 'ai_conversations'
    __table_args__ = (
        db.Index('idx_user', 'user_id'),
        db.Index('idx_updated_at', 'updated_at'),
        {
            'comment': 'AI对话表，存储学生与AI导师的对话会话',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='对话ID')
    conversation_no = db.Column(db.String(64), unique=True, nullable=False, 
                                comment='对话编号')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, 
                        comment='学生ID')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), 
                             comment='关联关卡ID')

    title = db.Column(db.String(200), default='', comment='对话标题')
    message_count = db.Column(db.Integer, default=0, comment='消息数量')
    knowledge_refs = db.Column(db.JSON, comment='引用的知识库文档ID列表')

    status = db.Column(db.SmallInteger, default=1, comment='状态：1正常/0已归档')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          comment='更新时间')

    # 关系
    messages = db.relationship('AIMessage', backref='conversation', lazy='dynamic',
                               order_by='AIMessage.created_at')

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_no': self.conversation_no,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'title': self.title,
            'message_count': self.message_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class AIMessage(db.Model):
    """
    AI消息记录表
    对话中的具体消息内容
    """
    __tablename__ = 'ai_messages'
    __table_args__ = (
        db.Index('idx_conversation', 'conversation_id'),
        {
            'comment': 'AI消息表，存储对话中的具体消息',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='消息ID')
    conversation_id = db.Column(db.Integer, db.ForeignKey('ai_conversations.id'), 
                                nullable=False, comment='所属对话ID')
    role = db.Column(db.Enum(MessageRole), nullable=False, comment='角色')
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    content_type = db.Column(db.Enum(ContentType), default=ContentType.TEXT, 
                             comment='内容类型')

    # 代码相关
    code_language = db.Column(db.String(20), comment='代码语言')
    referenced_code = db.Column(db.Text, comment='引用的学生代码片段')

    # 元数据
    tokens_used = db.Column(db.Integer, comment='消耗的token数')
    response_time_ms = db.Column(db.Integer, comment='响应耗时（毫秒）')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='发送时间')

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role.value,
            'content': self.content,
            'content_type': self.content_type.value,
            'code_language': self.code_language,
            'referenced_code': self.referenced_code,
            'tokens_used': self.tokens_used,
            'response_time_ms': self.response_time_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class KnowledgeBase(db.Model):
    """
    知识库表
    AI导师的知识库文档
    """
    __tablename__ = 'knowledge_base'
    __table_args__ = (
        db.Index('idx_category', 'category'),
        db.Index('idx_difficulty', 'difficulty'),
        {
            'comment': '知识库表，存储AI导师的知识文档',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='文档ID')
    title = db.Column(db.String(200), nullable=False, comment='文档标题')
    content = db.Column(db.Text, nullable=False, comment='文档内容（Markdown）')
    summary = db.Column(db.String(500), comment='内容摘要')

    # 分类标签
    category = db.Column(db.String(50), nullable=False, comment='分类')
    tags = db.Column(db.JSON, comment='标签数组')
    difficulty = db.Column(db.Enum(KnowledgeDifficulty), default=KnowledgeDifficulty.BEGINNER, 
                          comment='难度')

    # 向量检索（预留）
    embedding_vector = db.Column(db.LargeBinary, comment='文本嵌入向量')

    # 关联关卡
    related_challenges = db.Column(db.JSON, comment='关联的关卡ID列表')

    # 使用统计
    view_count = db.Column(db.Integer, default=0, comment='查看次数')
    reference_count = db.Column(db.Integer, default=0, comment='被AI引用次数')

    status = db.Column(db.SmallInteger, default=1, comment='状态：1正常/0下架')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建者ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'category': self.category,
            'tags': self.tags or [],
            'difficulty': self.difficulty.value,
            'view_count': self.view_count,
            'reference_count': self.reference_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class StudentProgress(db.Model):
    """
    学生进度表
    学情分析：记录学生的整体学习进度
    """
    __tablename__ = 'student_progress'
    __table_args__ = (
        db.UniqueConstraint('user_id', name='uk_user'),
        {
            'comment': '学生进度表，用于学情分析统计',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='进度ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, 
                        comment='学生ID')

    # 各段位进度统计
    bronze_completed = db.Column(db.Integer, default=0, comment='青铜已完成')
    bronze_total = db.Column(db.Integer, default=0, comment='青铜总关卡')
    silver_completed = db.Column(db.Integer, default=0, comment='白银已完成')
    silver_total = db.Column(db.Integer, default=0, comment='白银总关卡')
    gold_completed = db.Column(db.Integer, default=0, comment='黄金已完成')
    gold_total = db.Column(db.Integer, default=0, comment='黄金总关卡')
    diamond_completed = db.Column(db.Integer, default=0, comment='钻石已完成')
    diamond_total = db.Column(db.Integer, default=0, comment='钻石总关卡')
    king_completed = db.Column(db.Integer, default=0, comment='王者已完成')
    king_total = db.Column(db.Integer, default=0, comment='王者总关卡')

    # 综合统计
    total_submissions = db.Column(db.Integer, default=0, comment='总提交次数')
    total_stars = db.Column(db.Integer, default=0, comment='总获得星数')
    avg_score = db.Column(db.Numeric(5, 2), default=0, comment='平均分')
    current_streak = db.Column(db.Integer, default=0, comment='连续打卡天数')
    longest_streak = db.Column(db.Integer, default=0, comment='最长连续打卡天数')

    last_submission_at = db.Column(db.DateTime, comment='最后提交时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          comment='更新时间')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'progress': {
                'bronze': {'completed': self.bronze_completed, 'total': self.bronze_total},
                'silver': {'completed': self.silver_completed, 'total': self.silver_total},
                'gold': {'completed': self.gold_completed, 'total': self.gold_total},
                'diamond': {'completed': self.diamond_completed, 'total': self.diamond_total},
                'king': {'completed': self.king_completed, 'total': self.king_total},
            },
            'total_submissions': self.total_submissions,
            'total_stars': self.total_stars,
            'avg_score': float(self.avg_score) if self.avg_score else 0,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_submission_at': self.last_submission_at.isoformat() if self.last_submission_at else None,
        }


class Class(db.Model):
    """
    班级表
    教师管理班级
    """
    __tablename__ = 'classes'
    __table_args__ = (
        db.Index('idx_teacher', 'teacher_id'),
        {
            'comment': '班级表',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='班级ID')
    name = db.Column(db.String(100), nullable=False, comment='班级名称')
    description = db.Column(db.String(500), comment='班级描述')
    invite_code = db.Column(db.String(20), unique=True, comment='邀请码')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, 
                          comment='班主任ID')

    status = db.Column(db.SmallInteger, default=1, comment='状态：1正常/0解散')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
                          comment='更新时间')

    # 关系
    students = db.relationship('User', secondary='class_students', 
                               backref=db.backref('joined_classes', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'invite_code': self.invite_code,
            'teacher_id': self.teacher_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ClassStudent(db.Model):
    """
    班级学生关联表
    多对多关系
    """
    __tablename__ = 'class_students'
    __table_args__ = (
        db.UniqueConstraint('class_id', 'student_id', name='uk_class_student'),
        {
            'comment': '班级学生关联表',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
        }
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关联ID')
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False, 
                        comment='班级ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, 
                          comment='学生ID')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, comment='加入时间')
