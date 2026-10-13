"""
AI服务层 - 封装所有与DeepSeek API的交互逻辑

包含三个核心功能：
1. CodeJudge - 代码审判官：评估学生代码，返回星级评分
2. ChallengeGenerator - 关卡生成器：自动生成闯关题目
3. AIMentor - AI导师：基于RAG的问答助手

作者: AI Teaching Platform
版本: 1.0.0
"""
import json
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

from openai import OpenAI, APIError, RateLimitError, APITimeoutError


# ========== 配置日志 ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ========== 数据类定义 ==========

@dataclass
class JudgmentResult:
    """代码审判结果数据类"""
    function_score: int          # 功能实现度评分 (1-3)
    standard_score: int          # 代码规范度评分 (1-3)
    cool_score: int              # 性能与酷炫度评分 (1-3)
    total_stars: int             # 总星数 (1-3)
    comment: str                 # 详细评语
    hint: str                    # 引导提示
    raw_response: Optional[str] = None  # 原始AI响应
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'function_score': self.function_score,
            'standard_score': self.standard_score,
            'cool_score': self.cool_score,
            'total_stars': self.total_stars,
            'comment': self.comment,
            'hint': self.hint,
        }


@dataclass
class ChallengeTemplate:
    """生成的关卡模板数据类"""
    title: str                   # 关卡标题
    description: str             # 需求描述（Markdown）
    starter_code: str            # 初始脚手架代码
    scoring_criteria: Dict       # 审判标准JSON
    ai_prompt: str               # AI审判提示词
    expected_output: str         # 期望输出描述
    difficulty: str              # 段位
    category: str                # 分类
    tags: List[str]              # 标签
    time_limit: int              # 时间限制（分钟）
    hint_count: int              # 提示次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'description': self.description,
            'starter_code': self.starter_code,
            'scoring_criteria': self.scoring_criteria,
            'ai_prompt': self.ai_prompt,
            'expected_output': self.expected_output,
            'difficulty': self.difficulty,
            'category': self.category,
            'tags': self.tags,
            'time_limit': self.time_limit,
            'hint_count': self.hint_count,
        }


@dataclass
class MentorResponse:
    """AI导师回复数据类"""
    content: str                 # 回复内容
    referenced_knowledge: List[int]  # 引用的知识库文档ID
    tokens_used: int             # 消耗的token数
    response_time_ms: int        # 响应时间（毫秒）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'content': self.content,
            'referenced_knowledge': self.referenced_knowledge,
            'tokens_used': self.tokens_used,
            'response_time_ms': self.response_time_ms,
        }


# ========== 装饰器：重试机制 ==========

def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """
    重试装饰器
    
    参数:
        max_retries: 最大重试次数
        delay: 重试间隔（秒），每次翻倍
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (APIError, RateLimitError, APITimeoutError) as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"API调用失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}. "
                            f"{current_delay}秒后重试..."
                        )
                        time.sleep(current_delay)
                        current_delay *= 2  # 指数退避
                    else:
                        logger.error(f"API调用失败，已达到最大重试次数: {e}")
                        raise
                except Exception as e:
                    logger.error(f"未预期的错误: {e}")
                    raise
            
            raise last_exception
        return wrapper
    return decorator


# ========== 基础AI服务类 ==========

class BaseAIService:
    """AI服务基类，提供通用的DeepSeek API调用能力"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com", 
                 model: str = "deepseek-chat", timeout: int = 60):
        """
        初始化AI服务
        
        参数:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 使用的模型名称
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        
        # 初始化OpenAI客户端（兼容DeepSeek接口）
        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=f"{self.base_url}/v1",
                timeout=timeout,
            )
            logger.info(f"AI服务初始化成功: {base_url}, 模型: {model}")
        except Exception as e:
            logger.error(f"AI服务初始化失败: {e}")
            raise
    
    @retry_on_error(max_retries=3, delay=1.0)
    def chat_completion(self, messages: List[Dict[str, str]], 
                       temperature: float = 0.7,
                       max_tokens: int = 2000,
                       response_format: Optional[Dict] = None) -> str:
        """
        调用聊天补全API
        
        参数:
            messages: 消息列表
            temperature: 生成温度
            max_tokens: 最大token数
            response_format: 响应格式（如 {"type": "json_object"}）
        
        返回:
            AI生成的文本内容
        """
        start_time = time.time()
        
        try:
            kwargs = {
                'model': self.model,
                'messages': messages,
                'temperature': temperature,
                'max_tokens': max_tokens,
            }
            
            if response_format:
                kwargs['response_format'] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            content = response.choices[0].message.content
            
            logger.info(
                f"API调用成功 | 耗时: {elapsed_ms}ms | "
                f"Tokens: {response.usage.total_tokens if response.usage else 'N/A'}"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"API调用异常: {e}")
            raise
    
    @retry_on_error(max_retries=3, delay=1.0)
    def stream_chat(self, messages: List[Dict[str, str]], 
                   temperature: float = 0.7,
                   max_tokens: int = 2000):
        """
        流式聊天补全（用于AI导师实时回复）
        
        参数:
            messages: 消息列表
            temperature: 生成温度
            max_tokens: 最大token数
        
        返回:
            生成器，产出文本片段
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"流式API调用异常: {e}")
            raise


