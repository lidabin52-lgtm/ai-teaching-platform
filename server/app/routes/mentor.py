"""
AI导师模块API
处理AI对话、历史记录等接口
"""
from flask import Blueprint, request, jsonify, current_app, Response, stream_with_context
import json
from datetime import datetime
import uuid

from app.utils.auth import login_required
from app.utils.response import success, error, bad_request, not_found
from app.utils.db import query_one, query_all, execute, insert_and_get_id

# 创建蓝图
mentor_bp = Blueprint('mentor', __name__, url_prefix='/api/mentor')


@mentor_bp.route('/chat', methods=['POST'])
@login_required
def chat(current_user):
    """
    发送消息，返回AI回复
    
    请求体:
        {
            "message": "学生消息",
            "challenge_id": 1,  // 可选，当前闯关ID
            "stream": false     // 可选，是否流式响应
        }
    
    返回:
        {
            "code": 200,
            "data": {
                "conversation_id": "CONVxxx",
                "message_id": 123,
                "content": "AI回复内容",
                "referenced_knowledge": [1, 2]
            }
        }
    """
    user_id = current_user['user_id']
    data = request.get_json()
    
    if not data:
        return bad_request('请求体不能为空')
    
    message = data.get('message', '').strip()
    challenge_id = data.get('challenge_id')
    use_stream = data.get('stream', False)
    
    if not message:
        return bad_request('消息内容不能为空')
    
    if len(message) > 2000:
        return bad_request('消息长度不能超过2000个字符')
    
    # 获取或创建对话
    conversation = None
    if challenge_id:
        # 查找该关卡的现有对话
        conversation = query_one(
            """SELECT * FROM ai_conversations
               WHERE user_id = %s AND challenge_id = %s AND status = 1
               ORDER BY updated_at DESC LIMIT 1""",
            (user_id, challenge_id)
        )
    
    if not conversation:
        # 创建新对话
        conversation_no = f"CONV{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
        conversation_id = insert_and_get_id(
            """INSERT INTO ai_conversations (conversation_no, user_id, challenge_id, title)
               VALUES (%s, %s, %s, %s)""",
            (conversation_no, user_id, challenge_id, message[:50] + ('...' if len(message) > 50 else ''))
        )
        conversation = {'id': conversation_id, 'conversation_no': conversation_no}
    else:
        conversation_id = conversation['id']
    
    # 保存用户消息
    user_msg_id = insert_and_get_id(
        """INSERT INTO ai_messages (conversation_id, role, content, content_type)
           VALUES (%s, 'user', %s, 'text')""",
        (conversation_id, message)
    )
    
    # 获取关卡上下文
    challenge_context = None
    if challenge_id:
        challenge = query_one(
            "SELECT id, title, description FROM challenges WHERE id = %s",
            (challenge_id,)
        )
        if challenge:
            challenge_context = {
                'title': challenge['title'],
                'description': challenge['description']
            }
    
    # 获取知识库内容
    knowledge_base = _get_knowledge_base()
    
    try:
        # 调用AI导师服务
        from app.services.ai_service import AIMentor
        
        api_key = current_app.config.get('DEEPSEEK_API_KEY', '')
        base_url = current_app.config.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        
        if not api_key:
            # 模拟回复（开发环境）
            ai_response = _mock_mentor_response(message, challenge_context)
            
            # 保存AI消息
            ai_msg_id = insert_and_get_id(
                """INSERT INTO ai_messages (conversation_id, role, content, content_type)
                   VALUES (%s, 'assistant', %s, 'text')""",
                (conversation_id, ai_response)
            )
            
            # 更新对话统计
            execute(
                """UPDATE ai_conversations SET
                   message_count = message_count + 2,
                   updated_at = NOW()
                   WHERE id = %s""",
                (conversation_id,)
            )
            
            return success({
                'conversation_id': conversation['conversation_no'],
                'message_id': ai_msg_id,
                'content': ai_response,
                'referenced_knowledge': []
            })
        
        if use_stream:
            # 流式响应
            mentor = AIMentor(api_key=api_key, base_url=base_url, knowledge_base=knowledge_base)
            
            def generate():
                full_content = []
                for chunk in mentor.chat(
                    user_id=user_id,
                    message=message,
                    challenge_context=challenge_context,
                    stream=True
                ):
                    full_content.append(chunk)
                    yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                
                # 保存完整回复
                complete_response = ''.join(full_content)
                insert_and_get_id(
                    """INSERT INTO ai_messages (conversation_id, role, content, content_type)
                       VALUES (%s, 'assistant', %s, 'text')""",
                    (conversation_id, complete_response)
                )
                execute(
                    """UPDATE ai_conversations SET
                       message_count = message_count + 2,
                       updated_at = NOW()
                       WHERE id = %s""",
                    (conversation_id,)
                )
                yield "data: [DONE]\n\n"
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        else:
            # 普通响应
            mentor = AIMentor(api_key=api_key, base_url=base_url, knowledge_base=knowledge_base)
            response = mentor.chat(
                user_id=user_id,
                message=message,
                challenge_context=challenge_context,
                stream=False
            )
            
            # 保存AI消息
            ai_msg_id = insert_and_get_id(
                """INSERT INTO ai_messages (conversation_id, role, content, content_type, tokens_used, response_time_ms)
                   VALUES (%s, 'assistant', %s, 'text', %s, %s)""",
                (conversation_id, response.content, response.tokens_used, response.response_time_ms)
            )
            
            # 更新对话统计
            execute(
                """UPDATE ai_conversations SET
                   message_count = message_count + 2,
                   updated_at = NOW()
                   WHERE id = %s""",
                (conversation_id,)
            )
            
            return success({
                'conversation_id': conversation['conversation_no'],
                'message_id': ai_msg_id,
                'content': response.content,
                'referenced_knowledge': response.referenced_knowledge
            })
            
    except Exception as e:
        return error(f'AI服务异常: {str(e)}', code=500)


