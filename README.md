# 🎓 基于大模型的Web前端智能教学与实战训练平台

<p align="center">  
  <img src="https://img.shields.io/badge/Vue-3.4+-42b883?style=flat-square\&logo=vue.js" alt="Vue 3">  
  <img src="https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square\&logo=python" alt="Python 3.11">  
  <img src="https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square\&logo=flask" alt="Flask">  
  <img src="https://img.shields.io/badge/MySQL-8.0-4479a1?style=flat-square\&logo=mysql" alt="MySQL">  
  <img src="https://img.shields.io/badge/DeepSeek-AI-1e3a8a?style=flat-square" alt="DeepSeek AI">  
  <img src="https://img.shields.io/badge/Docker-Compose-2496ed?style=flat-square\&logo=docker" alt="Docker">  
</p>

<p align="center">  
  <b>AI驱动的智能前端教学平台，让学习编程更有趣、更高效！</b>  
</p>

---

## 📖 项目简介

本项目是一个基于大语言模型的Web前端智能教学与实战训练平台，旨在为前端初学者提供**游戏化、个性化、智能化**的学习体验。平台融合了AI技术，实现智能代码审判、个性化AI导师辅导、学情数据分析等功能。

### ✨ 核心特性

- 🎮 **游戏化闯关学习** - 青铜→白银→黄金→钻石→王者，段位晋升激发学习动力
- 🤖 **AI智能审判** - DeepSeek大模型实时评判代码，多维度评分反馈
- 👨‍🏫 **AI导师系统** - 24小时在线答疑，基于知识库的精准辅导
- 📊 **学情分析** - 教师端可视化数据看板，精准掌握学生学习情况
- 💻 **在线代码编辑** - 集成Monaco Editor，支持代码高亮、Emmet、实时预览
- 📱 **响应式设计** - 完美适配1920×1080和1366×768等多种分辨率

---

## 🛠️ 技术栈

### 前端技术栈

| 技术            | 版本    | 用途              |
| ------------- | ----- | --------------- |
| Vue.js        | 3.4+  | 渐进式JavaScript框架 |
| Vite          | 5.0+  | 下一代前端构建工具       |
| Element Plus  | 2.5+  | Vue 3组件库        |
| Monaco Editor | 0.45+ | VS Code同款代码编辑器  |
| Pinia         | 2.1+  | 状态管理            |
| Vue Router    | 4.2+  | 路由管理            |
| ECharts       | 5.4+  | 数据可视化图表         |
| Axios         | 1.6+  | HTTP客户端         |
| Marked        | 11.0+ | Markdown渲染      |

### 后端技术栈

| 技术                 | 版本    | 用途             |
| ------------------ | ----- | -------------- |
| Python             | 3.11+ | 编程语言           |
| Flask              | 3.0+  | Web框架          |
| Flask-SQLAlchemy   | 3.1+  | ORM数据库操作       |
| Flask-JWT-Extended | 4.5+  | JWT认证          |
| PyMySQL            | 1.1+  | MySQL连接驱动      |
| Gunicorn           | 21.0+ | WSGI HTTP服务器   |
| OpenAI             | 1.0+  | DeepSeek API调用 |

### 基础设施

| 技术             | 用途          |
| -------------- | ----------- |
| MySQL 8.0      | 关系型数据库      |
| Nginx          | 静态资源服务、反向代理 |
| Docker         | 容器化部署       |
| Docker Compose | 多容器编排       |

---

## 🚀 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- DeepSeek API Key（从 [DeepSeek平台](https://platform.deepseek.com/) 获取）

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd frontend-edu-platform
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
vim .env
```

### 3. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行数据初始化脚本
python seed_data.py

# 退出容器
exit
```

### 5. 访问应用

- 🌐 **前端页面**: <http://localhost>
- 🔧 **后端API**: <http://localhost:5000>
- 🗄️ **MySQL**: localhost:3306

### 6. 登录账号

| 角色 | 账号       | 密码     |
| -- | -------- | ------ |
| 教师 | admin    | 123456 |
| 学生 | student1 | 123456 |
| 学生 | student2 | 123456 |
| 学生 | student3 | 123456 |
| 学生 | student4 | 123456 |
| 学生 | student5 | 123456 |

---

## 📁 项目结构

