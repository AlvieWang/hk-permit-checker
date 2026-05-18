#!/usr/bin/env python3
"""
港澳通行证材料自查系统 - 后端API服务
提供智能对话能力，调用AI模型进行自然语言交互
适配 PythonAnywhere 部署
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 模拟AI Agent的对话逻辑
class PermitAgent:
    def __init__(self):
        self.state = {}
        
    def process_message(self, user_message, session_id):
        """处理用户消息，返回Agent回复"""
        
        # 简单的意图识别
        user_lower = user_message.lower()
        
        # 关键词匹配和回复
        if any(word in user_lower for word in ['你好', '您好', 'hello', 'hi']):
            return {
                'reply': '您好，欢迎咨询港澳通行证办理业务。我是出入境业务智能助手，将通过对话帮助您核查所需材料。\n\n请问您的户籍所在地是否为广东省？',
                'options': ['是', '否'],
                'progress': 10
            }
        
        elif '是' in user_lower or 'yes' in user_lower:
            return {
                'reply': '好的，确认您为广东省户籍。\n\n请问本次申请是「首次办理」、「续签/换证」还是「补办（丢失）」？',
                'options': ['首次办理', '续签/换证', '补办'],
                'progress': 20
            }
        
        elif '首次' in user_lower or '第一次' in user_lower:
            return {
                'reply': '好的，确认为首次办理。\n\n请问申请人是否已满16周岁？',
                'options': ['是', '否'],
                'progress': 30
            }
        
        elif '预约' in user_lower:
            return {
                'reply': '''📅 预约流程如下：\n\n<strong>方式一：微信小程序「深圳公安」</strong>\n1. 微信搜索「深圳公安」小程序\n2. 点击「出入境」→「出入境预约」\n3. 选择「龙岗区出入境服务大厅」\n4. 选择办理日期和时间段\n5. 填写信息，提交预约\n6. 预约成功后请截图保存\n\n<strong>方式二：「移民局12367」App</strong>\n1. 下载「移民局12367」App\n2. 登录后选择「预约办证」\n3. 选择大厅及时间段\n4. 提交并截图保存\n\n请问是否继续材料自查？''',
                'options': ['继续', '好的'],
                'progress': 50
            }
        
        elif '签注' in user_lower:
            return {
                'reply': '''📖 签注说明：\n\n<strong>港澳通行证 = 通行证 + 签注</strong>\n\n<strong>1️⃣ 通行证（卡片）</strong>\n您的出入资格证明，工本费约50元。\n\n<strong>2️⃣ 签注（许可次数）</strong>\n每次去港澳需要有签注。\n\n<strong>常见签注类型：</strong>\n• 个人旅游（G签）- 广东户籍可办\n• 三个月一次 - 约15元\n• 一年一次 - 约15元\n• 一年两次 - 约30元\n\n💡 建议：首次办证时可同时申请签注！\n\n请问是否继续材料自查？''',
                'options': ['继续', '好的'],
                'progress': 50
            }
        
        elif '重新' in user_lower or '开始' in user_lower:
            if session_id in self.state:
                del self.state[session_id]
            return {
                'reply': '好的，已重置对话。\n\n您好，欢迎咨询港澳通行证办理业务。请问您的户籍所在地是否为广东省？',
                'options': ['是', '否'],
                'progress': 10
            }
        
        else:
            # 默认回复
            return {
                'reply': '抱歉，我不太理解您的意思。请您选择下面的选项，或者输入以下关键词：\n\n• "预约" - 了解如何预约\n• "签注" - 了解什么是签注\n• "重新开始" - 重新开始对话',
                'options': ['预约', '签注', '重新开始'],
                'progress': 0
            }

# 创建Agent实例
agent = PermitAgent()

@app.route('/api/chat', methods=['POST'])
def chat():
    """对话API接口"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # 调用Agent处理消息
    response = agent.process_message(user_message, session_id)
    
    return jsonify(response)

@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'hk-permit-checker-api'})

@app.route('/')
def root():
    """根路径返回简单信息"""
    return jsonify({
        'service': '港澳通行证材料自查系统 - 后端API',
        'status': 'running',
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/api/health (GET)'
        }
    })

if __name__ == '__main__':
    # PythonAnywhere 会自动处理端口
    # 本地测试时可以指定端口
    app.run()
