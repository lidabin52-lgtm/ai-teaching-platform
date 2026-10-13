"""
应用配置模块
从环境变量读取所有配置项，支持Docker部署和本地开发
"""
import os


class Config:
    """基础配置类"""

    # ========== Flask基础配置 ==========
    SECRET_KEY = os.getenv('SECRET_KEY', 'ai-teaching-platform-secret-key-2024')

    # ========== 数据库配置（MySQL） ==========
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'frontend_edu')

    # SQLAlchemy数据库连接URI（如需使用SQLAlchemy可取消注释）
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # PyMySQL连接配置
    DB_CONFIG = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
        'database': MYSQL_DATABASE,
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor',  # 返回字典格式结果
    }

    # ========== DeepSeek API配置 ==========
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')  # 密钥只从 .env 读取，切勿硬编码
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    # 请求超时时间（秒）
    DEEPSEEK_TIMEOUT = int(os.getenv('DEEPSEEK_TIMEOUT', '60'))

    # ========== JWT配置 ==========
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-for-teaching-platform')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))

    # ========== CORS配置 ==========
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')

    # ========== 上传配置 ==========
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传16MB

    # ========== 运行环境 ==========
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    ENV = os.getenv('FLASK_ENV', 'production')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    ENV = 'production'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True


# 配置映射字典
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


def get_config():
    """
    根据环境变量获取对应的配置类
    默认使用生产环境配置
    """
    env = os.getenv('FLASK_ENV', 'production')
    return config_map.get(env, ProductionConfig)
