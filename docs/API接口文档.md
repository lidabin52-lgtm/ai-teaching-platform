# API 接口文档

> 基础URL: `http://<host>:<port>/api`
>
> 所有接口均返回 JSON 格式数据，`Content-Type: application/json`

---

## 目录

- [1. 认证说明](#1-认证说明)
- [2. 统一响应格式](#2-统一响应格式)
- [3. 用户模块](#3-用户模块)
  - [3.1 用户登录](#31-用户登录)
  - [3.2 用户注册](#32-用户注册)
  - [3.3 获取当前用户信息](#33-获取当前用户信息)
  - [3.4 获取用户闯关进度](#34-获取用户闯关进度)
  - [3.5 获取用户提交记录](#35-获取用户提交记录)
- [4. 闯关模块](#4-闯关模块)
  - [4.1 获取关卡列表](#41-获取关卡列表)
  - [4.2 获取关卡详情](#42-获取关卡详情)
  - [4.3 提交代码](#43-提交代码)
  - [4.4 获取关卡历史提交](#44-获取关卡历史提交)
- [5. AI导师模块](#5-ai导师模块)
  - [5.1 发送消息](#51-发送消息)
  - [5.2 获取对话历史](#52-获取对话历史)
  - [5.3 删除对话](#53-删除对话)
- [6. 学情分析模块](#6-学情分析模块)
  - [6.1 班级整体数据概览](#61-班级整体数据概览)
  - [6.2 知识掌握热力图](#62-知识掌握热力图)
  - [6.3 个体能力分析](#63-个体能力分析)
  - [6.4 高频错误分析](#64-高频错误分析)

---

## 1. 认证说明

系统采用 **JWT (JSON Web Token)** 进行身份认证。

### 认证流程

1. 调用 `/api/user/login` 接口获取 `token`
2. 后续请求在 HTTP Header 中携带 token：

```
Authorization: Bearer <token>
```

### Token 说明

- Token 中包含 `user_id`、`username`、`role` 信息
- 需要认证的接口使用 `@login_required` 装饰器，未携带或 Token 无效将返回 `401`
- 学情分析模块接口额外需要 **教师角色** 权限（`@teacher_required`），非教师角色将返回 `403`

### 角色说明

| 角色 | 说明 |
|------|------|
| `student` | 学生，可进行闯关、提交代码、与AI导师对话 |
| `teacher` | 教师，拥有学生所有权限，额外可查看学情分析数据 |

---

## 2. 统一响应格式

所有接口返回统一的 JSON 结构：

### 成功响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

### 错误响应

```json
{
  "code": 400,
  "message": "错误描述信息",
  "data": null
}
```

### 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

### HTTP 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 / Token 无效 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 3. 用户模块

> 路由前缀: `/api/user`

### 3.1 用户登录

用户通过用户名和密码登录系统，获取 JWT Token。

**请求**

- **URL**: `POST /api/user/login`
- **Content-Type**: `application/json`
- **是否需要认证**: 否

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `username` | string | 是 | 用户名，最大长度50字符 |
| `password` | string | 是 | 密码 |

**请求示例**

```json
{
  "username": "zhangsan",
  "password": "123456"
}
```

**成功响应**

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "nickname": "张三",
      "avatar": "/uploads/avatar/1.png",
      "role": "student"
    }
  }
}
```

**错误响应**

```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null
}
```

---

### 3.2 用户注册

注册新用户账号。

**请求**

- **URL**: `POST /api/user/register`
- **Content-Type**: `application/json`
- **是否需要认证**: 否

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `username` | string | 是 | 用户名，长度3-50字符 |
| `password` | string | 是 | 密码，最少6个字符 |
| `email` | string | 是 | 邮箱地址 |
| `nickname` | string | 否 | 昵称，不传则使用用户名 |

**请求示例**

```json
{
  "username": "zhangsan",
  "password": "123456",
  "email": "zhangsan@example.com",
  "nickname": "张三"
}
```

**成功响应**

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com"
  }
}
```

**错误响应**

```json
{
  "code": 400,
  "message": "用户名或邮箱已被注册",
  "data": null
}
```

---

### 3.3 获取当前用户信息

获取当前登录用户的详细信息，包括当前段位。

**请求**

- **URL**: `GET /api/user/info`
- **是否需要认证**: 是

**请求参数**

无

**成功响应**

```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "nickname": "张三",
    "avatar": "/uploads/avatar/1.png",
    "role": "student",
    "difficulty": "gold",
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `difficulty` | string | 当前段位，可选值: `bronze`/`silver`/`gold`/`diamond`/`king` |

---

### 3.4 获取用户闯关进度

获取当前用户在各段位的闯关进度统计数据。

**请求**

- **URL**: `GET /api/user/progress`
- **是否需要认证**: 是

**请求参数**

无

**成功响应**

```json
{
  "code": 200,
  "data": {
    "progress": {
      "bronze": { "completed": 8, "total": 10 },
      "silver": { "completed": 3, "total": 10 },
      "gold": { "completed": 0, "total": 10 },
      "diamond": { "completed": 0, "total": 5 },
      "king": { "completed": 0, "total": 5 }
    },
    "total_submissions": 25,
    "total_stars": 55,
    "avg_score": 78.5,
    "current_streak": 5,
    "longest_streak": 10,
    "last_submission_at": "2025-03-20T14:30:00"
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `progress` | object | 各段位完成进度，`completed` 为已完成数，`total` 为总数 |
| `total_submissions` | int | 总提交次数 |
| `total_stars` | int | 获得的总星数 |
| `avg_score` | float | 平均得分 |
| `current_streak` | int | 当前连续完成天数 |
| `longest_streak` | int | 最长连续完成天数 |
| `last_submission_at` | string/null | 最后提交时间 |

---

### 3.5 获取用户提交记录

分页获取当前用户的所有代码提交记录。

**请求**

- **URL**: `GET /api/user/submissions`
- **是否需要认证**: 是

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `page` | int | 否 | 1 | 页码 |
| `page_size` | int | 否 | 10 | 每页数量 |
| `challenge_id` | int | 否 | - | 关卡ID，传入则筛选特定关卡的提交 |

**请求示例**

```
GET /api/user/submissions?page=1&page_size=10&challenge_id=5
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 101,
        "challenge_id": 5,
        "challenge_title": "CSS布局：Flexbox",
        "difficulty": "silver",
        "category": "CSS",
        "total_score": 85,
        "stars": 3,
        "status": "completed",
        "ai_summary": "代码完成度很好！",
        "created_at": "2025-03-20T14:30:00"
      }
    ],
    "total": 25,
    "page": 1,
    "page_size": 10
  }
}
```

---

## 4. 闯关模块

> 路由前缀: `/api/challenge`

### 4.1 获取关卡列表

获取所有关卡列表，按段位分组，并标记每个关卡的状态（已完成/已解锁/未解锁）。

**请求**

- **URL**: `GET /api/challenge/list`
- **是否需要认证**: 是

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `difficulty` | string | 否 | - | 段位筛选，可选值: `bronze`/`silver`/`gold`/`diamond`/`king` |

**请求示例**

```
GET /api/challenge/list?difficulty=silver
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "bronze": [
      {
        "id": 1,
        "title": "HTML基础：创建第一个网页",
        "difficulty": "bronze",
        "category": "HTML",
        "tags": ["HTML", "基础"],
        "time_limit": 30,
        "order_num": 1,
        "status": "completed",
        "stars": 3,
        "best_score": 88
      },
      {
        "id": 2,
        "title": "HTML表单",
        "difficulty": "bronze",
        "category": "HTML",
        "tags": ["HTML", "表单"],
        "time_limit": 30,
        "order_num": 2,
        "status": "unlocked",
        "stars": 0
      }
    ],
    "silver": [],
    "gold": [],
    "diamond": [],
    "king": []
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | string | 关卡状态: `completed`(已完成) / `unlocked`(已解锁) / `locked`(未解锁) |
| `stars` | int | 获得的星级（0-3） |
| `best_score` | int | 最高得分（仅 `completed` 状态返回） |
| `locked_reason` | string | 未解锁原因（仅 `locked` 状态返回） |

---

### 4.2 获取关卡详情

获取指定关卡的详细信息，包括需求描述、初始代码、评分标准等。

**请求**

- **URL**: `GET /api/challenge/{challenge_id}`
- **是否需要认证**: 是

**路径参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `challenge_id` | int | 是 | 关卡ID |

**请求示例**

```
GET /api/challenge/1
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "id": 1,
    "title": "HTML基础：创建第一个网页",
    "description": "## 任务目标\n\n创建一个包含标题、段落和列表的基础HTML页面...",
    "difficulty": "bronze",
    "order_num": 1,
    "category": "HTML",
    "tags": ["HTML", "基础"],
    "starter_code": "<!DOCTYPE html>\n<html>\n<head>...</head>\n<body>...</body>\n</html>",
    "language": "html",
    "scoring_criteria": {
      "functionality": "页面包含标题、段落、列表",
      "code_quality": "代码缩进规范，标签正确嵌套",
      "creativity": "页面美观度"
    },
    "time_limit": 30,
    "hint_count": 3,
    "creator_name": "李老师",
    "created_at": "2025-01-10T08:00:00",
    "attempt_count": 3,
    "best_score": 88,
    "best_stars": 3,
    "is_completed": true
  }
}
```

**错误响应**

```json
{
  "code": 404,
  "message": "关卡不存在",
  "data": null
}
```

---

### 4.3 提交代码

提交代码到指定关卡，系统将调用AI审判服务进行评分。

**请求**

- **URL**: `POST /api/challenge/{challenge_id}/submit`
- **Content-Type**: `application/json`
- **是否需要认证**: 是

**路径参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `challenge_id` | int | 是 | 关卡ID |

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `code` | string | 是 | 学生提交的代码 |
| `time_spent` | int | 否 | 耗时（秒），默认0 |

**请求示例**

```json
{
  "code": "<!DOCTYPE html>\n<html>\n<head><title>我的网页</title></head>\n<body>\n  <h1>欢迎</h1>\n  <p>这是我的第一个网页</p>\n</body>\n</html>",
  "time_spent": 120
}
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "submission_id": 123,
    "function_score": 3,
    "standard_score": 2,
    "cool_score": 2,
    "total_stars": 3,
    "comment": "代码完成度很好！功能完整，结构清晰。继续保持！",
    "hint": ""
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `submission_id` | int | 提交记录ID |
| `function_score` | int | 功能性评分（1-3） |
| `standard_score` | int | 规范性评分（1-3） |
| `cool_score` | int | 创意性评分（1-3） |
| `total_stars` | int | 总星级（1-3） |
| `comment` | string | AI评语 |
| `hint` | string | 改进提示 |

**错误响应**

```json
{
  "code": 500,
  "message": "AI审判失败: 连接超时",
  "data": null
}
```

---

### 4.4 获取关卡历史提交

分页获取当前用户在指定关卡的所有历史提交记录。

**请求**

- **URL**: `GET /api/challenge/{challenge_id}/submissions`
- **是否需要认证**: 是

**路径参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `challenge_id` | int | 是 | 关卡ID |

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `page` | int | 否 | 1 | 页码 |
| `page_size` | int | 否 | 10 | 每页数量 |

**请求示例**

```
GET /api/challenge/1/submissions?page=1&page_size=5
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 123,
        "code": "<!DOCTYPE html>...",
        "ai_feedback": "代码完成度很好！功能完整...",
        "ai_summary": "代码完成度很好！",
        "total_score": 88,
        "stars": 3,
        "scores": {
          "correctness": 99,
          "code_quality": 66,
          "best_practice": 66,
          "creativity": 66
        },
        "status": "completed",
        "attempt_number": 3,
        "time_spent": 120,
        "created_at": "2025-03-20T14:30:00",
        "judged_at": "2025-03-20T14:30:15"
      }
    ],
    "total": 3,
    "page": 1,
    "page_size": 5
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | string | 提交状态: `judging`(审判中) / `completed`(已完成) / `failed`(失败) |
| `scores.correctness` | int | 功能正确性得分 |
| `scores.code_quality` | int | 代码质量得分 |
| `scores.best_practice` | int | 最佳实践得分 |
| `scores.creativity` | int | 创意性得分 |

---

## 5. AI导师模块

> 路由前缀: `/api/mentor`

### 5.1 发送消息

向AI导师发送消息，获取AI回复。支持普通响应和流式响应（SSE）两种模式。

**请求**

- **URL**: `POST /api/mentor/chat`
- **Content-Type**: `application/json`
- **是否需要认证**: 是

**请求参数**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `message` | string | 是 | - | 消息内容，最大长度2000字符 |
| `challenge_id` | int | 否 | - | 当前闯关ID，传入则关联到关卡上下文 |
| `stream` | bool | 否 | false | 是否使用流式响应 |

**请求示例**

```json
{
  "message": "请问CSS中Flex布局怎么实现垂直居中？",
  "challenge_id": 5,
  "stream": false
}
```

**成功响应（普通模式）**

```json
{
  "code": 200,
  "data": {
    "conversation_id": "CONV20250320143000A1B2C3D4",
    "message_id": 456,
    "content": "CSS Flex布局实现垂直居中有几种方式...\n\n最常用的是给父容器设置 `display: flex; align-items: center;`...",
    "referenced_knowledge": [1, 3]
  }
}
```

**成功响应（流式模式）**

当 `stream: true` 时，返回 `Content-Type: text/event-stream` 格式的 SSE 流：

```
data: {"content": "CSS"}

data: {"content": " Flex布局"}

data: {"content": "实现垂直居中..."}

data: [DONE]
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `conversation_id` | string | 对话编号，用于后续查询对话历史 |
| `message_id` | int | AI消息记录ID |
| `content` | string | AI回复内容 |
| `referenced_knowledge` | int[] | 引用的知识库文档ID列表 |

---

### 5.2 获取对话历史

获取用户的对话历史。支持两种模式：
- 不传 `conversation_id`：返回对话列表（分页）
- 传入 `conversation_id`：返回指定对话的消息详情

**请求**

- **URL**: `GET /api/mentor/history`
- **是否需要认证**: 是

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `conversation_id` | string | 否 | - | 对话编号，传入则返回该对话的消息列表 |
| `page` | int | 否 | 1 | 页码 |
| `page_size` | int | 否 | 20 | 每页数量 |

**请求示例（对话列表）**

```
GET /api/mentor/history?page=1&page_size=20
```

**成功响应（对话列表）**

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "CONV20250320143000A1B2C3D4",
        "title": "请问CSS中Flex布局...",
        "message_count": 8,
        "updated_at": "2025-03-20T14:35:00"
      }
    ],
    "total": 5,
    "page": 1,
    "page_size": 20
  }
}
```

**请求示例（对话详情）**

```
GET /api/mentor/history?conversation_id=CONV20250320143000A1B2C3D4
```

**成功响应（对话详情）**

```json
{
  "code": 200,
  "data": {
    "conversation": {
      "id": "CONV20250320143000A1B2C3D4",
      "title": "请问CSS中Flex布局...",
      "message_count": 8
    },
    "messages": [
      {
        "id": 100,
        "role": "user",
        "content": "请问CSS中Flex布局怎么实现垂直居中？",
        "content_type": "text",
        "created_at": "2025-03-20T14:30:00"
      },
      {
        "id": 101,
        "role": "assistant",
        "content": "CSS Flex布局实现垂直居中有几种方式...",
        "content_type": "text",
        "created_at": "2025-03-20T14:30:05"
      }
    ]
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `role` | string | 消息角色: `user`(用户) / `assistant`(AI导师) |
| `content_type` | string | 内容类型: `text` |

---

### 5.3 删除对话

删除（归档）指定对话。

**请求**

- **URL**: `DELETE /api/mentor/conversations/{conversation_no}`
- **是否需要认证**: 是

**路径参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `conversation_no` | string | 是 | 对话编号 |

**请求示例**

```
DELETE /api/mentor/conversations/CONV20250320143000A1B2C3D4
```

**成功响应**

```json
{
  "code": 200,
  "message": "对话已删除",
  "data": null
}
```

**错误响应**

```json
{
  "code": 404,
  "message": "对话不存在",
  "data": null
}
```

---

## 6. 学情分析模块

> 路由前缀: `/api/analytics`
>
> **注意**: 该模块所有接口均需要 **教师角色** 权限

### 6.1 班级整体数据概览

获取班级或全体学生的整体学习数据统计。

**请求**

- **URL**: `GET /api/analytics/overview`
- **是否需要认证**: 是（需教师权限）

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `class_id` | int | 否 | - | 班级ID，不传则返回所有学生数据 |

**请求示例**

```
GET /api/analytics/overview?class_id=1
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "total_students": 50,
    "total_challenges": 30,
    "completion_rate": 68.5,
    "avg_stars": 2.3,
    "stuck_top5": [
      {
        "challenge_id": 12,
        "title": "JavaScript异步编程",
        "difficulty": "gold",
        "stuck_count": 15
      },
      {
        "challenge_id": 8,
        "title": "CSS Grid布局",
        "difficulty": "silver",
        "stuck_count": 12
      }
    ]
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `total_students` | int | 学生总数 |
| `total_challenges` | int | 关卡总数 |
| `completion_rate` | float | 完成率（百分比） |
| `avg_stars` | float | 平均星级 |
| `stuck_top5` | array | 卡关Top5列表（提交次数多但未通过的关卡） |
| `stuck_top5[].stuck_count` | int | 卡关人数 |

**错误响应**

```json
{
  "code": 403,
  "message": "班级不存在或无权限访问",
  "data": null
}
```

---

### 6.2 知识掌握热力图

获取各知识分类在不同段位的掌握情况数据，用于绘制热力图。

**请求**

- **URL**: `GET /api/analytics/heatmap`
- **是否需要认证**: 是（需教师权限）

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `class_id` | int | 否 | - | 班级ID，不传则统计所有学生 |

**请求示例**

```
GET /api/analytics/heatmap?class_id=1
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "categories": ["CSS", "HTML", "JavaScript", "Vue", "React"],
    "series": [
      {
        "name": "青铜",
        "data": [85.0, 90.0, 60.0, 30.0, 20.0]
      },
      {
        "name": "白银",
        "data": [70.0, 80.0, 45.0, 15.0, 10.0]
      },
      {
        "name": "黄金",
        "data": [50.0, 65.0, 30.0, 10.0, 0.0]
      },
      {
        "name": "钻石",
        "data": [20.0, 40.0, 15.0, 0.0, 0.0]
      },
      {
        "name": "王者",
        "data": [0.0, 10.0, 5.0, 0.0, 0.0]
      }
    ]
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `categories` | string[] | 知识分类列表（X轴） |
| `series` | array | 各段位数据系列（Y轴） |
| `series[].name` | string | 段位名称（中文） |
| `series[].data` | float[] | 各分类的完成率（百分比） |

---

### 6.3 个体能力分析

获取指定学生的能力雷达图数据和最近提交记录。

**请求**

- **URL**: `GET /api/analytics/student/{student_id}`
- **是否需要认证**: 是（需教师权限）

**路径参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `student_id` | int | 是 | 学生ID |

**请求示例**

```
GET /api/analytics/student/10
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "student_info": {
      "id": 10,
      "username": "lisi",
      "nickname": "李四",
      "email": "lisi@example.com",
      "created_at": "2025-02-01T09:00:00"
    },
    "radar_data": {
      "dimensions": ["HTML", "CSS", "JavaScript", "Vue", "React"],
      "values": [88.5, 72.0, 55.3, 30.0, 15.0]
    },
    "recent_submissions": [
      {
        "id": 200,
        "challenge_id": 15,
        "title": "Vue组件通信",
        "category": "Vue",
        "difficulty": "gold",
        "score": 75,
        "stars": 2,
        "created_at": "2025-03-20T16:00:00"
      }
    ]
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `radar_data.dimensions` | string[] | 雷达图维度（知识分类） |
| `radar_data.values` | float[] | 各维度的平均得分 |
| `recent_submissions` | array | 最近10条提交记录 |

**错误响应**

```json
{
  "code": 404,
  "message": "学生不存在",
  "data": null
}
```

---

### 6.4 高频错误分析

获取AI聚类分析后的高频错误类型统计，帮助教师了解学生常见问题。

**请求**

- **URL**: `GET /api/analytics/errors`
- **是否需要认证**: 是（需教师权限）

**请求参数 (Query String)**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `class_id` | int | 否 | - | 班级ID，不传则统计所有学生 |
| `limit` | int | 否 | 10 | 返回的错误类型数量上限 |

**请求示例**

```
GET /api/analytics/errors?class_id=1&limit=5
```

**成功响应**

```json
{
  "code": 200,
  "data": {
    "error_types": [
      {
        "type": "语法错误",
        "count": 25,
        "examples": [
          "缺少闭合标签...</p>标签未正确闭合...",
          "属性值未加引号...",
          "标签嵌套顺序不正确..."
        ]
      },
      {
        "type": "样式问题",
        "count": 18,
        "examples": [
          "CSS选择器使用不当...",
          "Flex布局方向设置错误..."
        ]
      },
      {
        "type": "逻辑错误",
        "count": 12,
        "examples": [
          "条件判断逻辑有误..."
        ]
      }
    ],
    "total_analyzed": 100
  }
}
```

**字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `error_types` | array | 错误类型列表，按出现次数降序排列 |
| `error_types[].type` | string | 错误类型名称 |
| `error_types[].count` | int | 出现次数 |
| `error_types[].examples` | string[] | 错误示例（最多3条） |
| `total_analyzed` | int | 分析的低分提交总数 |

---

## 附录：段位说明

| 段位 | 英文标识 | 说明 |
|------|----------|------|
| 青铜 | `bronze` | 入门级 |
| 白银 | `silver` | 基础级 |
| 黄金 | `gold` | 进阶级 |
| 钻石 | `diamond` | 高级 |
| 王者 | `king` | 大师级 |
