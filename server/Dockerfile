# ==========================================
# 后端服务 Dockerfile
# 基于 Python 3.11-slim，使用 Gunicorn 启动 Flask 应用
# ==========================================

# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    FLASK_APP=app.py \
    FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户运行应用（安全最佳实践）
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# 暴露端口
EXPOSE 5000

# 使用 Gunicorn 启动应用
# workers = (2 * CPU核心数) + 1，这里设置为4个worker
# timeout 设置为 300 秒以支持长轮询和 AI 请求
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "--enable-stdio-inheritance", "wsgi:app"]
