#!/usr/bin/env python3
"""
港澳通行证材料自查系统 - 离线版本（不依赖网络）
基于规则引擎的智能对话系统
适配 PythonAnywhere 部署
"""

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# 手动实现 CORS（无需 flask-cors 依赖）
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


class OfflinePermitAgent:
    """离线版港澳通行证办理顾问"""
    
    def __init__(self):
        self.sessions = {}  # 存储会话状态
        
    def process_message(self, user_message, session_id):
        """处理用户消息，返回结构化回复"""
        
        # 初始化会话状态
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'step': 'start',
                'data': {}
            }
        
        session = self.sessions[session_id]
        user_lower = user_message.lower().strip()
        
        # 根摒当前步骤和用户输入，生成回复
        return self._handle_conversation(user_message, user_lower, session, session_id)
    
    
    def _handle_conversation(self, original_msg, msg_lower, session, session_id):
        """核心对话逻辑"""
        
        step = session['step']
        data = session['data']
        
        # ========== 开始阶段 ==========
        if step == 'start':
            if any(word in msg_lower for word in ['你好', '您好', 'hello', 'hi', '开始', '启动']):
                session['step'] = 'check_guojing'
                return self._reply(
                    '您好，欢迎咨询港澳通行证办理业务。我是出入境业务智能助手，将通过对话帮助您核查所需材料。\n\n请问您的户籍所在地是否为广东省？',
                    ['是', '否'],
                    10
                )
            else:
                return self._reply(
                    '您好！我是港澳通行证办理智能助手。\n\n请问需要帮助您：\n1. 核查办理材料\n2. 了解办理流程\n3. 查询收费标准\n\n请选择或输入您的需求。',
                    ['核查办理材料', '了解办理流程', '查询收费标准'],
                    5
                )
        
        # ========== 核查户籍 ==========
        elif step == 'check_guojing':
            if '是' in msg_lower or '广东' in msg_lower or '广州' in msg_lower or '深圳' in msg_lower:
                data['is_guojing'] = True
                session['step'] = 'check_first_time'
                return self._reply(
                    '好的，确认您为广东省户籍（可异地办理）。\n\n请问本次申请是：',
                    ['首次办理', '续签/换证', '补办（丢失）'],
                    20
                )
            elif '否' in msg_lower or '外地' in msg_lower:
                data['is_guojing'] = False
                session['step'] = 'check_first_time'
                return self._reply(
                    '好的，您为非广东省户籍。\n\n请问本次申请是：',
                    ['首次办理', '续签/换证', '补办（丢失）'],
                    20
                )
            else:
                return self._reply(
                    '抱歉，我没理解您的意思。请选择：',
                    ['是', '否'],
                    10
                )
        
        # ========== 检查办理类型 ==========
        elif step == 'check_first_time':
            if '首次' in msg_lower or '第一次' in msg_lower or '新办' in msg_lower:
                data['apply_type'] = 'first'
                session['step'] = 'check_age'
                return self._reply(
                    '好的，确认为首次办理。\n\n请问申请人是否已满16周岁？',
                    ['是', '否'],
                    30
                )
            elif '续签' in msg_lower or '换证' in msg_lower or '过期' in msg_lower:
                data['apply_type'] = 'renew'
                session['step'] = 'check_passport'
                return self._reply(
                    '好的，确认为续签/换证。\n\n请问您是否持有有效往来港澳通行证？',
                    ['是', '否'],
                    30
                )
            elif '补办' in msg_lower or '丢失' in msg_lower or '遗失' in msg_lower:
                data['apply_type'] = 'replace'
                session['step'] = 'check_loss_report'
                return self._reply(
                    '好的，确认为证件补办。\n\n请问您是否已办理挂失手续？',
                    ['是', '否'],
                    30
                )
            else:
                return self._reply(
                    '请选择办理类型：',
                    ['首次办理', '续签/换证', '补办（丢失）'],
                    20
                )
        
        # ========== 检查年龄（首次办理） ==========
        elif step == 'check_age':
            if '是' in msg_lower or '满' in msg_lower or '成年' in msg_lower:
                data['is_adult'] = True
                session['step'] = 'check_id_card'
                return self._reply(
                    '好的，申请人已满16周岁（可独立办理）。\n\n请问您是否携带：',
                    ['身份证原件', '临时身份证', '都没有'],
                    40
                )
            elif '否' in msg_lower or '未成年' in msg_lower:
                data['is_adult'] = False
                session['step'] = 'check_guardian'
                return self._reply(
                    '好的，申请人为未成年人（需监护人陪同）。\n\n请问是否由监护人陪同办理？',
                    ['是', '否'],
                    40
                )
            else:
                return self._reply(
                    '请选择：',
                    ['是', '否'],
                    30
                )
        
        # ========== 检查身份证（首次办理-成人） ==========
        elif step == 'check_id_card':
            if '身份证' in msg_lower and '没有' not in msg_lower and '都' not in msg_lower:
                data['has_id_card'] = True
                session['step'] = 'check_photo'
                return self._reply(
                    '✅ 已确认身份证原件。\n\n请问您是否准备好：',
                    ['现场拍照', '自带照片回执', '都不清楚'],
                    50
                )
            elif '临时' in msg_lower:
                data['has_id_card'] = 'temp'
                session['step'] = 'check_photo'
                return self._reply(
                    '✅ 已确认临时身份证。\n\n请问您是否准备好：',
                    ['现场拍照', '自带照片回执', '都不清楚'],
                    50
                )
            else:
                return self._reply(
                    '⚠️ 首次办理必须携带身份证原件！\n\n请问您是否：',
                    ['回家取身份证', '办理临时身份证', '取消预约'],
                    40
                )
        
        # ========== 检查照片（首次办理） ==========
        elif step == 'check_photo':
            if '现场' in msg_lower:
                data['photo_type'] = 'onsite'
                session['step'] = 'check_form'
                return self._reply(
                    '✅ 选择现场拍照（免费，约5分钟）。\n\n请问您是否准备好：',
                    ['现场填表', '自带申请表', '都不清楚'],
                    60
                )
            elif '照片回执' in msg_lower or '自带' in msg_lower:
                data['photo_type'] = 'own'
                session['step'] = 'check_form'
                return self._reply(
                    '✅ 已准备照片回执。\n\n请问您是否准备好：',
                    ['现场填表', '自带申请表', '都不清楚'],
                    60
                )
            else:
                return self._reply(
                    '请选择拍照方式：',
                    ['现场拍照', '自带照片回执', '都不清楚'],
                    50
                )
        
        # ========== 检查申请表 ==========
        elif step == 'check_form':
            if '现场' in msg_lower and '自带' not in msg_lower:
                data['form_type'] = 'onsite'
                session['step'] = 'check_appointment'
                return self._reply(
                    '✅ 选择现场填表（有工作人员指导）。\n\n请问您是否已预约？',
                    ['是', '否'],
                    70
                )
            elif '自带' in msg_lower or '申请表' in msg_lower:
                data['form_type'] = 'own'
                session['step'] = 'check_appointment'
                return self._reply(
                    '✅ 已准备申请表。\n\n请问您是否已预约？',
                    ['是', '否'],
                    70
                )
            else:
                return self._reply(
                    '请选择填表方式：',
                    ['现场填表', '自带申请表', '都不清楚'],
                    60
                )
        
        # ========== 检查预约 ==========
        elif step == 'check_appointment':
            if '是' in msg_lower or '预约' in msg_lower:
                data['has_appointment'] = True
                return self._finish_check(session_id)
            elif '否' in msg_lower or '没有' in msg_lower:
                data['has_appointment'] = False
                session['step'] = 'show_appointment_guide'
                return self._reply(
                    '⚠️ 必须先预约才能办理！\n\n请问需要我教您如何预约吗？',
                    ['是，教我预约', '我自己会'],
                    75
                )
            else:
                return self._reply(
                    '请选择：',
                    ['是', '否'],
                    70
                )
        
        # ========== 显示预约指南 ==========
        elif step == 'show_appointment_guide':
            if '教' in msg_lower or '是' in msg_lower:
                session['step'] = 'check_appointment'
                return self._reply(
                    '📅 预约流程如下：\n\n<strong>方式一：微信小程序「深圳公安」</strong>\n1. 微信搜索「深圳公安」小程序\n2. 点击「出入境」→「出入境预约」\n3. 选择「龙岗区出入境服务大厅」\n4. 选择办理日期和时间段\n5. 填写信息，提交预约\n6. 预约成功后请截图保存\n\n<strong>方式二：「移民局12367」App</strong>\n1. 下载「移民局12367」App\n2. 登录后选择「预约办证」\n3. 选择大厅及时间段\n4. 提交并截图保存\n\n预约成功后，请回复"已预约"。',
                    ['已预约', '好的'],
                    80
                )
            else:
                session['step'] = 'check_appointment'
                return self._reply(
                    '好的，请务必提前预约！\n\n预约完成后，请回复"已预约"。',
                    ['已预约'],
                    75
                )
        
        # ========== 处理"已预约" ==========
        if '预约' in msg_lower:
            return self._finish_check(session_id)
        
        # ========== 常见问题解答 ==========
        if '签注' in msg_lower:
            session['step'] = step  # 保持当前步骤
            return self._reply(
                '📖 签注说明：\n\n<strong>港澳通行证 = 通行证 + 签注</strong>\n\n<strong>1️⃣ 通行证（卡片）</strong>\n您的出入资格证明，工本费约50元。\n\n<strong>2️⃣ 签注（许可次数）</strong>\n每次去港澳需要有签注。\n\n<strong>常见签注类型：</strong>\n• 个人旅游（G签）- 广东户籍可办\n• 三个月一次 - 约15元\n• 一年一次 - 约15元\n• 一年两次 - 约30元\n\n💡 建议：首次办证时可同时申请签注！\n\n请问是否继续材料自查？',
                ['继续', '好的'],
                50
            )
        
        if '费用' in msg_lower or '多少钱' in msg_lower or '收费' in msg_lower:
            session['step'] = step
            return self._reply(
                '💰 收费标准（官方2024年5月更新）：\n\n<strong>1️⃣ 往来港澳通行证</strong>\n• 工本费：约50元/证\n\n<strong>2️⃣ 签注费用</strong>\n• 一次有效签注：15元/件\n• 二次有效签注：30元/件\n• 短期多次签注：80元/件\n\n<strong>3️⃣ 其他费用</strong>\n• 照片：现场免费拍照\n• 快递：约15-20元（可选）\n\n请问是否继续？',
                ['继续', '好的'],
                50
            )
        
        if '时间' in msg_lower or '多久' in msg_lower or '工作日' in msg_lower:
            session['step'] = step
            return self._reply(
                '⏰ 办理时限：\n\n<strong>广东省户籍：</strong>\n• 首次办理：约7个工作日\n• 续签：约5个工作日\n\n<strong>非广东省户籍：</strong>\n• 首次办理：约20个工作日（需核查户籍信息）\n\n<strong>领取方式：</strong>\n• 邮寄：约多2-3天\n• 自取：办结后凭回执单领取\n\n请问是否继续？',
                ['继续', '好的'],
                50
            )
        
        if '地址' in msg_lower or '哪里' in msg_lower or '大厅' in msg_lower:
            session['step'] = step
            return self._reply(
                '📍 办理地点：\n\n<strong>推荐：龙岗区出入境服务大厅</strong>\n地址：深圳市龙岗区龙翔大道8033-1号\n\n<strong>办公时间：</strong>\n• 周一至周五：9:00-12:00，14:00-18:00\n• 周六：9:00-12:00（需预约）\n\n<strong>其他可选大厅：</strong>\n• 深圳市出入境管理局（罗湖区）\n• 各区出入境大厅\n\n请问是否继续？',
                ['继续', '好的'],
                50
            )
        
        if '预约' in msg_lower and session['step'] != 'show_appointment_guide':
            session['step'] = 'show_appointment_guide'
            return self._reply(
                '📅 预约流程如下：\n\n<strong>方式一：微信小程序「深圳公安」</strong>\n1. 微信搜索「深圳公安」小程序\n2. 点击「出入境」→「出入境预约」\n3. 选择「龙岗区出入境服务大厅」\n4. 选择办理日期和时间段\n5. 填写信息，提交预约\n6. 预约成功后请截图保存\n\n请问是否继续材料自查？',
                ['继续', '好的'],
                50
            )
        
        # ========== 重新开始 ==========
        if '重新' in msg_lower or '开始' in msg_lower or '重启' in msg_lower:
            del self.sessions[session_id]
            return self._reply(
                '好的，已重置对话。\n\n您好，欢迎咨询港澳通行证办理业务。请问您的户籍所在地是否为广东省？',
                ['是', '否'],
                10
            )
        
        # ========== 默认回复 ==========
        return self._reply(
            '抱歉，我不太理解您的意思。请您选择下面的选项，或者输入以下关键词：\n\n• "预约" - 了解如何预约\n• "签注" - 了解什么是签注\n• "费用" - 查询收费标准\n• "时间" - 查询办理时限\n• "地址" - 查询办理地点\n• "重新开始" - 重新开始对话',
            ['预约', '签注', '费用', '重新开始'],
            0
        )
    
    
    def _finish_check(self, session_id):
        """完成材料核查，生成总结"""
        session = self.sessions[session_id]
        data = session['data']
        
        # 构建材料清单
        checklist = []
        checklist.append('✅ <strong>必须材料：</strong>')
        checklist.append('☑ 身份证原件（在有效期内）')
        
        if data.get('is_adult') is False:
            checklist.append('☑ 监护人身份证原件')
            checklist.append('☑ 监护关系证明（户口本/出生证）')
        
        checklist.append('')
        checklist.append('✅ <strong>照片材料：</strong>')
        if data.get('photo_type') == 'onsite':
            checklist.append('☑ 现场免费拍照（推荐）')
        else:
            checklist.append('☑ 数字相片采集回执')
        
        checklist.append('')
        checklist.append('✅ <strong>申请表格：</strong>')
        if data.get('form_type') == 'onsite':
            checklist.append('☑ 现场填写申请表')
        else:
            checklist.append('☑ 提前下载并打印申请表')
        
        checklist.append('')
        checklist.append('✅ <strong>预约证明：</strong>')
        checklist.append('☑ 预约成功截图')
        
        checklist_text = '\n'.join(checklist)
        
        # 构建提示
        tips = []
        tips.append('📌 <strong>重要提示：</strong>')
        tips.append('1. 请提前预约，无预约无法办理')
        tips.append('2. 建议出发前再次检查材料')
        tips.append('3. 可现场拍照，无需提前准备照片')
        tips.append('4. 首次办理必须本人到场（需录入指纹）')
        tips.append('5. 签注可同时申请，建议一次办好')
        
        tips_text = '\n'.join(tips)
        
        return self._reply(
            f'🎉 <strong>材料核查完成！</strong>\n\n您已准备好以下材料：\n\n{checklist_text}\n\n{tips_text}\n\n祝办理顺利！\n\n如需重新核查，请回复"重新开始"。',
            ['重新开始'],
            100
        )
    
    
    def _reply(self, text, options=None, progress=0):
        """生成结构化回复"""
        return {
            'reply': text,
            'options': options or [],
            'progress': progress
        }


# 创建Agent实例
agent = OfflinePermitAgent()


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
        'service': 'hk-permit-checker-api-offline',
        'version': '2.0-offline'
    })


@app.route('/')
def root():
    """根路径返回简单信息"""
    return jsonify({
        'service': '港澳通行证材料自查系统 - 离线版API',
        'status': 'running',
        'version': '2.0-offline',
        'features': [
            '完全离线，不依赖外部API',
            '基于规则引擎的智能对话',
            '支持材料核查、流程指导、费用查询'
        ],
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/api/health (GET)'
        }
    })


if __name__ == '__main__':
    app.run()
