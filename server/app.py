"""
Flask应用入口文件
创建并配置Flask应用，注册所有Blueprint

启动方式:
    python app.py

环境变量:
    FLASK_ENV: 运行环境（development/production）
    MYSQL_HOST: 数据库主机
    MYSQL_PORT: 数据库端口
    MYSQL_USER: 数据库用户名
    MYSQL_PASSWORD: 数据库密码
    MYSQL_DATABASE: 数据库名
    DEEPSEEK_API_KEY: DeepSeek API密钥
    JWT_SECRET: JWT密钥
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def create_app():
    """
    应用工厂函数
    创建并配置Flask应用
    """
    app = Flask(__name__)
    
    # ========== 加载配置 ==========
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai-teaching-platform-secret-key-2024')
    
    # 数据库配置
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', '3306'))
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '123456')
    app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE', 'frontend_edu')
    
    # DeepSeek API配置
    app.config['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY', '')
    app.config['DEEPSEEK_API_BASE'] = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    app.config['DEEPSEEK_MODEL'] = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    
    # JWT配置
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'jwt-secret-key-for-teaching-platform')
    
    # 运行环境
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    
    # ========== 配置CORS ==========
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    CORS(app, resources={
        r'/api/*': {
            'origins': cors_origins,
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization'],
            'supports_credentials': True
        }
    })
    
    # ========== 注册Blueprint ==========
    # 用户模块
    from app.routes.user import user_bp
    app.register_blueprint(user_bp)
    
    # 闯关模块
    from app.routes.challenge import challenge_bp
    app.register_blueprint(challenge_bp)
    
    # AI导师模块
    from app.routes.mentor import mentor_bp
    app.register_blueprint(mentor_bp)
    
    # 学情分析模块
    from app.routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)
    
    # ========== 全局错误处理 ==========
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'code': 400,
            'message': '请求参数错误',
            'data': str(error) if app.debug else None
        }), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            'code': 401,
            'message': '未授权，请先登录',
            'data': None
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            'code': 403,
            'message': '权限不足',
            'data': None
        }), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'code': 404,
            'message': '请求的资源不存在',
            'data': None
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'code': 500,
            'message': '服务器内部错误',
            'data': str(error) if app.debug else None
        }), 500
    
    # ========== 健康检查接口 ==========
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查接口"""
        return jsonify({
            'code': 200,
            'message': '服务运行正常',
            'data': {
                'status': 'healthy',
                'version': '1.0.0'
            }
        })
    
    # ========== 根路径 ==========
    @app.route('/', methods=['GET'])
    def index():
        """根路径"""
        return jsonify({
            'code': 200,
            'message': 'AI前端智能教学与实战训练平台 API',
            'data': {
                'version': '1.0.0',
                'docs': '/api/health'
            }
        })
    
    return app


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    # 启动开发服务器
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║   AI前端智能教学与实战训练平台 API 服务                    ║
    ╠══════════════════════════════════════════════════════════╣
    ║   地址: http://localhost:{port}                            ║
    ║   环境: {'开发模式' if debug else '生产模式'}                            ║
    ║   健康检查: http://localhost:{port}/api/health              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
