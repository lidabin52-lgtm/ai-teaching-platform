/**
 * 课程数据
 * 包含所有课程的详细知识内容
 */

export const coursesList = [
  {
    id: 1,
    icon: '🌐',
    title: 'HTML基础',
    difficulty: '青铜段位',
    tagType: 'warning',
    challenges: 5,
    startChallengeId: 1,
    sections: [
      {
        title: 'HTML是什么？',
        content: '## HTML简介\n\n**HTML**（HyperText Markup Language，超文本标记语言）是构建网页的标准语言。它不是编程语言，而是一种**标记语言**，用标签来描述网页的结构和内容。\n\n### HTML的作用\n- 定义网页的**结构**和**内容**\n- 使用标签告诉浏览器如何显示内容\n- 是所有网页的基础\n\n### 第一个HTML页面\n一个最简单的HTML页面只需要几个基本标签：',
        codeTitle: '最简单的HTML页面',
        codeExample: '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>我的第一个网页</title>\n</head>\n<body>\n    <h1>Hello World！</h1>\n    <p>这是我用HTML写的第一个网页。</p>\n</body>\n</html>',
        keyPoints: [
          '<!DOCTYPE html> 声明文档类型为HTML5',
          '<html> 是根元素，包含整个页面',
          '<head> 存放页面元信息（标题、字符编码等）',
          '<body> 存放页面可见内容',
          '<title> 定义浏览器标签页显示的标题',
        ],
        practiceTip: '尝试修改上面的代码，把"Hello World"改成你自己的名字，看看页面会发生什么变化。'
      },
      {
        title: '常用文本标签',
        content: '## 文本标签\n\nHTML提供了丰富的标签来组织和格式化文本内容。\n\n### 标题标签\nHTML有6级标题，从h1到h6，h1最大，h6最小。\n\n### 段落和换行\n- <p> 定义段落\n- <br> 强制换行\n- <hr> 水平分割线\n\n### 文本格式化\n- <strong> 或 <b>：加粗\n- <em> 或 <i>：斜体\n- <mark>：高亮\n- <code>：行内代码\n- <del>：删除线',
        codeTitle: '文本标签示例',
        codeExample: '<h1>一级标题</h1>\n<h2>二级标题</h2>\n<h3>三级标题</h3>\n\n<p>这是一个<strong>加粗</strong>的文本。</p>\n<p>这是一个<em>斜体</em>的文本。</p>\n<p>这是<mark>高亮显示</mark>的文本。</p>\n<p>使用<code>console.log()</code>输出内容。</p>\n\n<hr>\n\n<p>第一段内容</p>\n<p>第二段内容</p>',
        keyPoints: [
          '标题标签从h1到h6，重要性递减',
          '一个页面通常只有一个h1',
          'strong表示语义上的重要，em表示语气上的强调',
          'mark用于高亮需要用户注意的内容',
        ],
        practiceTip: '创建一个包含多级标题和格式化文本的自我介绍页面。'
      },
      {
        title: '链接与图片',
        content: '## 超链接\n\n<a>标签用于创建超链接，可以跳转到其他页面或网站。\n\n### 常用属性\n- **href**：链接目标URL\n- **target**：打开方式（_blank=新窗口）\n\n## 图片\n\n<img>标签用于嵌入图片。\n\n### 常用属性\n- **src**：图片地址\n- **alt**：替代文本（图片无法显示时）\n- **width/height**：尺寸',
        codeTitle: '链接和图片示例',
        codeExample: '<!-- 超链接 -->\n<a href="https://www.example.com">点击访问</a>\n<a href="https://www.example.com" target="_blank">新窗口打开</a>\n\n<!-- 图片 -->\n<img src="https://picsum.photos/300/200" alt="示例图片" width="300">\n\n<!-- 图片链接（点击图片跳转） -->\n<a href="https://www.example.com" target="_blank">\n    <img src="https://picsum.photos/300/200" alt="可点击的图片">\n</a>',
        keyPoints: [
          'href属性指定链接目标，可以是URL或页面锚点',
          'target="_blank"让链接在新标签页打开',
          'alt属性很重要：图片加载失败时显示，也有助于SEO和无障碍访问',
          'img是自闭合标签，不需要结束标签',
        ],
        practiceTip: '创建一个包含3个链接和2张图片的导航页面。'
      },
      {
        title: '表格与表单',
        content: '## 表格\n\n表格用<table>标签创建，包含表头（<thead>）和表体（<tbody>）。\n\n### 表格标签\n- <table>：表格容器\n- <tr>：表格行\n- <th>：表头单元格（加粗居中）\n- <td>：普通单元格\n\n## 表单\n\n表单用<form>标签创建，用于收集用户输入。\n\n### 常用输入类型\n- text：单行文本\n- password：密码\n- email：邮箱\n- number：数字\n- radio：单选按钮\n- checkbox：复选框\n- submit：提交按钮',
        codeTitle: '表格和表单示例',
        codeExample: '<!-- 表格 -->\n<table border="1">\n  <thead>\n    <tr><th>姓名</th><th>年龄</th><th>城市</th></tr>\n  </thead>\n  <tbody>\n    <tr><td>张三</td><td>25</td><td>北京</td></tr>\n    <tr><td>李四</td><td>30</td><td>上海</td></tr>\n  </tbody>\n</table>\n\n<!-- 表单 -->\n<form>\n  <label>用户名：</label>\n  <input type="text" placeholder="请输入用户名">\n  <br><br>\n  <label>密码：</label>\n  <input type="password" placeholder="请输入密码">\n  <br><br>\n  <label>性别：</label>\n  <input type="radio" name="gender" value="male"> 男\n  <input type="radio" name="gender" value="female"> 女\n  <br><br>\n  <button type="submit">提交</button>\n</form>',
        keyPoints: [
          '表格由table > tr > th/td嵌套组成',
          'th默认加粗居中，td是普通单元格',
          '表单input的type属性决定输入类型',
          'radio通过相同的name属性实现单选互斥',
        ],
        practiceTip: '创建一个包含表格的学生信息展示页面，以及一个注册表单。'
      },
      {
        title: '语义化标签',
        content: '## 什么是语义化？\n\n语义化是指使用**有意义的HTML标签**来描述内容的含义，而不是只用div和span。\n\n### 为什么需要语义化？\n1. **可读性**：代码更易理解\n2. **SEO**：搜索引擎更好地理解页面\n3. **无障碍**：屏幕阅读器更好地辅助视障用户\n4. **维护性**：结构清晰，便于修改\n\n### 常用语义化标签\n- header：页面头部\n- nav：导航链接\n- main：主要内容\n- article：独立内容块\n- section：内容分组\n- aside：侧边栏\n- footer：页面底部',
        codeTitle: '语义化标签示例',
        codeExample: '<header>\n  <nav>\n    <a href="/">首页</a>\n    <a href="/about">关于</a>\n  </nav>\n</header>\n\n<main>\n  <article>\n    <h1>文章标题</h1>\n    <p>发布时间：<time>2024-01-01</time></p>\n    <section>\n      <h2>第一节</h2>\n      <p>内容...</p>\n    </section>\n  </article>\n  <aside>\n    <h3>相关推荐</h3>\n    <ul><li>推荐文章1</li><li>推荐文章2</li></ul>\n  </aside>\n</main>\n\n<footer>\n  <p>版权所有 2024</p>\n</footer>',
        keyPoints: [
          'header：页面头部，通常包含导航',
          'nav：导航链接区域',
          'main：页面主要内容（每个页面只有一个）',
          'article：独立的内容块（如文章）',
          'section：内容的分组/分节',
          'footer：页面底部',
        ],
        practiceTip: '用语义化标签重构你之前写的页面，替换掉所有的div。'
      }
    ]
  },
  {
    id: 2,
    icon: '🎨',
    title: 'CSS样式',
    difficulty: '白银段位',
    tagType: '',
    challenges: 4,
    startChallengeId: 6,
    sections: [
      {
        title: 'CSS基础与选择器',
        content: '## CSS是什么？\n\n**CSS**（Cascading Style Sheets，层叠样式表）用于控制网页的**外观和布局**。\n\n### 三种引入方式\n1. **行内样式**：写在标签的style属性中\n2. **内部样式表**：写在<style>标签中\n3. **外部样式表**：通过<link>引入.css文件（推荐）\n\n### CSS选择器\n选择器用于选中要添加样式的HTML元素。',
        codeTitle: 'CSS选择器示例',
        codeExample: '/* 元素选择器 - 选中所有p标签 */\np {\n    color: blue;\n    font-size: 16px;\n}\n\n/* 类选择器 - 选中class="intro"的元素 */\n.intro {\n    background-color: #f0f0f0;\n    padding: 10px;\n}\n\n/* ID选择器 - 选中id="header"的元素 */\n#header {\n    background: #333;\n    color: white;\n}\n\n/* 后代选择器 - div内的所有span */\ndiv span {\n    color: red;\n}\n\n/* 伪类选择器 - 鼠标悬停效果 */\na:hover {\n    color: orange;\n}',
        keyPoints: [
          '元素选择器直接用标签名',
          '类选择器用 . 开头，ID选择器用 # 开头',
          '后代选择器用空格分隔',
          '优先级：ID > 类 > 元素',
        ],
        practiceTip: '为一个HTML页面添加不同的CSS样式，体验各种选择器的效果。'
      },
      {
        title: '盒模型',
        content: '## 什么是盒模型？\n\n每个HTML元素都可以看作一个"盒子"，由4层组成：\n\n- **Content**（内容）：元素的实际内容\n- **Padding**（内边距）：内容与边框之间的空间\n- **Border**（边框）：围绕内边距的线\n- **Margin**（外边距）：边框与其他元素之间的空间\n\n### box-sizing\n- content-box（默认）：width只包含内容\n- border-box（推荐）：width包含padding和border',
        codeTitle: '盒模型示例',
        codeExample: '.box {\n    width: 200px;\n    height: 100px;\n    padding: 20px;\n    border: 2px solid #333;\n    margin: 30px auto;\n    box-sizing: border-box;\n    background: #f5f5f5;\n}',
        keyPoints: [
          '盒模型从内到外：content > padding > border > margin',
          'border-box让设置宽高更直观（推荐使用）',
          'margin可以为负值，实现元素重叠效果',
          'padding不能为负值',
        ],
        practiceTip: '创建两个盒子，一个用content-box，一个用border-box，设置相同的width和padding，对比它们的实际大小。'
      },
      {
        title: 'Flexbox布局',
        content: '## Flex布局\n\nFlexbox是一种**一维布局模型**，可以轻松实现各种对齐和分布效果。\n\n### 容器属性（设在父元素上）\n- display: flex：启用Flex布局\n- flex-direction：主轴方向\n- justify-content：主轴对齐\n- align-items：交叉轴对齐\n- flex-wrap：是否换行\n\n### 项目属性（设在子元素上）\n- flex: 1：平均分配空间\n- align-self：单独对齐',
        codeTitle: 'Flex布局示例',
        codeExample: '.container {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    height: 300px;\n    gap: 10px;\n}\n\n.item {\n    flex: 1;\n    height: 100px;\n    background: #409eff;\n    color: white;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n}',
        keyPoints: [
          'display: flex 启用弹性布局',
          'justify-content 控制主轴（水平）对齐',
          'align-items 控制交叉轴（垂直）对齐',
          'flex: 1 让子元素平均分配空间',
          'gap 设置子元素之间的间距',
        ],
        practiceTip: '用Flex布局实现一个水平导航栏和一个垂直居中的登录框。'
      },
      {
        title: '定位与层叠',
        content: '## CSS定位\n\nposition属性控制元素的定位方式：\n\n- **static**（默认）：正常文档流\n- **relative**：相对定位，相对自身原位置偏移\n- **absolute**：绝对定位，相对最近的非static祖先\n- **fixed**：固定定位，相对浏览器窗口\n- **sticky**：粘性定位，滚动到阈值时固定\n\n### z-index\n当元素重叠时，z-index值越大越在上面。',
        codeTitle: '定位示例',
        codeExample: '.parent {\n    position: relative;\n    width: 300px;\n    height: 200px;\n    background: #f0f0f0;\n}\n\n.child1 {\n    position: absolute;\n    top: 10px;\n    left: 10px;\n    z-index: 2;\n}\n\n.child2 {\n    position: absolute;\n    top: 20px;\n    left: 20px;\n    z-index: 1;\n}\n\n.fixed-bar {\n    position: fixed;\n    bottom: 0;\n    left: 0;\n    right: 0;\n    background: #333;\n    color: white;\n    padding: 10px;\n    z-index: 100;\n}',
        keyPoints: [
          'absolute定位的元素脱离文档流',
          'absolute相对于最近的relative/absolute/fixed祖先定位',
          'fixed始终相对于浏览器窗口定位',
          'z-index只在定位元素（非static）之间生效',
        ],
        practiceTip: '创建一个固定在页面底部的工具栏，以及一个相对定位容器内的绝对定位元素。'
      }
    ]
  },
  {
    id: 3,
    icon: '⚡',
    title: 'JavaScript基础',
    difficulty: '黄金段位',
    tagType: 'success',
    challenges: 3,
    startChallengeId: 10,
    sections: [
      {
        title: '变量与数据类型',
        content: '## 变量声明\n\nJavaScript有三种声明变量的方式：\n\n- var：旧方式，函数作用域（不推荐）\n- let：块级作用域，可重新赋值\n- const：块级作用域，不可重新赋值（推荐用于常量）\n\n## 基本数据类型\n- string：字符串\n- number：数字\n- boolean：布尔值\n- null：空值\n- undefined：未定义\n- object：对象\n- array：数组',
        codeTitle: '变量与数据类型',
        codeExample: '// 变量声明\nconst name = "张三";\nconst age = 25;\nconst isStudent = true;\nconst hobbies = ["编程", "音乐", "运动"];\nconst info = { name: "张三", age: 25 };\n\n// 模板字符串\nconst greeting = "你好，" + name + "！今年" + age + "岁。";\n\n// 解构赋值\nconst userName = info.name;\nconst first = hobbies[0];',
        keyPoints: [
          '优先使用const，需要重新赋值时用let，避免使用var',
          '模板字符串用反引号，支持变量插值',
          '解构赋值可以快速提取对象和数组的值',
          'typeof可以检测数据类型',
        ],
        practiceTip: '创建一个包含各种数据类型的变量，并用console.log()输出它们的类型。'
      },
      {
        title: 'DOM操作',
        content: '## 什么是DOM？\n\n**DOM**（Document Object Model，文档对象模型）是HTML文档的编程接口。JavaScript通过DOM可以：\n- 获取页面元素\n- 修改内容和样式\n- 添加和删除元素\n- 响应用户事件\n\n### 获取元素\n- document.getElementById("id")\n- document.querySelector(".class")\n- document.querySelectorAll("div")',
        codeTitle: 'DOM操作示例',
        codeExample: '// 获取元素\nconst title = document.getElementById("title");\nconst items = document.querySelectorAll(".item");\n\n// 修改内容和样式\ntitle.textContent = "新标题";\ntitle.style.color = "red";\ntitle.classList.add("active");\ntitle.classList.toggle("hidden");\n\n// 创建和添加元素\nconst newDiv = document.createElement("div");\nnewDiv.textContent = "新创建的元素";\nnewDiv.classList.add("item");\ndocument.body.appendChild(newDiv);\n\n// 删除元素\nconst oldItem = document.querySelector(".old");\noldItem.remove();',
        keyPoints: [
          'querySelector用CSS选择器语法，更灵活',
          'textContent修改纯文本，innerHTML修改HTML',
          'classList.add/remove/toggle操作类名',
          'createElement + appendChild 创建并添加元素',
        ],
        practiceTip: '创建一个按钮，点击后动态添加一个包含文字的新div到页面中。'
      },
      {
        title: '事件处理',
        content: '## 事件监听\n\n使用addEventListener为元素绑定事件处理函数。\n\n### 常用事件\n- click：点击\n- input：输入内容变化\n- submit：表单提交\n- keydown/keyup：键盘按下/松开\n- mouseover/mouseout：鼠标移入/移出\n\n### 事件对象\n事件处理函数接收一个event对象，包含事件信息。',
        codeTitle: '事件处理示例',
        codeExample: 'const btn = document.getElementById("myBtn");\nconst input = document.getElementById("myInput");\nconst form = document.getElementById("myForm");\n\n// 点击事件\nbtn.addEventListener("click", function(event) {\n    console.log("按钮被点击了！");\n});\n\n// 输入事件（实时监听）\ninput.addEventListener("input", function() {\n    console.log("当前值:", this.value);\n});\n\n// 表单提交事件\nform.addEventListener("submit", function(event) {\n    event.preventDefault(); // 阻止默认提交\n    console.log("表单已提交");\n});',
        keyPoints: [
          'addEventListener比onclick更灵活（可绑定多个）',
          'event.preventDefault()阻止默认行为',
          'event.stopPropagation()阻止事件冒泡',
          '事件委托利用冒泡机制，减少事件绑定数量',
        ],
        practiceTip: '创建一个表单，实现实时输入验证：用户名至少3个字符，密码至少6个字符。'
      }
    ]
  },
  {
    id: 4,
    icon: '💎',
    title: '综合应用',
    difficulty: '钻石段位',
    tagType: 'info',
    challenges: 2,
    startChallengeId: 13,
    sections: [
      {
        title: '项目实战思路',
        content: '## 综合应用\n\n到了这个阶段，你需要将HTML、CSS、JavaScript三件套**综合运用**来完成实际项目。\n\n### 开发流程\n1. **分析需求**：明确要实现的功能\n2. **设计结构**：规划HTML结构\n3. **编写样式**：CSS实现视觉效果\n4. **添加交互**：JavaScript实现动态功能\n5. **测试优化**：检查兼容性和用户体验',
        codeTitle: '待办事项应用核心逻辑',
        codeExample: '// 数据存储\nlet todos = JSON.parse(localStorage.getItem("todos")) || [];\n\n// 渲染列表\nfunction renderTodos() {\n    const list = document.getElementById("todoList");\n    list.innerHTML = todos.map(function(todo, i) {\n        return "<li class=\"" + (todo.done ? "done" : "") + "\">"\n            + "<input type=\"checkbox\" " + (todo.done ? "checked" : "")\n            + " onchange=\"toggleTodo(" + i + ")\">"\n            + "<span>" + todo.text + "</span>"\n            + "<button onclick=\"deleteTodo(" + i + ")\">删除</button>"\n            + "</li>";\n    }).join("");\n    localStorage.setItem("todos", JSON.stringify(todos));\n}\n\n// 添加待办\nfunction addTodo(text) {\n    todos.push({ text: text, done: false });\n    renderTodos();\n}',
        keyPoints: [
          'localStorage实现数据持久化',
          '数组方法map/filter/splice是核心操作',
          '函数封装提高代码复用性',
          '先规划结构，再写样式，最后加交互',
        ],
        practiceTip: '完成钻石段位的两个闯关项目：待办事项应用和图片轮播组件。'
      }
    ]
  },
  {
    id: 5,
    icon: '👑',
    title: '王者挑战',
    difficulty: '王者段位',
    tagType: 'danger',
    challenges: 1,
    startChallengeId: 15,
    sections: [
      {
        title: '王者之路',
        content: '## 终极挑战\n\n王者段位只有一个关卡：**独立完成一个个人作品集网站**。\n\n这个项目需要你综合运用所有学到的知识：\n\n### 技术要求\n- HTML5语义化标签\n- CSS响应式设计\n- Flexbox/Grid布局\n- JavaScript交互效果\n- 固定导航栏\n- 平滑滚动\n- 表单验证\n\n### 设计要求\n- 统一的配色方案\n- 适配手机和桌面端\n- 流畅的动画效果\n- 代码整洁有注释',
        codeTitle: '项目结构参考',
        codeExample: '<!-- 推荐的页面结构 -->\n<nav>         <!-- 固定导航 -->\n  <a href="#hero">首页</a>\n  <a href="#works">作品</a>\n  <a href="#about">关于</a>\n  <a href="#contact">联系</a>\n</nav>\n\n<section id="hero">   <!-- 全屏英雄区 -->\n  <h1>你的名字</h1>\n  <p>前端开发者</p>\n</section>\n\n<section id="works">  <!-- 作品展示 Grid布局 -->\n  <div class="grid">\n    <div class="card">作品1</div>\n    <div class="card">作品2</div>\n    <div class="card">作品3</div>\n  </div>\n</section>\n\n<section id="about">  <!-- 关于我 两栏布局 -->\n  <div class="flex">\n    <img src="photo.jpg">\n    <div>详细介绍...</div>\n  </div>\n</section>\n\n<section id="contact"> <!-- 联系表单 -->\n  <form>表单内容...</form>\n</section>',
        keyPoints: [
          '先规划结构，再写样式，最后加交互',
          '使用CSS变量统一管理配色',
          '移动端优先的响应式设计',
          '代码注释让项目更专业',
        ],
        practiceTip: '不要急于写代码，先在纸上画出页面布局草图，然后逐步实现每个区域。'
      }
    ]
  },
  {
    id: 6,
    icon: '🤖',
    title: 'AI辅助学习',
    difficulty: '全段位',
    tagType: '',
    challenges: 0,
    startChallengeId: 0,
    sections: [
      {
        title: 'AI导师使用指南',
        content: '## 你的AI编程导师\n\n在闯关过程中，你可以随时呼叫AI导师来帮助你解决编程问题。\n\n### AI导师能做什么？\n- **知识讲解**：解释HTML/CSS/JS概念\n- **代码调试**：帮你找出代码中的错误\n- **思路引导**：不直接给答案，引导你思考\n- **代码审查**：评价你的代码质量\n- **知识拓展**：推荐相关学习资源\n\n### 如何提问更有效？\n1. 描述你**想实现什么效果**\n2. 说明你**已经尝试了什么**\n3. 贴出你的**相关代码**\n4. 说明你遇到了**什么错误**',
        codeTitle: '提问示例',
        codeExample: '// 不好的提问\n"代码不工作"\n\n// 好的提问\n"我在做Flex布局练习，想让三个div水平居中。\n我用了display:flex和justify-content:center，\n但是div之间没有间距。请问怎么设置元素之间的间距？"\n\n// 带代码的提问\n"我的表格代码如下，但是边框没有显示出来：\n<table>\n  <tr><td>内容</td></tr>\n</table>\n请问是什么原因？"',
        keyPoints: [
          '具体描述问题比笼统提问更有效',
          '贴出代码和错误信息帮助AI定位问题',
          'AI导师会引导你思考，而不是直接给答案',
          '善用AI导师，但不要过度依赖',
        ],
        practiceTip: '在闯关过程中遇到问题时，先自己思考5分钟，再呼叫AI导师。'
      }
    ]
  }
]