```
frontend-edu-platform/
├── 📁 client/                    # 前端项目
│   ├── 📁 public/               # 静态资源
│   ├── 📁 src/
│   │   ├── 📁 api/              # API接口封装
│   │   ├── 📁 assets/           # 样式、图片资源
│   │   ├── 📁 components/       # 公共组件
│   │   │   ├── AIMentorDrawer.vue      # AI导师侧边栏
│   │   │   ├── JudgeResultModal.vue    # 审判结果弹窗
│   │   │   └── SkillTree.vue           # 技能树组件
│   │   ├── 📁 router/           # 路由配置
│   │   ├── 📁 store/            # Pinia状态管理
│   │   ├── 📁 views/            # 页面视图
│   │   │   ├── 📁 challenge/    # 闯关模块
│   │   │   │   └── ChallengePage.vue   # 闯关主页面
│   │   │   └── 📁 teacher/      # 教师模块
│   │   │       ├── TeacherDashboard.vue # 教师仪表盘
│   │   │       └── StudentDetail.vue    # 学生详情
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 入口文件
│   ├── Dockerfile               # 前端Docker配置
│   ├── nginx.conf               # Nginx配置文件
│   ├── package.json             # 依赖配置
│   └── vite.config.js           # Vite配置
│
├── 📁 server/                    # 后端项目
│   ├── 📁 app/
│   │   ├── 📁 models/           # 数据模型
│   │   │   └── models.py        # SQLAlchemy模型定义
│   │   ├── 📁 routes/           # API路由
│   │   │   ├── user.py          # 用户模块
│   │   │   ├── challenge.py     # 闯关模块
│   │   │   ├── mentor.py        # AI导师模块
│   │   │   └── analytics.py     # 学情分析模块
│   │   ├── 📁 services/         # 业务逻辑层
│   │   │   └── ai_service.py    # AI服务（DeepSeek集成）
│   │   ├── 📁 utils/            # 工具函数
│   │   │   ├── decorators.py    # 装饰器（认证、角色校验）
│   │   │   └── response.py      # 统一响应格式
│   │   └── __init__.py          # 应用工厂
│   ├── 📁 logs/                 # 日志目录
│   ├── app.py                   # 应用入口
│   ├── config.py                # 配置文件
│   ├── requirements.txt         # Python依赖
│   ├── seed_data.py             # 数据初始化脚本
│   └── Dockerfile               # 后端Docker配置
│
├── docker-compose.yml           # Docker编排配置
├── .env.example                 # 环境变量示例
└── README.md                    # 项目说明
```

---

## ⚙️ 环境变量说明

### 必需配置

| 变量名                | 说明                    | 示例                |
| ------------------ | --------------------- | ----------------- |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥        | `sk-xxxxxxxxxx`   |
| `JWT_SECRET_KEY`   | JWT签名密钥（生产环境请使用随机强密钥） | `your-secret-key` |

### 数据库配置

| 变量名                   | 说明           | 默认值            |
| --------------------- | ------------ | -------------- |
| `MYSQL_ROOT_PASSWORD` | MySQL root密码 | `root123456`   |
| `MYSQL_DATABASE`      | 数据库名称        | `frontend_edu` |
| `MYSQL_USER`          | 数据库用户名       | `edu_user`     |
| `MYSQL_PASSWORD`      | 数据库密码        | `edu_pass123`  |

### AI服务配置

| 变量名                 | 说明             | 默认值                           |
| ------------------- | -------------- | ----------------------------- |
| `DEEPSEEK_BASE_URL` | DeepSeek API地址 | `https://api.deepseek.com/v1` |
| `DEEPSEEK_MODEL`    | 使用模型           | `deepseek-chat`               |

### 其他配置

| 变量名                | 说明            | 默认值    |
| ------------------ | ------------- | ------ |
| `JWT_EXPIRE_HOURS` | Token过期时间（小时） | `24`   |
| `LOG_LEVEL`        | 日志级别          | `INFO` |

---

## 🎯 功能列表

### 学生端功能

- ✅ 用户登录/注册（JWT认证）
- ✅ 技能树可视化展示
- ✅ 代码闯关挑战（15个关卡）
- ✅ 在线代码编辑（Monaco Editor）
- ✅ 实时代码预览
- ✅ AI智能代码审判
- ✅ 星级评分系统
- ✅ AI导师实时问答
- ✅ 学习进度追踪
- ✅ 个人成绩统计