def _get_knowledge_base():
    """获取知识库内容"""
    docs = query_all(
        """SELECT id, title, content, summary, category, tags
           FROM knowledge_base
           WHERE status = 1
           ORDER BY reference_count DESC, view_count DESC
           LIMIT 10"""
    )
    
    return [{
        'id': d['id'],
        'title': d['title'],
        'content': d['content'],
        'summary': d['summary'],
        'category': d['category']
    } for d in docs]


def _mock_mentor_response(message, challenge_context):
    """模拟AI导师回复（开发环境）"""
    if challenge_context:
        return f"你好！我看到你正在进行「{challenge_context['title']}」关卡。关于你的问题「{message[:30]}...」，让我来帮你分析一下：\n\n这是一个很好的问题！建议你先仔细阅读关卡需求，然后尝试动手实践。如果遇到具体问题，可以随时问我更详细的细节。"
    else:
        return f"你好！我是你的前端学习助手小智老师。关于「{message[:30]}...」这个问题，我来为你解答：\n\n建议你通过闯关练习来巩固这方面的知识。如果有更具体的问题，欢迎继续提问！"


@mentor_bp.route('/history', methods=['GET'])
@login_required
def get_history(current_user):
    """
    获取对话历史
    
    查询参数:
        conversation_id: 对话编号（可选，不传则返回对话列表）
        page: 页码
        page_size: 每页数量
    """
    user_id = current_user['user_id']
    conversation_no = request.args.get('conversation_id')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    if conversation_no:
        # 获取特定对话的消息历史
        conversation = query_one(
            "SELECT * FROM ai_conversations WHERE conversation_no = %s AND user_id = %s",
            (conversation_no, user_id)
        )
        
        if not conversation:
            return not_found('对话不存在')
        
        messages = query_all(
            """SELECT id, role, content, content_type, created_at
               FROM ai_messages
               WHERE conversation_id = %s
               ORDER BY created_at ASC""",
            (conversation['id'],)
        )
        
        items = [{
            'id': m['id'],
            'role': m['role'],
            'content': m['content'],
            'content_type': m['content_type'],
            'created_at': m['created_at'].isoformat() if m['created_at'] else None
        } for m in messages]
        
        return success({
            'conversation': {
                'id': conversation['conversation_no'],
                'title': conversation['title'],
                'message_count': conversation['message_count']
            },
            'messages': items
        })
    else:
        # 返回对话列表
        total = query_one(
            "SELECT COUNT(*) as count FROM ai_conversations WHERE user_id = %s AND status = 1",
            (user_id,)
        )['count']
        
        offset = (page - 1) * page_size
        conversations = query_all(
            """SELECT c.id, c.conversation_no, c.title, c.message_count, c.updated_at,
                      ch.title as challenge_title
               FROM ai_conversations c
               LEFT JOIN challenges ch ON c.challenge_id = ch.id
               WHERE c.user_id = %s AND c.status = 1
               ORDER BY c.updated_at DESC
               LIMIT %s OFFSET %s""",
            (user_id, page_size, offset)
        )
        
        items = [{
            'id': c['conversation_no'],
            'title': c['title'] or c['challenge_title'] or '新对话',
            'message_count': c['message_count'],
            'updated_at': c['updated_at'].isoformat() if c['updated_at'] else None
        } for c in conversations]
        
        from app.utils.response import paginate
        return jsonify(paginate(items, total, page, page_size))


@mentor_bp.route('/conversations/<conversation_no>', methods=['DELETE'])
@login_required
def delete_conversation(current_user, conversation_no):
    """删除对话（归档）"""
    user_id = current_user['user_id']
    
    result = execute(
        "UPDATE ai_conversations SET status = 0 WHERE conversation_no = %s AND user_id = %s",
        (conversation_no, user_id)
    )
    
    if result == 0:
        return not_found('对话不存在')
    
    return success(message='对话已删除')