# ========== 一、代码审判官 ==========

class CodeJudge(BaseAIService):
    """
    代码审判官
    
    从三个维度评估学生代码：
    - 功能实现度：是否完成所有需求
    - 代码规范度：代码风格、可读性
    - 性能与酷炫度：优化程度、创意
    
    返回1-3星评分和详细评语
    """
    
    # 系统提示词模板
    SYSTEM_PROMPT_TEMPLATE = """你是一位严格但富有耐心的Web前端代码审判官。

【你的职责】
评估学生提交的代码，从以下三个维度进行评分：
1. 功能实现度：代码是否完成了关卡的所有需求
2. 代码规范度：代码是否规范、可读、符合最佳实践
3. 性能与酷炫度：代码是否有优化、有创意、有亮点

【评分规则】
每个维度评分1-3分：
- 1分：未达标（功能缺失/代码混乱/无优化）
- 2分：达标（完成功能/代码规范/有基本优化）
- 3分：优秀（超额完成/代码优雅/有创意亮点）

【星级计算】
基础1星 + 规范>=2加1星 + 酷炫>=2加1星 = 总星数（1-3星）

【评语风格】
- 先肯定优点，再指出具体改进点
- 语言亲切，像一位耐心的老师
- 评语控制在200字以内

【输出格式】
必须返回严格的JSON格式，不要有任何其他内容：
{{
  "function_score": 1-3的整数,
  "standard_score": 1-3的整数,
  "cool_score": 1-3的整数,
  "total_stars": 1-3的整数,
  "comment": "详细评语，先肯定后建议，200字以内",
  "hint": "如果功能未完全实现，给一个不直接泄露答案的引导提示；如果已完成，返回空字符串"
}}

【段位调整】
当前学生段位：{difficulty}
- 青铜：标准较宽松，多鼓励
- 白银：标准适中，指出明显问题
- 黄金及以上：标准严格，要求代码质量"""

    # 用户提示词模板
    USER_PROMPT_TEMPLATE = """请评估以下学生代码：

【关卡需求】
{description}

【审判标准】
{scoring_criteria}

【学生段位】
{difficulty}

【学生提交的代码】
```{language}
{code}
```

请严格按照JSON格式返回评分结果。"""

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com",
                 model: str = "deepseek-chat", timeout: int = 60):
        """初始化代码审判官"""
        super().__init__(api_key, base_url, model, timeout)
        logger.info("代码审判官服务初始化完成")
    
    def judge(self, 
              description: str,
              scoring_criteria: Dict,
              code: str,
              difficulty: str = "bronze",
              language: str = "html") -> JudgmentResult:
        """
        审判学生代码
        
        参数:
            description: 关卡需求描述
            scoring_criteria: 审判标准（JSON格式）
            code: 学生提交的代码
            difficulty: 学生段位（bronze/silver/gold/diamond/king）
            language: 代码语言
        
        返回:
            JudgmentResult: 审判结果
        """
        logger.info(f"开始审判代码 | 段位: {difficulty} | 语言: {language}")
        
        # 构建提示词
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(difficulty=self._get_difficulty_label(difficulty))
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            description=description,
            scoring_criteria=json.dumps(scoring_criteria, ensure_ascii=False, indent=2),
            difficulty=self._get_difficulty_label(difficulty),
            language=language,
            code=code
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # 调用API，要求JSON格式响应
            response = self.chat_completion(
                messages=messages,
                temperature=0.3,  # 低温度，更确定性
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            result = self._parse_judgment_response(response)
            result.raw_response = response
            
            logger.info(
                f"审判完成 | 功能:{result.function_score} 规范:{result.standard_score} "
                f"酷炫:{result.cool_score} | 总星数:{result.total_stars}"
            )
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}\n原始响应: {response}")
            # 返回默认评分
            return self._get_default_judgment()
        except Exception as e:
            logger.error(f"审判过程异常: {e}")
            return self._get_default_judgment()
    
    def _parse_judgment_response(self, response: str) -> JudgmentResult:
        """解析AI返回的JSON响应"""
        try:
            data = json.loads(response)
            
            # 计算总星数（如果AI没有正确计算）
            total_stars = data.get('total_stars', 1)
            if 'function_score' in data and 'standard_score' in data and 'cool_score' in data:
                calculated_stars = 1
                if data.get('standard_score', 0) >= 2:
                    calculated_stars += 1
                if data.get('cool_score', 0) >= 2:
                    calculated_stars += 1
                total_stars = min(calculated_stars, 3)
            
            return JudgmentResult(
                function_score=int(data.get('function_score', 2)),
                standard_score=int(data.get('standard_score', 2)),
                cool_score=int(data.get('cool_score', 2)),
                total_stars=total_stars,
                comment=data.get('comment', '代码评估完成'),
                hint=data.get('hint', ''),
            )
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.error(f"解析审判结果失败: {e}")
            raise
    
    def _get_default_judgment(self) -> JudgmentResult:
        """获取默认审判结果（API失败时使用）"""
        return JudgmentResult(
            function_score=2,
            standard_score=2,
            cool_score=1,
            total_stars=2,
            comment="代码已提交，系统正在评估中。请稍后查看详细结果。",
            hint="建议检查代码是否满足所有需求点。",
        )
    
    def _get_difficulty_label(self, difficulty: str) -> str:
        """获取段位中文标签"""
        labels = {
            'bronze': '青铜',
            'silver': '白银',
            'gold': '黄金',
            'diamond': '钻石',
            'king': '王者'
        }
        return labels.get(difficulty.lower(), '青铜')


