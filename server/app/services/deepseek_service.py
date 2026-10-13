"""
DeepSeek AI服务模块
封装DeepSeek API调用，支持流式和非流式对话
使用OpenAI兼容接口格式
"""
from openai import OpenAI
from flask import current_app


class DeepSeekService:
    """DeepSeek AI服务封装类"""

    def __init__(self):
        """初始化DeepSeek客户端"""
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化OpenAI兼容客户端"""
        try:
            api_key = current_app.config.get('DEEPSEEK_API_KEY', '')
            api_base = current_app.config.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
            model = current_app.config.get('DEEPSEEK_MODEL', 'deepseek-chat')

            if not api_key:
                print("警告: DeepSeek API Key 未配置")

            self.client = OpenAI(
                api_key=api_key,
                base_url=f"{api_base}/v1",
            )
            self.model = model
        except Exception as e:
            print(f"DeepSeek客户端初始化失败: {e}")

    def chat(self, messages, stream=False, temperature=0.7, max_tokens=2000):
        """
        发送对话请求

        参数:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            stream: 是否使用流式响应
            temperature: 生成温度（0-1）
            max_tokens: 最大生成token数

        返回:
            非流式: 完整回复文本
            流式: 生成器，逐步产出文本片段
        """
        if not self.client:
            raise Exception("DeepSeek客户端未初始化，请检查API Key配置")

        timeout = current_app.config.get('DEEPSEEK_TIMEOUT', 60)

        # 构建系统提示词（教学场景专用）
        system_prompt = {
            "role": "system",
            "content": (
                "你是一个专业的前端开发教学助手。你的任务是：\n"
                "1. 解答前端开发相关问题（HTML、CSS、JavaScript、Vue、React等）\n"
                "2. 分析和审查用户提交的代码，给出改进建议\n"
                "3. 提供清晰、易懂的解释，适合不同水平的学习者\n"
                "4. 在适当的时候给出代码示例和实践建议\n"
                "请用中文回答问题。"
            )
        }

        full_messages = [system_prompt] + messages

        if stream:
            # 流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            return self._stream_response(response)
        else:
            # 非流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            return response.choices[0].message.content

    def _stream_response(self, response):
        """
        流式响应生成器
        逐步产出文本片段
        """
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def analyze_code(self, code, language, analyze_type='review'):
        """
        代码分析

        参数:
            code: 代码内容
            language: 编程语言
            analyze_type: 分析类型 (review/explain/optimize/debug)

        返回:
            分析结果文本
        """
        type_prompts = {
            'review': '请审查以下代码，指出问题和改进建议：',
            'explain': '请解释以下代码的功能和逻辑：',
            'optimize': '请优化以下代码，并说明优化理由：',
            'debug': '以下代码有bug，请找出并修复：',
        }

        prompt = f"{type_prompts.get(analyze_type, type_prompts['review'])}\n\n"
        prompt += f"语言: {language}\n```{language}\n{code}\n```"

        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, stream=False, temperature=0.3)


# 创建全局服务实例
deepseek_service = DeepSeekService()