### 教师端功能

- ✅ 班级学情总览
- ✅ 学生成绩分布图
- ✅ 关卡通过率热力图
- ✅ 常见错误词云
- ✅ 学生个人详情
- ✅ 能力雷达图
- ✅ 学习轨迹分析

### AI功能

- ✅ 代码智能评判（正确性/规范性/最佳实践）
- ✅ 多维度评分反馈
- ✅ 个性化学习建议
- ✅ RAG增强的AI导师问答
- ✅ 知识库检索
- ✅ 对话历史管理

---

## 📸 截图展示

### 学生端

#### 技能树页面

> 可视化展示所有关卡，不同段位使用不同颜色标识

```
[青铜] [白银] [黄金] [钻石] [王者]
  🌳     🌳     🌳     🌳     👑
```

#### 闯关页面

> 左侧需求描述 | 中间代码编辑器 | 右侧实时预览

```
┌─────────────────────────────────────────────────────────┐
│  关卡：HTML基础结构  |  青铜段位  |  ⭐⭐⭐              │
├──────────────┬─────────────────────┬────────────────────┤
│              │                     │                    │
│  📋 需求描述  │   💻 代码编辑器     │   👁️ 实时预览      │
│              │                     │                    │
│  Markdown    │   Monaco Editor     │   iframe渲染       │
│  渲染        │   语法高亮          │   代码效果         │
│              │   Emmet支持         │                    │
│              │                     │                    │
├──────────────┴─────────────────────┴────────────────────┤
│  [🚀 提交审判]  [👨‍🏫 呼叫导师]  [🔄 重置代码]           │
└─────────────────────────────────────────────────────────┘
```

#### AI导师侧边栏

> 实时对话，支持Markdown格式回复

```
┌─────────────────┐
│   🤖 AI导师      │
├─────────────────┤
│ 你好！有什么可   │
│ 以帮你的吗？     │
│                 │
│ [输入问题...]   │
└─────────────────┘
```

### 教师端

#### 学情仪表盘

> 数据可视化，多维度展示班级学习情况

```
┌─────────────────────────────────────────────┐
│  📊 学情分析仪表盘                           │
├─────────────────┬───────────────────────────┤
│  总学生: 50     │   [成绩分布饼图]          │
│  活跃: 45       │                           │
│  平均进度: 60%  │                           │
├─────────────────┴───────────────────────────┤
│  [关卡通过率热力图]                          │
├─────────────────────────────────────────────┤
│  [常见错误词云]                              │
└─────────────────────────────────────────────┘
```

#### 学生详情

> 个人能力雷达图、学习轨迹追踪

```
┌─────────────────────────────────────────────┐
│  学生：张三                                  │
├─────────────────┬───────────────────────────┤
│  [能力雷达图]   │   最近提交记录             │
│                 │   - HTML基础: ⭐⭐⭐       │
│                 │   - CSS选择器: ⭐⭐        │
│                 │   - Flex布局: ⭐⭐⭐       │
├─────────────────┴───────────────────────────┤
│  [学习进度曲线]                              │
└─────────────────────────────────────────────┘
```

---

## 🔧 开发指南

### 前端开发

```bash
cd client

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 后端开发

```bash
cd server

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py
```

### 数据库迁移

```bash
# 进入后端容器
docker-compose exec backend bash

# 使用Flask命令管理数据库
flask db init      # 初始化迁移
flask db migrate   # 创建迁移
flask db upgrade   # 应用迁移
```

---

## 🐛 常见问题

### Q: 前端页面显示空白？

A: 检查Nginx配置是否正确，确保Vue Router的history模式已配置try_files。

### Q: AI功能无法使用？

A: 确认`DEEPSEEK_API_KEY`已正确配置，且API Key有效。

### Q: 数据库连接失败？

A: 检查MySQL服务是否启动，以及数据库连接配置是否正确。

### Q: 代码预览不生效？

A: 检查iframe的sandbox属性配置，确保允许脚本执行。

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证开源。

---

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Element Plus](https://element-plus.org/) - Vue 3组件库
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - 代码编辑器
- [DeepSeek](https://deepseek.com/) - 大语言模型服务
- [Flask](https://flask.palletsprojects.com/) - Python Web框架

---

<p align="center">  
  Made with ❤️ by 前端智能教学平台团队  
</p>