# ========== 二、关卡生成器 ==========

class ChallengeGenerator(BaseAIService):
    """
    关卡生成器
    
    根据教师指定的知识点和难度，自动生成闯关题目
    """
    
    # 系统提示词模板
    SYSTEM_PROMPT_TEMPLATE = """你是一位专业的Web前端课程设计师。

【你的职责】
根据教师指定的知识点和难度，设计一个完整的技能闯关关卡。

【关卡设计要求】
1. 标题简洁明了，能激发学习兴趣
2. 需求描述使用Markdown格式，包含：
   - 🎯 任务目标
   - 📋 具体要求（编号列表）
   - 💡 提示（可选）
   - ✅ 验收标准
3. 初始脚手架代码要合理，留出需要学生填写的部分
4. 审判标准要明确、可量化

【输出格式】
必须返回严格的JSON格式：
{{
  "title": "关卡标题",
  "description": "Markdown格式的需求描述",
  "starter_code": "初始代码模板",
  "scoring_criteria": {{
    "correctness": 40,
    "code_quality": 30,
    "best_practice": 20,
    "creativity": 10
  }},
  "ai_prompt": "AI审判时使用的系统提示词",
  "expected_output": "期望输出描述",
  "category": "分类（HTML/CSS/JavaScript等）",
  "tags": ["标签1", "标签2"],
  "time_limit": 30,
  "hint_count": 3
}}"""

    # 用户提示词模板
    USER_PROMPT_TEMPLATE = """请设计一个闯关关卡：

【知识点】
{knowledge_point}

【目标段位】
{difficulty}

【希望考察的技能点】
{skills}

【关卡序号】
第 {order_num} 关（同段位内）

请生成完整的关卡内容，包括标题、需求描述、初始代码、审判标准等。"""

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com",
                 model: str = "deepseek-chat", timeout: int = 60):
        """初始化关卡生成器"""
        super().__init__(api_key, base_url, model, timeout)
        logger.info("关卡生成器服务初始化完成")
    
    def generate(self,
                 knowledge_point: str,
                 difficulty: str,
                 skills: List[str],
                 order_num: int = 1) -> ChallengeTemplate:
        """
        生成关卡
        
        参数:
            knowledge_point: 知识点名称（如"CSS Flexbox布局"）
            difficulty: 目标段位（bronze/silver/gold/diamond/king）
            skills: 希望考察的技能点列表
            order_num: 关卡序号（同段位内）
        
        返回:
            ChallengeTemplate: 生成的关卡模板
        """
        logger.info(f"开始生成关卡 | 知识点: {knowledge_point} | 段位: {difficulty}")
        
        # 构建提示词
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            knowledge_point=knowledge_point,
            difficulty=self._get_difficulty_label(difficulty),
            skills='、'.join(skills),
            order_num=order_num
        )
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT_TEMPLATE},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.chat_completion(
                messages=messages,
                temperature=0.7,  # 适中温度，保持创意
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            template = self._parse_challenge_response(response, difficulty)
            
            logger.info(f"关卡生成完成 | 标题: {template.title}")
            return template
            
        except Exception as e:
            logger.error(f"关卡生成失败: {e}")
            return self._get_default_challenge(knowledge_point, difficulty)
    
    def _parse_challenge_response(self, response: str, difficulty: str) -> ChallengeTemplate:
        """解析AI返回的关卡JSON"""
        try:
            data = json.loads(response)
            
            return ChallengeTemplate(
                title=data.get('title', '未命名关卡'),
                description=data.get('description', '暂无描述'),
                starter_code=data.get('starter_code', ''),
                scoring_criteria=data.get('scoring_criteria', {
                    'correctness': 40,
                    'code_quality': 30,
                    'best_practice': 20,
                    'creativity': 10
                }),
                ai_prompt=data.get('ai_prompt', ''),
                expected_output=data.get('expected_output', ''),
                difficulty=difficulty,
                category=data.get('category', 'Other'),
                tags=data.get('tags', []),
                time_limit=data.get('time_limit', 30),
                hint_count=data.get('hint_count', 3),
            )
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"解析关卡数据失败: {e}")
            raise
    
    def _get_default_challenge(self, knowledge_point: str, difficulty: str) -> ChallengeTemplate:
        """获取默认关卡（生成失败时使用）"""
        return ChallengeTemplate(
            title=f"{knowledge_point}基础练习",
            description=f"## 🎯 任务目标\n练习{knowledge_point}的基础用法。\n\n## 📋 具体要求\n1. 完成基础代码编写\n2. 确保代码可正常运行\n\n## ✅ 验收标准\n- 代码结构正确\n- 功能实现完整",
            starter_code="<!-- 请在此编写你的代码 -->\n",
            scoring_criteria={
                'correctness': 40,
                'code_quality': 30,
                'best_practice': 20,
                'creativity': 10
            },
            ai_prompt="评估代码的正确性和规范性",
            expected_output="正确的代码实现",
            difficulty=difficulty,
            category='Other',
            tags=['基础'],
            time_limit=30,
            hint_count=3,
        )
    
    def _get_difficulty_label(self, difficulty: str) -> str:
        """获取段位中文标签"""
        labels = {
            'bronze': '青铜（入门）',
            'silver': '白银（基础）',
            'gold': '黄金（进阶）',
            'diamond': '钻石（高级）',
            'king': '王者（专家）'
        }
        return labels.get(difficulty.lower(), '青铜')


