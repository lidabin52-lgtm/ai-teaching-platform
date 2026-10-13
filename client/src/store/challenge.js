/**
 * 闯关状态管理 Store
 * 管理关卡数据、编辑器状态、审判结果等
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// ========== 完整Mock数据（15关） ==========
const MOCK_CHALLENGES = [
  // 青铜段位（5关）
  {
    id: 1, title: 'HTML基础结构', difficulty: 'bronze', difficultyLabel: '青铜',
    orderNum: 1, category: 'HTML', tags: ['基础', 'HTML结构'], language: 'html',
    timeLimit: 30, hintCount: 3, minStars: 1, status: 'unlocked', bestStars: 0,
    description: `# 🏗️ HTML基础结构\n\n## 任务目标\n创建一个标准的HTML5页面结构。\n\n## 具体要求\n1. 使用正确的 \`<!DOCTYPE html>\` 声明\n2. 包含 \`<html>\`、\`<head>\`、\`<body>\` 标签\n3. 在 \`<head>\` 中添加 \`<title>\` 标签，内容为"我的第一个网页"\n4. 在 \`<body>\` 中添加一个 \`<h1>\` 标题，内容为"Hello World"\n5. 添加一个 \`<p>\` 段落，内容为"欢迎来到前端学习之旅！"\n\n## 预期效果\n页面应该显示一个主标题和一段欢迎文字。`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <!-- 在这里添加title标签 -->\n</head>\n<body>\n    <!-- 在这里添加h1标题和p段落 -->\n</body>\n</html>`
  },
  {
    id: 2, title: '常用文本标签', difficulty: 'bronze', difficultyLabel: '青铜',
    orderNum: 2, category: 'HTML', tags: ['基础', '文本标签'], language: 'html',
    timeLimit: 30, hintCount: 3, minStars: 1, status: 'locked', bestStars: 0,
    description: `# 📝 常用文本标签\n\n## 任务目标\n掌握HTML中常用的文本格式化标签。\n\n## 具体要求\n1. 使用 \`<strong>\` 标记重要内容\n2. 使用 \`<em>\` 标记强调内容\n3. 使用 \`<mark>\` 高亮显示内容\n4. 使用 \`<code>\` 显示代码片段\n5. 添加一个有序列表 \`<ol>\`，包含3个学习步骤\n6. 添加一个无序列表 \`<ul>\`，包含3个前端技术`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>文本标签练习</title>\n</head>\n<body>\n    <!-- 在这里创建格式化文本 -->\n</body>\n</html>`
  },
  {
    id: 3, title: '链接与图片', difficulty: 'bronze', difficultyLabel: '青铜',
    orderNum: 3, category: 'HTML', tags: ['基础', '链接', '图片'], language: 'html',
    timeLimit: 30, hintCount: 3, minStars: 1, status: 'locked', bestStars: 0,
    description: `# 🔗 链接与图片\n\n## 任务目标\n学会在网页中添加超链接和图片。\n\n## 具体要求\n1. 创建一个指向 https://www.example.com 的超链接\n2. 设置链接在新标签页打开\n3. 插入一张图片，使用 picsum.photos\n4. 为图片添加alt属性`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>链接与图片</title>\n</head>\n<body>\n    <h1>链接与图片练习</h1>\n    <!-- 在这里添加超链接和图片 -->\n</body>\n</html>`
  },
  {
    id: 4, title: '表格基础', difficulty: 'bronze', difficultyLabel: '青铜',
    orderNum: 4, category: 'HTML', tags: ['基础', '表格'], language: 'html',
    timeLimit: 30, hintCount: 3, minStars: 1, status: 'locked', bestStars: 0,
    description: `# 📊 表格基础\n\n## 任务目标\n创建一个简单的数据表格。\n\n## 具体要求\n1. 创建一个3行3列的表格\n2. 第一行为表头：姓名、年龄、城市\n3. 添加两条数据行\n4. 为表格添加边框`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>表格练习</title>\n</head>\n<body>\n    <h1>学生信息表</h1>\n    <!-- 在这里创建表格 -->\n</body>\n</html>`
  },
  {
    id: 5, title: '表单元素', difficulty: 'bronze', difficultyLabel: '青铜',
    orderNum: 5, category: 'HTML', tags: ['基础', '表单'], language: 'html',
    timeLimit: 30, hintCount: 3, minStars: 1, status: 'locked', bestStars: 0,
    description: `# 📋 表单元素\n\n## 任务目标\n创建一个用户注册表单。\n\n## 具体要求\n1. 用户名输入框（text类型）\n2. 邮箱输入框（email类型）\n3. 密码输入框（password类型）\n4. 性别单选按钮\n5. 兴趣爱好复选框\n6. 提交按钮`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>表单练习</title>\n</head>\n<body>\n    <h1>用户注册</h1>\n    <!-- 在这里创建表单 -->\n</body>\n</html>`
  },
  // 白银段位（4关）
  {
    id: 6, title: 'CSS选择器', difficulty: 'silver', difficultyLabel: '白银',
    orderNum: 6, category: 'CSS', tags: ['CSS', '选择器'], language: 'html',
    timeLimit: 40, hintCount: 3, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 🎯 CSS选择器\n\n## 任务目标\n掌握CSS的各种选择器用法。\n\n## 具体要求\n1. 使用元素选择器设置所有p元素颜色\n2. 使用类选择器设置特定样式\n3. 使用ID选择器设置特定样式\n4. 使用后代选择器设置嵌套元素样式`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>CSS选择器</title>\n    <style>\n        /* 在这里编写CSS */\n    </style>\n</head>\n<body>\n    <p class="intro">带有intro类的段落</p>\n    <p id="highlight">带有ID的段落</p>\n    <p>普通段落</p>\n</body>\n</html>`
  },
  {
    id: 7, title: '盒模型基础', difficulty: 'silver', difficultyLabel: '白银',
    orderNum: 7, category: 'CSS', tags: ['CSS', '盒模型'], language: 'html',
    timeLimit: 40, hintCount: 3, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 📦 盒模型基础\n\n## 任务目标\n理解CSS盒模型的各个组成部分。\n\n## 具体要求\n1. 设置宽高、背景色\n2. 设置padding、border、margin\n3. 使用box-sizing: border-box`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>盒模型</title>\n    <style>\n        /* 在这里编写CSS */\n    </style>\n</head>\n<body>\n    <div class="box1">标准盒模型</div>\n    <div class="box2">border-box</div>\n</body>\n</html>`
  },
  {
    id: 8, title: 'Flex布局入门', difficulty: 'silver', difficultyLabel: '白银',
    orderNum: 8, category: 'CSS', tags: ['CSS', 'Flexbox'], language: 'html',
    timeLimit: 40, hintCount: 3, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 🎯 Flex布局入门\n\n## 任务目标\n掌握Flex布局的基本用法。\n\n## 具体要求\n1. 设置display: flex\n2. 使用justify-content分布子元素\n3. 使用align-items垂直居中`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>Flex布局</title>\n    <style>\n        /* 在这里编写CSS */\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="item">1</div>\n        <div class="item">2</div>\n        <div class="item">3</div>\n    </div>\n</body>\n</html>`
  },
  {
    id: 9, title: '定位与层叠', difficulty: 'silver', difficultyLabel: '白银',
    orderNum: 9, category: 'CSS', tags: ['CSS', '定位'], language: 'html',
    timeLimit: 40, hintCount: 3, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 📍 定位与层叠\n\n## 任务目标\n掌握CSS定位属性。\n\n## 具体要求\n1. 相对定位容器\n2. 绝对定位子元素\n3. 固定定位元素\n4. z-index层叠顺序`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>定位练习</title>\n    <style>\n        /* 在这里编写CSS */\n    </style>\n</head>\n<body>\n    <div class="container">\n        <div class="box red">红</div>\n        <div class="box green">绿</div>\n        <div class="box blue">蓝</div>\n    </div>\n</body>\n</html>`
  },
  // 黄金段位（3关）
  {
    id: 10, title: 'DOM操作基础', difficulty: 'gold', difficultyLabel: '黄金',
    orderNum: 10, category: 'JavaScript', tags: ['JS', 'DOM'], language: 'html',
    timeLimit: 45, hintCount: 2, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 🌳 DOM操作基础\n\n## 任务目标\n掌握JavaScript DOM操作。\n\n## 具体要求\n1. 获取元素\n2. 改变文字内容\n3. 改变样式\n4. 添加新元素\n5. 使用addEventListener绑定事件`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>DOM操作</title>\n    <style>\n        #message { padding: 20px; border: 1px solid #ccc; margin: 10px 0; }\n    </style>\n</head>\n<body>\n    <div id="message">Hello</div>\n    <button id="btn1">改变文字</button>\n    <button id="btn2">改变颜色</button>\n    <button id="btn3">添加元素</button>\n    <script>\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  },
  {
    id: 11, title: '事件处理与表单验证', difficulty: 'gold', difficultyLabel: '黄金',
    orderNum: 11, category: 'JavaScript', tags: ['JS', '事件', '表单'], language: 'html',
    timeLimit: 45, hintCount: 2, minStars: 2, status: 'locked', bestStars: 0,
    description: `# ✅ 事件处理与表单验证\n\n## 任务目标\n实现表单验证功能。\n\n## 具体要求\n1. 用户名至少3个字符\n2. 密码至少6个字符\n3. 验证失败显示错误信息\n4. 阻止表单默认提交`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>表单验证</title>\n    <style>\n        .error { color: red; font-size: 12px; }\n    </style>\n</head>\n<body>\n    <form id="loginForm">\n        <div>\n            <label>用户名：</label>\n            <input type="text" id="username">\n            <span class="error" id="usernameError"></span>\n        </div>\n        <div>\n            <label>密码：</label>\n            <input type="password" id="password">\n            <span class="error" id="passwordError"></span>\n        </div>\n        <button type="submit">登录</button>\n    </form>\n    <script>\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  },
  {
    id: 12, title: '数组与循环', difficulty: 'gold', difficultyLabel: '黄金',
    orderNum: 12, category: 'JavaScript', tags: ['JS', '数组'], language: 'html',
    timeLimit: 45, hintCount: 2, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 🔄 数组与循环\n\n## 任务目标\n掌握JavaScript数组操作和循环。\n\n## 具体要求\n1. 创建学生数组\n2. 遍历显示列表\n3. 计算平均分\n4. 找出最高分\n5. filter过滤优秀学生`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>数组操作</title>\n</head>\n<body>\n    <h2>学生成绩列表</h2>\n    <div id="studentList"></div>\n    <h3>统计信息</h3>\n    <div id="stats"></div>\n    <script>\n        const students = [\n            { name: '张三', score: 85 },\n            { name: '李四', score: 72 },\n            { name: '王五', score: 90 },\n            { name: '赵六', score: 65 },\n            { name: '孙七', score: 88 }\n        ];\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  },
  // 钻石段位（2关）
  {
    id: 13, title: '待办事项应用', difficulty: 'diamond', difficultyLabel: '钻石',
    orderNum: 13, category: '综合', tags: ['综合', 'DOM', '事件'], language: 'html',
    timeLimit: 60, hintCount: 1, minStars: 2, status: 'locked', bestStars: 0,
    description: `# ✅ 待办事项应用\n\n## 任务目标\n创建一个功能完整的待办事项应用。\n\n## 具体要求\n1. 添加新任务\n2. 完成/未完成切换\n3. 删除任务\n4. 显示任务数量\n5. localStorage持久化`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>待办事项</title>\n    <style>\n        .completed { text-decoration: line-through; color: #999; }\n        .todo-item { padding: 10px; border-bottom: 1px solid #eee; }\n    </style>\n</head>\n<body>\n    <h1>待办事项</h1>\n    <div>\n        <input type="text" id="todoInput" placeholder="输入新任务">\n        <button id="addBtn">添加</button>\n    </div>\n    <ul id="todoList"></ul>\n    <div>\n        <span>待完成: <span id="activeCount">0</span></span>\n        <span>已完成: <span id="completedCount">0</span></span>\n    </div>\n    <script>\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  },
  {
    id: 14, title: '图片轮播组件', difficulty: 'diamond', difficultyLabel: '钻石',
    orderNum: 14, category: '综合', tags: ['综合', 'CSS', 'JS'], language: 'html',
    timeLimit: 60, hintCount: 1, minStars: 2, status: 'locked', bestStars: 0,
    description: `# 🎠 图片轮播组件\n\n## 任务目标\n创建一个自动轮播的图片组件。\n\n## 具体要求\n1. 3张图片轮播\n2. 自动轮播（3秒）\n3. 左右切换按钮\n4. 底部指示器\n5. 鼠标悬停暂停`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <title>图片轮播</title>\n    <style>\n        .carousel { position: relative; width: 600px; height: 400px; overflow: hidden; margin: 0 auto; }\n        .slide { display: none; } .slide.active { display: block; }\n        .slide img { width: 100%; height: 100%; object-fit: cover; }\n        .prev, .next { position: absolute; top: 50%; transform: translateY(-50%); padding: 10px; background: rgba(0,0,0,0.5); color: white; cursor: pointer; }\n        .prev { left: 10px; } .next { right: 10px; }\n    </style>\n</head>\n<body>\n    <div class="carousel">\n        <div class="slide active"><img src="https://picsum.photos/600/400?random=1" alt="1"></div>\n        <div class="slide"><img src="https://picsum.photos/600/400?random=2" alt="2"></div>\n        <div class="slide"><img src="https://picsum.photos/600/400?random=3" alt="3"></div>\n        <div class="prev" id="prevBtn">&#10094;</div>\n        <div class="next" id="nextBtn">&#10095;</div>\n    </div>\n    <script>\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  },
  // 王者段位（1关）
  {
    id: 15, title: '综合实战：个人作品集', difficulty: 'king', difficultyLabel: '王者',
    orderNum: 15, category: '综合', tags: ['综合', 'HTML', 'CSS', 'JS'], language: 'html',
    timeLimit: 90, hintCount: 0, minStars: 3, status: 'locked', bestStars: 0,
    description: `# 👑 综合实战：个人作品集网站\n\n## 任务目标\n运用所学知识创建完整的个人作品集。\n\n## 具体要求\n1. 固定导航栏，平滑滚动\n2. 全屏英雄区，打字机效果\n3. Grid布局作品展示\n4. 两栏关于我布局\n5. 联系表单\n6. 响应式设计\n7. 滚动动画`,
    starterCode: `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>个人作品集</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: 'Microsoft YaHei', sans-serif; }\n        /* 在这里添加更多CSS */\n    </style>\n</head>\n<body>\n    <nav>导航栏</nav>\n    <section id="hero" style="height:100vh;display:flex;align-items:center;justify-content:center;">英雄区</section>\n    <section id="works" style="padding:60px 20px;">作品展示</section>\n    <section id="about" style="padding:60px 20px;">关于我</section>\n    <section id="contact" style="padding:60px 20px;">联系我</section>\n    <script>\n        // 在这里编写JavaScript\n    </script>\n</body>\n</html>`
  }
]

const MOCK_JUDGE_RESULT = {
  functionScore: 3,
  standardScore: 2,
  coolScore: 2,
  totalStars: 3,
  comment: '代码完成度很好！功能完整，结构清晰。建议继续优化代码规范性。',
  hint: ''
}

// ========== Store定义 ==========
export const useChallengeStore = defineStore('challenge', () => {
  // ========== State ==========
  const currentChallenge = ref(null)
  const challengeList = ref([])
  const editorCode = ref('')
  const isSubmitting = ref(false)
  const judgeResult = ref(null)
  const showJudgeModal = ref(false)
  const previewKey = ref(0)
  const submissions = ref([])
  const isLoading = ref(false)
  const useBackend = ref(false) // 是否使用后端API

  // ========== Getters ==========
  const difficultyColor = computed(() => {
    const colors = {
      bronze: '#CD7F32', silver: '#C0C0C0', gold: '#FFD700',
      diamond: '#B9F2FF', king: '#FF6B6B'
    }
    return colors[currentChallenge.value?.difficulty] || '#999'
  })

  const difficultyBadge = computed(() => {
    const badges = {
      bronze: '青铜', silver: '白银', gold: '黄金',
      diamond: '钻石', king: '王者'
    }
    return badges[currentChallenge.value?.difficulty] || '未知'
  })

  const canSubmit = computed(() => {
    return editorCode.value.trim().length > 0 && !isSubmitting.value
  })

  const bestStars = computed(() => {
    return currentChallenge.value?.bestStars || 0
  })

  // ========== Actions ==========

  /**
   * 加载关卡列表
   */
  async function loadChallengeList() {
    isLoading.value = true
    try {
      // 尝试从后端API加载
      const res = await fetch('/api/challenge/list')
      if (res.ok) {
        const data = await res.json()
        if (data.code === 200 && data.data && data.data.length > 0) {
          challengeList.value = data.data
          useBackend.value = true
          return challengeList.value
        }
      }
    } catch (e) {
      // 后端不可用，使用Mock数据
      console.log('使用Mock数据')
    }

    // 使用Mock数据
    await new Promise(resolve => setTimeout(resolve, 300))
    challengeList.value = MOCK_CHALLENGES
    useBackend.value = false
    return challengeList.value
  }

  /**
   * 加载关卡详情
   */
  async function loadChallengeDetail(challengeId) {
    isLoading.value = true
    try {
      // 尝试从后端API加载
      const res = await fetch(`/api/challenge/${challengeId}`)
      if (res.ok) {
        const data = await res.json()
        if (data.code === 200 && data.data) {
          currentChallenge.value = data.data
          editorCode.value = data.data.starter_code || data.data.starterCode || ''
          useBackend.value = true
          return currentChallenge.value
        }
      }
    } catch (e) {
      console.log('使用Mock数据')
    }

    // 使用Mock数据
    await new Promise(resolve => setTimeout(resolve, 200))
    const challenge = MOCK_CHALLENGES.find(c => c.id === challengeId)
    if (!challenge) throw new Error('关卡不存在')

    currentChallenge.value = challenge
    editorCode.value = challenge.starterCode
    useBackend.value = false
    return challenge
  }

  /**
   * 更新编辑器代码
   */
  function updateCode(code) {
    editorCode.value = code
  }

  /**
   * 重置代码
   */
  function resetCode() {
    if (currentChallenge.value) {
      editorCode.value = currentChallenge.value.starterCode || currentChallenge.value.starter_code || ''
      previewKey.value++
    }
  }

  /**
   * 提交代码审判
   */
  async function submitCode() {
    if (!canSubmit.value) return

    isSubmitting.value = true
    try {
      // 尝试调用后端API
      if (useBackend.value && currentChallenge.value) {
        const res = await fetch(`/api/challenge/${currentChallenge.value.id}/submit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: editorCode.value })
        })
        if (res.ok) {
          const data = await res.json()
          if (data.code === 200 && data.data) {
            judgeResult.value = data.data
            showJudgeModal.value = true
            return judgeResult.value
          }
        }
      }

      // Mock审判结果
      await new Promise(resolve => setTimeout(resolve, 1500))
      const scores = [2, 3][Math.floor(Math.random() * 2)]
      judgeResult.value = {
        functionScore: scores,
        standardScore: scores,
        coolScore: Math.max(1, scores - 1),
        totalStars: scores,
        comment: '代码完成度不错！功能基本实现，结构清晰。建议继续优化代码规范性和最佳实践。',
        hint: ''
      }
      showJudgeModal.value = true

      // 更新关卡状态
      if (currentChallenge.value) {
        currentChallenge.value.status = 'completed'
        currentChallenge.value.bestStars = Math.max(currentChallenge.value.bestStars, scores)
        // 解锁下一关
        const next = MOCK_CHALLENGES.find(c => c.orderNum === currentChallenge.value.orderNum + 1)
        if (next) next.status = 'unlocked'
      }

      return judgeResult.value
    } catch (error) {
      console.error('提交代码失败:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  /**
   * 关闭审判弹窗
   */
  function closeJudgeModal() {
    showJudgeModal.value = false
  }

  /**
   * 获取下一关
   */
  function getNextChallenge() {
    if (!currentChallenge.value) return null
    const currentIndex = challengeList.value.findIndex(c => c.id === currentChallenge.value.id)
    return challengeList.value[currentIndex + 1] || null
  }

  return {
    currentChallenge, challengeList, editorCode, isSubmitting,
    judgeResult, showJudgeModal, previewKey, submissions, isLoading,
    difficultyColor, difficultyBadge, canSubmit, bestStars,
    loadChallengeList, loadChallengeDetail, updateCode, resetCode,
    submitCode, closeJudgeModal, getNextChallenge
  }
})
