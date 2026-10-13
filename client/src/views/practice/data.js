/**
 * 在线练习题库
 * 与技能闯关不同，这里是自由选题的练习场
 * 每道题都有：题目描述、初始代码、参考答案、测试用例、AI点评要点
 */

export const practiceCategories = [
  { id: 'html', name: 'HTML基础', icon: '🌐', color: '#e44d26' },
  { id: 'css', name: 'CSS样式', icon: '🎨', color: '#264de4' },
  { id: 'js', name: 'JavaScript', icon: '⚡', color: '#f7df1e' },
  { id: 'comprehensive', name: '综合实战', icon: '💎', color: '#9b59b6' }
]

export const practiceList = [
  // ========== HTML 基础 ==========
  {
    id: 1,
    categoryId: 'html',
    title: '制作个人名片卡片',
    difficulty: '简单',
    difficultyType: 'success',
    description: '使用HTML标签制作一张个人名片卡片，包含头像区域、姓名、职位、联系方式和简介。',
    requirements: [
      '使用语义化标签（header, main, section等）',
      '包含头像占位区域（用div+背景色代替）',
      '包含姓名、职位、邮箱、电话信息',
      '包含一段个人简介',
      '整体结构清晰，标签嵌套正确'
    ],
    language: 'html',
    fileName: 'card.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>个人名片</title>\n</head>\n<body>\n    <!-- 在这里编写你的名片 -->\n    \n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>个人名片</title>\n</head>\n<body>\n    <article class="card">\n        <header>\n            <div class="avatar">头像</div>\n            <h1>张三</h1>\n            <p class="title">前端开发工程师</p>\n        </header>\n        <main>\n            <section class="contact">\n                <p>邮箱：zhangsan@example.com</p>\n                <p>电话：138-0000-0000</p>\n            </section>\n            <section class="bio">\n                <h2>个人简介</h2>\n                <p>热爱前端开发，擅长HTML/CSS/JavaScript，\n                致力于打造优秀的用户体验。</p>\n            </section>\n        </main>\n    </article>\n</body>\n</html>',
    aiReviewPoints: [
      '检查是否使用了语义化标签（article, header, section等）',
      '检查标签嵌套是否正确，是否有未闭合的标签',
      '检查信息结构是否完整（姓名、职位、联系方式、简介）',
      '建议使用合适的标题层级（h1用于姓名，h2用于分节标题）'
    ]
  },
  {
    id: 2,
    categoryId: 'html',
    title: '构建商品列表页面',
    difficulty: '中等',
    difficultyType: '',
    description: '使用HTML表格和列表标签构建一个商品信息展示页面，展示3个商品的名称、价格、描述和特性。',
    requirements: [
      '使用table展示商品基本信息（名称、价格、库存）',
      '使用ul/ol列表展示每个商品的特性',
      '使用表单包含一个"加入购物车"按钮',
      '合理使用th和td区分表头和数据'
    ],
    language: 'html',
    fileName: 'products.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>商品列表</title>\n</head>\n<body>\n    <h1>商品列表</h1>\n    <!-- 在这里编写商品列表 -->\n    \n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>商品列表</title>\n</head>\n<body>\n    <h1>商品列表</h1>\n    <table border="1">\n        <thead>\n            <tr>\n                <th>商品名称</th>\n                <th>价格</th>\n                <th>库存</th>\n                <th>操作</th>\n            </tr>\n        </thead>\n        <tbody>\n            <tr>\n                <td>JavaScript高级编程</td>\n                <td>99元</td>\n                <td>50</td>\n                <td><button>加入购物车</button></td>\n            </tr>\n            <tr>\n                <td>CSS权威指南</td>\n                <td>89元</td>\n                <td>30</td>\n                <td><button>加入购物车</button></td>\n            </tr>\n            <tr>\n                <td>HTML5与CSS3基础</td>\n                <td>69元</td>\n                <td>100</td>\n                <td><button>加入购物车</button></td>\n            </tr>\n        </tbody>\n    </table>\n</body>\n</html>',
    aiReviewPoints: [
      '检查table结构是否完整（thead + tbody）',
      '检查th用于表头、td用于数据单元格',
      '检查表单元素是否正确使用',
      '建议为表格添加caption标题'
    ]
  },
  {
    id: 3,
    categoryId: 'html',
    title: '制作注册表单',
    difficulty: '简单',
    difficultyType: 'success',
    description: '创建一个用户注册表单，包含用户名、邮箱、密码、确认密码和兴趣爱好选择。',
    requirements: [
      '使用label标签关联表单控件',
      '包含text、email、password、checkbox输入类型',
      '包含一个submit提交按钮',
      '使用fieldset和legend分组表单内容'
    ],
    language: 'html',
    fileName: 'form.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>用户注册</title>\n</head>\n<body>\n    <h1>用户注册</h1>\n    <!-- 在这里编写注册表单 -->\n    \n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>用户注册</title>\n</head>\n<body>\n    <h1>用户注册</h1>\n    <form>\n        <fieldset>\n            <legend>基本信息</legend>\n            <label for="username">用户名：</label>\n            <input type="text" id="username" placeholder="请输入用户名">\n            <br><br>\n            <label for="email">邮箱：</label>\n            <input type="email" id="email" placeholder="请输入邮箱">\n        </fieldset>\n        <fieldset>\n            <legend>安全设置</legend>\n            <label for="pwd">密码：</label>\n            <input type="password" id="pwd" placeholder="请输入密码">\n            <br><br>\n            <label for="pwd2">确认密码：</label>\n            <input type="password" id="pwd2" placeholder="请再次输入密码">\n        </fieldset>\n        <fieldset>\n            <legend>兴趣爱好</legend>\n            <input type="checkbox" id="coding" value="coding">\n            <label for="coding">编程</label>\n            <input type="checkbox" id="music" value="music">\n            <label for="music">音乐</label>\n            <input type="checkbox" id="sports" value="sports">\n            <label for="sports">运动</label>\n        </fieldset>\n        <br>\n        <button type="submit">注册</button>\n    </form>\n</body>\n</html>',
    aiReviewPoints: [
      '检查label的for属性是否与input的id对应',
      '检查是否使用了正确的input type（email、password等）',
      '检查fieldset/legend是否正确分组',
      '建议为必填字段添加required属性'
    ]
  },

  // ========== CSS 样式 ==========
  {
    id: 4,
    categoryId: 'css',
    title: 'Flex导航栏布局',
    difficulty: '简单',
    difficultyType: 'success',
    description: '使用Flexbox实现一个水平导航栏，要求Logo在左侧，导航链接在右侧均匀分布，整体垂直居中。',
    requirements: [
      '使用display: flex布局',
      'Logo在左侧，导航链接在右侧',
      '链接之间间距均匀',
      '导航项垂直居中',
      '高度固定60px，背景色深色'
    ],
    language: 'html',
    fileName: 'navbar.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>Flex导航栏</title>\n    <style>\n        /* 在这里编写CSS样式 */\n        \n    </style>\n</head>\n<body>\n    <nav class="navbar">\n        <div class="logo">MyLogo</div>\n        <div class="nav-links">\n            <a href="#">首页</a>\n            <a href="#">产品</a>\n            <a href="#">关于</a>\n            <a href="#">联系我们</a>\n        </div>\n    </nav>\n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>Flex导航栏</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: sans-serif; }\n        \n        .navbar {\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            height: 60px;\n            background: #333;\n            padding: 0 20px;\n        }\n        \n        .logo {\n            color: white;\n            font-size: 24px;\n            font-weight: bold;\n        }\n        \n        .nav-links {\n            display: flex;\n            gap: 20px;\n        }\n        \n        .nav-links a {\n            color: white;\n            text-decoration: none;\n            padding: 8px 16px;\n        }\n        \n        .nav-links a:hover {\n            background: #555;\n            border-radius: 4px;\n        }\n    </style>\n</head>\n<body>\n    <nav class="navbar">\n        <div class="logo">MyLogo</div>\n        <div class="nav-links">\n            <a href="#">首页</a>\n            <a href="#">产品</a>\n            <a href="#">关于</a>\n            <a href="#">联系我们</a>\n        </div>\n    </nav>\n</body>\n</html>',
    aiReviewPoints: [
      '检查是否使用了display: flex',
      '检查justify-content和align-items的使用',
      '检查gap属性设置元素间距',
      '建议使用hover伪类增强交互体验'
    ]
  },
  {
    id: 5,
    categoryId: 'css',
    title: '卡片悬浮效果',
    difficulty: '中等',
    difficultyType: '',
    description: '制作3张并排的卡片，鼠标悬浮时卡片上浮并显示阴影效果，包含图片区、标题和描述。',
    requirements: [
      '3张卡片使用Flex或Grid水平排列',
      '卡片有圆角和边框',
      '鼠标悬浮时transform: translateY(-10px)',
      '悬浮时增加box-shadow',
      '添加transition过渡动画'
    ],
    language: 'html',
    fileName: 'cards.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>卡片悬浮效果</title>\n    <style>\n        /* 在这里编写CSS样式 */\n        \n    </style>\n</head>\n<body>\n    <div class="cards-container">\n        <div class="card">\n            <div class="card-img">图片1</div>\n            <h3>卡片标题1</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n        <div class="card">\n            <div class="card-img">图片2</div>\n            <h3>卡片标题2</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n        <div class="card">\n            <div class="card-img">图片3</div>\n            <h3>卡片标题3</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n    </div>\n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>卡片悬浮效果</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: sans-serif; padding: 40px; background: #f5f5f5; }\n        \n        .cards-container {\n            display: flex;\n            gap: 20px;\n            justify-content: center;\n        }\n        \n        .card {\n            width: 250px;\n            background: white;\n            border-radius: 12px;\n            overflow: hidden;\n            border: 1px solid #e0e0e0;\n            transition: transform 0.3s, box-shadow 0.3s;\n            cursor: pointer;\n        }\n        \n        .card:hover {\n            transform: translateY(-10px);\n            box-shadow: 0 12px 24px rgba(0,0,0,0.15);\n        }\n        \n        .card-img {\n            height: 150px;\n            background: #ddd;\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            color: #999;\n        }\n        \n        .card h3 { padding: 16px 16px 8px; }\n        .card p { padding: 0 16px 16px; color: #666; font-size: 14px; }\n    </style>\n</head>\n<body>\n    <div class="cards-container">\n        <div class="card">\n            <div class="card-img">图片1</div>\n            <h3>卡片标题1</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n        <div class="card">\n            <div class="card-img">图片2</div>\n            <h3>卡片标题2</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n        <div class="card">\n            <div class="card-img">图片3</div>\n            <h3>卡片标题3</h3>\n            <p>这是卡片描述内容</p>\n        </div>\n    </div>\n</body>\n</html>',
    aiReviewPoints: [
      '检查是否使用了transition实现平滑过渡',
      '检查transform: translateY的使用是否正确',
      '检查box-shadow的参数设置',
      '建议添加cursor: pointer增强交互提示'
    ]
  },
  {
    id: 6,
    categoryId: 'css',
    title: '响应式三栏布局',
    difficulty: '困难',
    difficultyType: 'danger',
    description: '实现经典的三栏布局：左侧导航（200px）、中间内容（自适应）、右侧边栏（250px），在窄屏下变为单栏。',
    requirements: [
      '桌面端：左-中-右三栏布局',
      '中间内容区域宽度自适应',
      '使用media query在768px以下变为单栏',
      '各栏有不同背景色区分',
      '最小高度100vh'
    ],
    language: 'html',
    fileName: 'layout.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>响应式三栏布局</title>\n    <style>\n        /* 在这里编写CSS样式 */\n        \n    </style>\n</head>\n<body>\n    <div class="layout">\n        <aside class="sidebar-left">左侧导航</aside>\n        <main class="content">中间内容区域</main>\n        <aside class="sidebar-right">右侧边栏</aside>\n    </div>\n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>响应式三栏布局</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        \n        .layout {\n            display: flex;\n            min-height: 100vh;\n        }\n        \n        .sidebar-left {\n            width: 200px;\n            background: #2c3e50;\n            color: white;\n            padding: 20px;\n        }\n        \n        .content {\n            flex: 1;\n            background: #ecf0f1;\n            padding: 20px;\n        }\n        \n        .sidebar-right {\n            width: 250px;\n            background: #3498db;\n            color: white;\n            padding: 20px;\n        }\n        \n        @media (max-width: 768px) {\n            .layout {\n                flex-direction: column;\n            }\n            .sidebar-left,\n            .sidebar-right {\n                width: 100%;\n            }\n        }\n    </style>\n</head>\n<body>\n    <div class="layout">\n        <aside class="sidebar-left">左侧导航</aside>\n        <main class="content">中间内容区域</main>\n        <aside class="sidebar-right">右侧边栏</aside>\n    </div>\n</body>\n</html>',
    aiReviewPoints: [
      '检查flex布局中flex: 1是否正确使用',
      '检查media query断点设置是否合理',
      '检查flex-direction: column在响应式下的使用',
      '建议添加过渡动画使布局切换更平滑'
    ]
  },

  // ========== JavaScript ==========
  {
    id: 7,
    categoryId: 'js',
    title: '实现数组去重',
    difficulty: '简单',
    difficultyType: 'success',
    description: '编写一个函数，去除数组中的重复元素，返回一个新数组。要求至少使用两种不同的实现方式。',
    requirements: [
      '函数名为unique，接收一个数组参数',
      '返回去重后的新数组（不修改原数组）',
      '至少实现两种方式（Set、indexOf、filter等）',
      '处理各种数据类型（数字、字符串）'
    ],
    language: 'javascript',
    fileName: 'unique.js',
    initialCode: '// 方式一：使用 Set\nfunction unique(arr) {\n    // 请补充代码\n    \n}\n\n// 方式二：使用 indexOf\nfunction unique2(arr) {\n    // 请补充代码\n    \n}\n\n// 测试\nconst arr = [1, 2, 2, 3, 4, 4, 5, 1, 3];\nconsole.log(unique(arr));   // 期望: [1, 2, 3, 4, 5]\nconsole.log(unique2(arr));  // 期望: [1, 2, 3, 4, 5]',
    referenceCode: '// 方式一：使用 Set（最简洁）\nfunction unique(arr) {\n    return [...new Set(arr)];\n}\n\n// 方式二：使用 filter + indexOf\nfunction unique2(arr) {\n    return arr.filter((item, index) => {\n        return arr.indexOf(item) === index;\n    });\n}\n\n// 方式三：使用 reduce\nfunction unique3(arr) {\n    return arr.reduce((acc, cur) => {\n        if (!acc.includes(cur)) acc.push(cur);\n        return acc;\n    }, []);\n}\n\n// 测试\nconst arr = [1, 2, 2, 3, 4, 4, 5, 1, 3];\nconsole.log(unique(arr));   // [1, 2, 3, 4, 5]\nconsole.log(unique2(arr));  // [1, 2, 3, 4, 5]\nconsole.log(unique3(arr));  // [1, 2, 3, 4, 5]',
    aiReviewPoints: [
      '检查是否正确使用Set数据结构去重',
      '检查filter+indexOf的逻辑是否正确',
      '注意：Set方式无法去除对象类型的重复',
      '建议了解各种方式的性能差异'
    ]
  },
  {
    id: 8,
    categoryId: 'js',
    title: '实现深拷贝函数',
    difficulty: '困难',
    difficultyType: 'danger',
    description: '编写一个deepClone函数，实现对象的深拷贝，能正确处理嵌套对象、数组和基本数据类型。',
    requirements: [
      '函数名为deepClone，接收一个对象参数',
      '正确处理嵌套对象和数组',
      '正确处理null和基本数据类型',
      '不使用JSON.parse(JSON.stringify())'
    ],
    language: 'javascript',
    fileName: 'deepClone.js',
    initialCode: '/**\n * 深拷贝函数\n * @param {Object} obj - 要拷贝的对象\n * @returns {Object} 深拷贝后的新对象\n */\nfunction deepClone(obj) {\n    // 请补充代码\n    \n}\n\n// 测试\nconst original = {\n    name: "张三",\n    age: 25,\n    hobbies: ["编程", "音乐"],\n    address: {\n        city: "北京",\n        district: "海淀"\n    }\n};\n\nconst cloned = deepClone(original);\ncloned.address.city = "上海";\nconsole.log(original.address.city); // 期望: "北京"（不受影响）',
    referenceCode: '/**\n * 深拷贝函数（递归实现）\n */\nfunction deepClone(obj) {\n    // 处理null和非对象类型\n    if (obj === null || typeof obj !== "object") {\n        return obj;\n    }\n    \n    // 处理日期\n    if (obj instanceof Date) {\n        return new Date(obj.getTime());\n    }\n    \n    // 处理数组\n    if (Array.isArray(obj)) {\n        return obj.map(item => deepClone(item));\n    }\n    \n    // 处理普通对象\n    const cloned = {};\n    for (const key in obj) {\n        if (obj.hasOwnProperty(key)) {\n            cloned[key] = deepClone(obj[key]);\n        }\n    }\n    return cloned;\n}\n\n// 测试\nconst original = {\n    name: "张三",\n    age: 25,\n    hobbies: ["编程", "音乐"],\n    address: { city: "北京", district: "海淀" }\n};\n\nconst cloned = deepClone(original);\ncloned.address.city = "上海";\nconsole.log(original.address.city); // "北京"\nconsole.log(cloned.address.city);   // "上海"',
    aiReviewPoints: [
      '检查递归终止条件是否正确（null和非object）',
      '检查是否正确区分数组和普通对象',
      '检查是否使用hasOwnProperty避免原型链属性',
      '进阶：考虑循环引用的处理（WeakMap）'
    ]
  },
  {
    id: 9,
    categoryId: 'js',
    title: '实现发布订阅模式',
    difficulty: '困难',
    difficultyType: 'danger',
    description: '编写一个EventEmitter类，实现on（订阅）、emit（发布）、off（取消订阅）和once（只订阅一次）方法。',
    requirements: [
      'on(eventName, callback)：注册事件监听',
      'emit(eventName, ...args)：触发事件',
      'off(eventName, callback)：移除事件监听',
      'once(eventName, callback)：只触发一次'
    ],
    language: 'javascript',
    fileName: 'emitter.js',
    initialCode: 'class EventEmitter {\n    constructor() {\n        // 请补充代码\n        \n    }\n    \n    on(eventName, callback) {\n        // 订阅事件\n        \n    }\n    \n    emit(eventName, ...args) {\n        // 发布事件\n        \n    }\n    \n    off(eventName, callback) {\n        // 取消订阅\n        \n    }\n    \n    once(eventName, callback) {\n        // 只订阅一次\n        \n    }\n}\n\n// 测试\nconst emitter = new EventEmitter();\nconst fn = (msg) => console.log("收到消息:", msg);\n\nemitter.on("test", fn);\nemitter.emit("test", "Hello");  // 期望输出: 收到消息: Hello\nemitter.off("test", fn);\nemitter.emit("test", "World");  // 期望: 无输出（已取消订阅）',
    referenceCode: 'class EventEmitter {\n    constructor() {\n        this.events = {};\n    }\n    \n    on(eventName, callback) {\n        if (!this.events[eventName]) {\n            this.events[eventName] = [];\n        }\n        this.events[eventName].push(callback);\n        return this;\n    }\n    \n    emit(eventName, ...args) {\n        const callbacks = this.events[eventName];\n        if (callbacks) {\n            callbacks.forEach(cb => cb(...args));\n        }\n        return this;\n    }\n    \n    off(eventName, callback) {\n        const callbacks = this.events[eventName];\n        if (callbacks) {\n            this.events[eventName] = callbacks.filter(\n                cb => cb !== callback && cb.original !== callback\n            );\n        }\n        return this;\n    }\n    \n    once(eventName, callback) {\n        const wrapper = (...args) => {\n            callback(...args);\n            this.off(eventName, wrapper);\n        };\n        wrapper.original = callback;\n        this.on(eventName, wrapper);\n        return this;\n    }\n}\n\n// 测试\nconst emitter = new EventEmitter();\nconst fn = (msg) => console.log("收到消息:", msg);\n\nemitter.on("test", fn);\nemitter.emit("test", "Hello");\nemitter.off("test", fn);\nemitter.emit("test", "World");\n\nemitter.once("greet", (name) => console.log("你好," + name));\nemitter.emit("greet", "张三");\nemitter.emit("greet", "李四"); // 不会输出',
    aiReviewPoints: [
      '检查事件存储结构是否使用对象+数组',
      '检查off方法是否正确过滤回调函数',
      '检查once的实现是否在触发后自动移除',
      '建议支持链式调用（return this）'
    ]
  },
  {
    id: 10,
    categoryId: 'js',
    title: '实现防抖和节流',
    difficulty: '中等',
    difficultyType: '',
    description: '分别实现debounce（防抖）和throttle（节流）函数，理解两者的区别和应用场景。',
    requirements: [
      'debounce(fn, delay)：连续调用只执行最后一次',
      'throttle(fn, interval)：固定间隔执行一次',
      '两个函数都支持取消操作',
      '代码注释说明两者的区别'
    ],
    language: 'javascript',
    fileName: 'debounce-throttle.js',
    initialCode: '/**\n * 防抖函数\n * 场景：搜索框输入、窗口resize\n * 效果：连续触发时，只在最后一次触发后等待delay毫秒再执行\n */\nfunction debounce(fn, delay) {\n    // 请补充代码\n    \n}\n\n/**\n * 节流函数\n * 场景：滚动事件、按钮重复点击\n * 效果：在interval毫秒内最多执行一次\n */\nfunction throttle(fn, interval) {\n    // 请补充代码\n    \n}',
    referenceCode: '/**\n * 防抖函数\n * 场景：搜索框输入、窗口resize\n * 效果：连续触发时，只在最后一次触发后等待delay毫秒再执行\n */\nfunction debounce(fn, delay) {\n    let timer = null;\n    \n    const debounced = function (...args) {\n        if (timer) clearTimeout(timer);\n        timer = setTimeout(() => {\n            fn.apply(this, args);\n            timer = null;\n        }, delay);\n    };\n    \n    debounced.cancel = () => {\n        clearTimeout(timer);\n        timer = null;\n    };\n    \n    return debounced;\n}\n\n/**\n * 节流函数\n * 场景：滚动事件、按钮重复点击\n * 效果：在interval毫秒内最多执行一次\n */\nfunction throttle(fn, interval) {\n    let lastTime = 0;\n    \n    const throttled = function (...args) {\n        const now = Date.now();\n        if (now - lastTime >= interval) {\n            fn.apply(this, args);\n            lastTime = now;\n        }\n    };\n    \n    throttled.cancel = () => {\n        lastTime = 0;\n    };\n    \n    return throttled;\n}\n\n// 测试\nconst log = debounce((msg) => console.log("防抖:", msg), 300);\nconst scroll = throttle(() => console.log("节流: 滚动事件"), 500);',
    aiReviewPoints: [
      '检查防抖是否正确使用clearTimeout',
      '检查节流是否使用时间戳判断间隔',
      '检查是否保存了this上下文和arguments',
      '理解区别：防抖是"等停止后再执行"，节流是"匀速执行"'
    ]
  },

  // ========== 综合实战 ==========
  {
    id: 11,
    categoryId: 'comprehensive',
    title: '待办事项应用',
    difficulty: '中等',
    difficultyType: '',
    description: '使用HTML+CSS+JavaScript实现一个完整的待办事项应用，支持添加、完成、删除待办，数据存储在localStorage中。',
    requirements: [
      '输入框+添加按钮添加新待办',
      '点击待办切换完成/未完成状态',
      '删除按钮移除待办',
      '使用localStorage持久化数据',
      '显示待办总数和已完成数量'
    ],
    language: 'html',
    fileName: 'todo.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>待办事项</title>\n    <style>\n        /* 在这里编写样式 */\n        \n    </style>\n</head>\n<body>\n    <div class="todo-app">\n        <h1>待办事项</h1>\n        <div class="input-area">\n            <input type="text" id="todoInput" placeholder="输入待办事项...">\n            <button onclick="addTodo()">添加</button>\n        </div>\n        <ul id="todoList"></ul>\n        <div class="stats" id="stats"></div>\n    </div>\n    <script>\n        // 在这里编写JavaScript逻辑\n        \n    </script>\n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>待办事项</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: sans-serif; background: #f0f2f5; padding: 40px; }\n        .todo-app { max-width: 500px; margin: 0 auto; background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }\n        h1 { margin-bottom: 20px; color: #333; }\n        .input-area { display: flex; gap: 8px; margin-bottom: 20px; }\n        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }\n        .input-area button { padding: 10px 20px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }\n        ul { list-style: none; }\n        li { display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee; gap: 10px; }\n        li.done span { text-decoration: line-through; color: #999; }\n        li span { flex: 1; cursor: pointer; }\n        li button { background: #f56c6c; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; }\n        .stats { margin-top: 16px; color: #666; font-size: 14px; }\n    </style>\n</head>\n<body>\n    <div class="todo-app">\n        <h1>待办事项</h1>\n        <div class="input-area">\n            <input type="text" id="todoInput" placeholder="输入待办事项..." onkeydown="if(event.key===\'Enter\')addTodo()">\n            <button onclick="addTodo()">添加</button>\n        </div>\n        <ul id="todoList"></ul>\n        <div class="stats" id="stats"></div>\n    </div>\n    <script>\n        let todos = JSON.parse(localStorage.getItem("todos")) || [];\n        \n        function save() {\n            localStorage.setItem("todos", JSON.stringify(todos));\n        }\n        \n        function render() {\n            const list = document.getElementById("todoList");\n            list.innerHTML = todos.map(function(todo, i) {\n                return \'<li class="\' + (todo.done ? "done" : "") + \'">\' +\n                    \'<input type="checkbox" \' + (todo.done ? "checked" : "") + \' onchange="toggle(\' + i + \')">\' +\n                    \'<span onclick="toggle(\' + i + \')">\' + todo.text + \'</span>\' +\n                    \'<button onclick="remove(\' + i + \')">删除</button>\' +\n                    \'</li>\';\n            }).join("");\n            const done = todos.filter(function(t) { return t.done; }).length;\n            document.getElementById("stats").textContent = "总计: " + todos.length + " | 已完成: " + done;\n        }\n        \n        function addTodo() {\n            const input = document.getElementById("todoInput");\n            const text = input.value.trim();\n            if (!text) return;\n            todos.push({ text: text, done: false });\n            input.value = "";\n            save(); render();\n        }\n        \n        function toggle(i) {\n            todos[i].done = !todos[i].done;\n            save(); render();\n        }\n        \n        function remove(i) {\n            todos.splice(i, 1);\n            save(); render();\n        }\n        \n        render();\n    </script>\n</body>\n</html>',
    aiReviewPoints: [
      '检查localStorage的读写是否正确',
      '检查数组操作（push、splice、filter）是否正确',
      '检查事件绑定是否合理',
      '建议添加输入验证和空状态提示'
    ]
  },
  {
    id: 12,
    categoryId: 'comprehensive',
    title: '倒计时器',
    difficulty: '简单',
    difficultyType: 'success',
    description: '实现一个倒计时器，用户可以设置分钟数，点击开始后倒计时，支持暂停和重置功能。',
    requirements: [
      '输入框设置倒计时分钟数',
      '显示 MM:SS 格式的倒计时',
      '开始、暂停、重置三个按钮',
      '倒计时结束时弹出提示'
    ],
    language: 'html',
    fileName: 'timer.html',
    initialCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>倒计时器</title>\n    <style>\n        /* 在这里编写样式 */\n        \n    </style>\n</head>\n<body>\n    <div class="timer-app">\n        <h1>倒计时器</h1>\n        <div class="display" id="display">00:00</div>\n        <div class="controls">\n            <input type="number" id="minutes" value="5" min="1">\n            <button onclick="start()">开始</button>\n            <button onclick="pause()">暂停</button>\n            <button onclick="reset()">重置</button>\n        </div>\n    </div>\n    <script>\n        // 在这里编写JavaScript逻辑\n        \n    </script>\n</body>\n</html>',
    referenceCode: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>倒计时器</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #1a1a2e; }\n        .timer-app { text-align: center; color: white; }\n        h1 { margin-bottom: 30px; }\n        .display { font-size: 72px; font-family: monospace; margin-bottom: 30px; background: #16213e; padding: 20px 40px; border-radius: 12px; }\n        .controls { display: flex; gap: 10px; justify-content: center; align-items: center; }\n        .controls input { width: 80px; padding: 10px; border: none; border-radius: 6px; font-size: 16px; text-align: center; }\n        .controls button { padding: 10px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; color: white; }\n        .controls button:nth-child(2) { background: #4caf50; }\n        .controls button:nth-child(3) { background: #ff9800; }\n        .controls button:nth-child(4) { background: #f44336; }\n    </style>\n</head>\n<body>\n    <div class="timer-app">\n        <h1>倒计时器</h1>\n        <div class="display" id="display">05:00</div>\n        <div class="controls">\n            <input type="number" id="minutes" value="5" min="1">\n            <button onclick="start()">开始</button>\n            <button onclick="pause()">暂停</button>\n            <button onclick="reset()">重置</button>\n        </div>\n    </div>\n    <script>\n        let totalSeconds = 300;\n        let remaining = 300;\n        let timer = null;\n        \n        function updateDisplay() {\n            const m = String(Math.floor(remaining / 60)).padStart(2, "0");\n            const s = String(remaining % 60).padStart(2, "0");\n            document.getElementById("display").textContent = m + ":" + s;\n        }\n        \n        function start() {\n            if (timer) return;\n            const min = parseInt(document.getElementById("minutes").value) || 5;\n            if (remaining <= 0) {\n                totalSeconds = min * 60;\n                remaining = totalSeconds;\n            }\n            timer = setInterval(function() {\n                remaining--;\n                updateDisplay();\n                if (remaining <= 0) {\n                    clearInterval(timer);\n                    timer = null;\n                    alert("时间到！");\n                }\n            }, 1000);\n        }\n        \n        function pause() {\n            clearInterval(timer);\n            timer = null;\n        }\n        \n        function reset() {\n            pause();\n            const min = parseInt(document.getElementById("minutes").value) || 5;\n            totalSeconds = min * 60;\n            remaining = totalSeconds;\n            updateDisplay();\n        }\n        \n        updateDisplay();\n    </script>\n</body>\n</html>',
    aiReviewPoints: [
      '检查setInterval和clearInterval的使用',
      '检查时间计算逻辑是否正确（分秒转换）',
      '检查padStart补零的使用',
      '建议添加倒计时结束的视觉反馈'
    ]
  }
]