# ========== 三、AI导师 ==========

class AIMentor(BaseAIService):
    """
    AI导师
    
    基于RAG增强的问答助手，回答学生关于前端学习的问题
    """
    
    # 系统提示词模板（包含知识库内容）
    SYSTEM_PROMPT_TEMPLATE = """你是Web前端学习助手"小智老师"。

【你的角色】
- 耐心、专业的前端教学助手
- 善于用简单易懂的方式解释复杂概念
- 会结合具体代码示例进行讲解

【回答原则】
1. 基于提供的知识库内容回答问题，不编造不确定的信息
2. 如果知识库没有相关答案，建议学生完成更多闯关练习来探索
3. 回答要简洁明了，必要时提供代码示例
4. 鼓励学生独立思考，不直接给出完整答案

【知识库内容】
{knowledge_base}

【当前关卡上下文】
{challenge_context}

【注意事项】
- 如果学生问的是当前关卡相关的问题，结合关卡需求给出针对性建议
- 如果问题超出知识库范围，诚实告知并建议学习路径
- 保持友好、鼓励的语气"""

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com",
                 model: str = "deepseek-chat", timeout: int = 60,
                 knowledge_base: Optional[List[Dict]] = None):
        """
        初始化AI导师
        
        参数:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 模型名称
            timeout: 超时时间
            knowledge_base: 知识库内容列表（用于RAG）
        """
        super().__init__(api_key, base_url, model, timeout)
        self.knowledge_base = knowledge_base or []
        self.conversation_history: Dict[int, List[Dict]] = {}  # 用户ID -> 历史记录
        self.max_history = 5  # 保留最近5轮对话
        logger.info(f"AI导师服务初始化完成 | 知识库文档数: {len(self.knowledge_base)}")
    
    def chat(self, 
             user_id: int,
             message: str,
             challenge_context: Optional[Dict] = None,
             stream: bool = False) -> MentorResponse:
        """
        与学生对话
        
        参数:
            user_id: 学生用户ID
            message: 学生消息
            challenge_context: 当前关卡上下文（可选）
            stream: 是否使用流式响应
        
        返回:
            MentorResponse: 导师回复
        """
        start_time = time.time()
        logger.info(f"AI导师对话 | 用户: {user_id} | 消息: {message[:50]}...")
        
        # 构建知识库文本
        kb_text = self._build_knowledge_base_text()
        
        # 构建关卡上下文
        challenge_text = self._build_challenge_context(challenge_context)
        
        # 构建系统提示词
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(
            knowledge_base=kb_text,
            challenge_context=challenge_text
        )
        
        # 构建消息列表（含历史记录）
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史记录
        history = self._get_conversation_history(user_id)
        messages.extend(history)
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        try:
            if stream:
                # 流式响应（用于实时显示）
                return self._handle_stream_response(user_id, messages, start_time)
            else:
                # 普通响应
                response = self.chat_completion(
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                elapsed_ms = int((time.time() - start_time) * 1000)
                
                # 更新历史记录
                self._update_conversation_history(user_id, message, response)
                
                # 识别引用的知识库
                referenced_kb = self._identify_referenced_knowledge(response)
                
                result = MentorResponse(
                    content=response,
                    referenced_knowledge=referenced_kb,
                    tokens_used=0,  # 流式响应无法获取准确token数
                    response_time_ms=elapsed_ms
                )
                
                logger.info(f"AI导师回复完成 | 耗时: {elapsed_ms}ms")
                return result
                
        except Exception as e:
            logger.error(f"AI导师对话异常: {e}")
            return MentorResponse(
                content="抱歉，我暂时无法回答。请稍后再试，或尝试完成更多闯关练习来探索答案。",
                referenced_knowledge=[],
                tokens_used=0,
                response_time_ms=int((time.time() - start_time) * 1000)
            )
    
    def _handle_stream_response(self, user_id: int, messages: List[Dict], 
                                start_time: float):
        """处理流式响应"""
        # 流式响应返回生成器
        full_content = []
        
        for chunk in self.stream_chat(messages, temperature=0.7, max_tokens=2000):
            full_content.append(chunk)
            yield chunk
        
        # 流结束后更新历史
        complete_response = ''.join(full_content)
        self._update_conversation_history(user_id, messages[-1]['content'], complete_response)
    
    def _build_knowledge_base_text(self) -> str:
        """构建知识库文本（用于RAG）"""
        if not self.knowledge_base:
            return "（知识库为空）"
        
        kb_parts = []
        for doc in self.knowledge_base[:5]:  # 只取前5篇最相关的
            kb_parts.append(f"【{doc.get('title', '未命名')}】\n{doc.get('content', '')[:500]}...")
        
        return '\n\n'.join(kb_parts)
    
    def _build_challenge_context(self, challenge_context: Optional[Dict]) -> str:
        """构建关卡上下文文本"""
        if not challenge_context:
            return "（当前不在任何关卡中）"
        
        return f"""关卡: {challenge_context.get('title', '未知')}
需求: {challenge_context.get('description', '无')[:200]}..."""
    
    def _get_conversation_history(self, user_id: int) -> List[Dict]:
        """获取用户的对话历史"""
        history = self.conversation_history.get(user_id, [])
        # 只取最近max_history轮
        return history[-self.max_history * 2:] if history else []
    
    def _update_conversation_history(self, user_id: int, user_msg: str, assistant_msg: str):
        """更新对话历史"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({"role": "user", "content": user_msg})
        self.conversation_history[user_id].append({"role": "assistant", "content": assistant_msg})
        
        # 限制历史长度
        if len(self.conversation_history[user_id]) > self.max_history * 2:
            self.conversation_history[user_id] = self.conversation_history[user_id][-self.max_history * 2:]
    
    def _identify_referenced_knowledge(self, response: str) -> List[int]:
        """识别回复中引用的知识库文档（简单实现）"""
        referenced = []
        for i, doc in enumerate(self.knowledge_base):
            # 如果回复中包含知识库文档标题，认为引用了该文档
            if doc.get('title') and doc['title'] in response:
                referenced.append(i)
        return referenced
    
    def clear_history(self, user_id: int):
        """清空用户的对话历史"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
            logger.info(f"已清空用户 {user_id} 的对话历史")
    
    def update_knowledge_base(self, knowledge_base: List[Dict]):
        """更新知识库内容"""
        self.knowledge_base = knowledge_base
        logger.info(f"知识库已更新 | 文档数: {len(knowledge_base)}")


# ========== 工厂函数 ==========

def create_ai_services(api_key: str, base_url: str = "https://api.deepseek.com",
                       model: str = "deepseek-chat", timeout: int = 60,
                       knowledge_base: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """
    创建所有AI服务的工厂函数
    
    参数:
        api_key: DeepSeek API密钥
        base_url: API基础URL
        model: 模型名称
        timeout: 超时时间
        knowledge_base: 知识库内容（用于AI导师）
    
    返回:
        Dict包含三个服务实例: {'judge': CodeJudge, 'generator': ChallengeGenerator, 'mentor': AIMentor}
    """
    return {
        'judge': CodeJudge(api_key, base_url, model, timeout),
        'generator': ChallengeGenerator(api_key, base_url, model, timeout),
        'mentor': AIMentor(api_key, base_url, model, timeout, knowledge_base),
    }


# ========== 使用示例 ==========

if __name__ == "__main__":
    # 示例：初始化AI服务
    # services = create_ai_services(
    #     api_key="your-api-key",
    #     knowledge_base=[
    #         {"title": "HTML基础", "content": "HTML是超文本标记语言..."},
    #         {"title": "CSS选择器", "content": "CSS选择器用于选择元素..."},
    #     ]
    # )
    
    # 示例：代码审判
    # judge = services['judge']
    # result = judge.judge(
    #     description="创建一个包含标题和段落的HTML页面",
    #     scoring_criteria={"correctness": 40, "code_quality": 30, "best_practice": 20, "creativity": 10},
    #     code="<h1>Hello</h1><p>World</p>",
    #     difficulty="bronze",
    #     language="html"
    # )
    # print(result.to_dict())
    
    print("AI服务层模块已加载")
    print("包含三个核心类：CodeJudge, ChallengeGenerator, AIMentor")
