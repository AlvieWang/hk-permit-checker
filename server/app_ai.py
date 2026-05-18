#!/usr/bin/env python3
"""
港澳通行证材料自查系统 - AI版本
使用免费AI API（Groq）提供真实智能对话
适配 PythonAnywhere 部署
"""

from flask import Flask, request, jsonify
import os
import requests
import json

app = Flask(__name__)

# 手动实现 CORS（无需 flask-cors 依赖）
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


class AIPermitAgent:
    """AI驱动的港澳通行证办理顾问（使用Groq免费API）"""
    
    def __init__(self):
        # 从环境变量获取API密钥（更安全）
        self.api_key = os.environ.get('GROQ_API_KEY', '')
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        
        # 系统提示词（定义AI的角色和行为）
        self.system_prompt = """你是深圳公安出入境业务的智能助手，专门帮助市民核查港澳通行证办理材料。

你的任务：
1. 通过友好对话，逐步核查用户办理港澳通行证所需的材料
2. 提供准确的办事指南（预约流程、收费标准、办理地点等）
3. 根据用户情况（户籍、年龄、办理类型）给出个性化建议

对话原则：
- 使用官方口吻，但保持友好
- 每次只问一个问题，避免信息过载
- 提供清晰的选项按钮（如"是/否"）
- 在合适时机提供办事指南（预约、签注说明、收费标准等）

材料清单（广东省户籍，首次办理，16周岁以上）：
✅ 必须材料：
- 身份证原件（有效期内的）
- 照片回执（可现场免费拍照）
- 申请表（可现场填写）
- 预约凭证（必须提前预约）

✅ 可选材料：
- 监护关系证明（16周岁以下需要）

收费标准（2024年5月更新）：
- 港澳通行证工本费：约50元
- 一次有效签注：15元
- 二次有效签注：30元

预约方式：
1. 微信小程序「深圳公安」→ 出入境 → 出入境预约
2. 「移民局12367」App → 预约办证

办理地点：
深圳市龙岗区龙翔大道8033-1号（龙岗区出入境服务大厅）

开始对话时，先问候用户，然后询问："请问您的户籍所在地是否为广东省？"
"""
    
    def process_message(self, user_message, session_id):
        """调用Groq API处理用户消息"""
        
        # 检查是否配置了API密钥
        if not self.api_key:
            return {
                'reply': '⚠️ AI服务未配置API密钥。\n\n正在切换到离线模式...\n\n您好，欢迎咨询港澳通行证办理业务。我是出入境业务智能助手，将通过对话帮助您核查所需材料。\n\n请问您的户籍所在地是否为广东省？',
                'options': ['是', '否'],
                'progress': 10,
                'using_offline_mode': True
            }
        
        try:
            # 调用Groq API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'llama3-8b-8192',  # Groq免费模型
                'messages': [
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': user_message}
                ],
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['choices'][0]['message']['content']
                
                # 尝试从AI回复中提取选项（如果有的话）
                options = self._extract_options(ai_reply)
                
                return {
                    'reply': ai_reply,
                    'options': options,
                    'progress': 50,  # AI模式下进度较难精确计算
                    'using_ai': True
                }
            else:
                # API调用失败，返回离线回复
                return self._offline_fallback(user_message)
                
        except Exception as e:
            print(f"AI API调用失败：{e}")
            # 失败时使用离线模式
            return self._offline_fallback(user_message)
    
    
    def _extract_options(self, text):
        """从AI回复中提取选项（简单实现）"""
        # 查找常见的选项模式
        options = []
        
        # 检查是否包含选项按钮的提示
        if '是' in text and '否' in text:
            options = ['是', '否']
        elif '首次' in text:
            options = ['首次办理', '续签/换证', '补办']
        elif '预约' in text:
            options = ['查看预约指南', '继续']
        elif '重新' in text:
            options = ['重新开始', '继续']
        
        return options if options else ['继续', '重新开始']
    
    
    def _offline_fallback(self, user_message):
        """离线模式的备用回复（简化版）"""
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ['你好', '您好', 'hello']):
            return {
                'reply': '您好，欢迎咨询港澳通行证办理业务。我是出入境业务智能助手（离线模式）。\n\n请问您的户籍所在地是否为广东省？',
                'options': ['是', '否'],
                'progress': 10
            }
        elif '是' in user_lower:
            return {
                'reply': '好的，确认您为广东省户籍。\n\n请问本次申请是「首次办理」、「续签/换证」还是「补办（丢失）」？',
                'options': ['首次办理', '续签/换证', '补办'],
                'progress': 20
            }
        elif '重新' in user_lower:
            return {
                'reply': '好的，已重置对话。\n\n请问您的户籍所在地是否为广东省？',
                'options': ['是', '否'],
                'progress': 10
            }
        else:
            return {
                'reply': '（AI服务暂时不可用，当前为离线模式）\n\n请问需要帮助您：\n1. 核查办理材料\n2. 了解预约流程\n3. 查询收费标准\n\n请选择或输入您的需求。',
                'options': ['核查材料', '预约流程', '收费标准', '重新开始'],
                'progress': 5
            }
    
    
    def set_api_key(self, api_key):
        """设置API密钥"""
        self.api_key = api_key


# 创建Agent实例
agent = AIPermitAgent()


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """对话API接口"""
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # 调用Agent处理消息
    response = agent.process_message(user_message, session_id)
    
    return jsonify(response)


@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'hk-permit-checker-api-ai',
        'version': '2.0-ai',
        'ai_enabled': bool(agent.api_key)
    })


@app.route('/api/set-key', methods=['POST', 'OPTIONS'])
def set_key():
    """设置API密钥（仅用于测试，生产环境应使用环境变量）"""
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.json
    api_key = data.get('api_key', '')
    
    if api_key:
        agent.set_api_key(api_key)
        return jsonify({'status': 'success', 'message': 'API密钥已设置'})
    else:
        return jsonify({'status': 'error', 'message': 'API密钥不能为空'}), 400


@app.route('/')
def root():
    """根路径返回简单信息"""
    return jsonify({
        'service': '港澳通行证材料自查系统 - AI版API',
        'status': 'running',
        'version': '2.0-ai',
        'ai_provider': 'Groq (免费)',
        'ai_enabled': bool(agent.api_key),
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/api/health (GET)',
            'set_key': '/api/set-key (POST) - 设置API密钥'
        },
        'note': '使用Groq免费API，需先配置API密钥。获取地址：<ADDRESS_REMOVED>
    })


if __name__ == '__main__':
    # 从命令行参数或环境变量获取API密钥
    import sys
    if len(sys.argv) > 1:
        agent.set_api_key(sys.argv[1])
        print(f"✅ API密钥已通过命令行参数设置")
    
    app.run(debug=True)
