# ===========================================
# 前端Dockerfile
# 基于大模型的Web前端智能教学与实战训练平台
# ===========================================

# ========== 构建阶段 ==========
FROM node:20-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制依赖文件（利用Docker缓存层）
COPY package*.json ./

# 安装依赖
RUN npm install --production=false

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# ========== 运行阶段 ==========
FROM nginx:alpine

# 安装必要的工具
RUN apk add --no-cache tzdata

# 设置时区
ENV TZ=Asia/Shanghai

# 复制构建产物到Nginx目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 创建健康检查脚本
RUN echo '#!/bin/sh' > /healthcheck.sh && \
    echo 'curl -f http://localhost:80/ || exit 1' >> /healthcheck.sh && \
    chmod +x /healthcheck.sh

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /healthcheck.sh

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
