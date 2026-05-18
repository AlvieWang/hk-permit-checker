// 港澳通行证材料自查系统 - 对话逻辑
// 模拟深圳公安出入境智能助手

// 状态管理
const state = {
    step: 0,
    userData: {
        isGuangdong: null,
        applicationType: null,
        age: null,
        idCardReady: null,
        photoReceipt: null,
        applicationForm: null,
        appointment: null
    },
    checklist: {
        idCard: false,
        photo: false,
        form: false,
        appointment: false
    }
};

// 时间更新
function updateTime() {
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('current-time').textContent = timeStr;
}

// 初始化
window.onload = function() {
    updateTime();
    setInterval(updateTime, 1000);
    initializeChat();
};

// 初始化聊天
function initializeChat() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = '';
    
    addAgentMessage(
        '您好，欢迎咨询港澳通行证办理业务。我将通过几个问题帮助您核查所需材料是否齐全。请您回答以下问题：<br><br><strong>请问您的户籍所在地是否为广东省？</strong>',
        [
            { text: '是', value: 'yes' },
            { text: '否', value: 'no' }
        ]
    );
}

// 添加Agent消息
function addAgentMessage(text, options = null) {
    const messagesContainer = document.getElementById('chat-messages');
    const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    let optionsHTML = '';
    if (options) {
        optionsHTML = '<div class="message-options">';
        options.forEach(opt => {
            optionsHTML += `<button class="option-btn" onclick="handleOption('${opt.value}', '${opt.text}')">${opt.text}</button>`;
        });
        optionsHTML += '</div>';
    }
    
    const messageHTML = `
        <div class="message agent-message">
            <div class="message-avatar">🧑💼</div>
            <div class="message-content">
                <div class="message-header">
                    <strong>出入境业务助手</strong>
                    <span class="time">${time}</span>
                </div>
                <div class="message-text">${text}</div>
                ${optionsHTML}
            </div>
        </div>
    `;
    
    messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

// 添加用户消息
function addUserMessage(text) {
    const messagesContainer = document.getElementById('chat-messages');
    const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    const messageHTML = `
        <div class="message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <div class="message-header">
                    <strong>您</strong>
                    <span class="time">${time}</span>
                </div>
                <div class="message-text">${text}</div>
            </div>
        </div>
    `;
    
    messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

// 处理选项点击
function handleOption(value, text) {
    addUserMessage(text);
    
    setTimeout(() => {
        processAnswer(value, text);
    }, 500);
}

// 处理文本输入
function sendUserMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    
    if (!text) return;
    
    addUserMessage(text);
    input.value = '';
    
    setTimeout(() => {
        processTextInput(text);
    }, 500);
}

// 回车发送
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendUserMessage();
    }
}

// 快捷操作
function quickAction(action) {
    addUserMessage(action);
    
    setTimeout(() => {
        if (action === '如何预约') {
            showAppointmentHelp();
        } else if (action === '签注是什么') {
            showEndorsementInfo();
        } else if (action === '重新开始') {
            resetChat();
        }
    }, 500);
}

// 处理答案
function processAnswer(value, text) {
    switch (state.step) {
        case 0: // 广东省户籍
            state.userData.isGuangdong = (value === 'yes');
            state.step = 1;
            askApplicationType();
            break;
            
        case 1: // 申请类型
            state.userData.applicationType = value;
            state.step = 2;
            askAge();
            break;
            
        case 2: // 年龄
            state.userData.age = (value === 'yes') ? 20 : 15;
            state.step = 3;
            askIdCard();
            break;
            
        case 3: // 身份证
            state.userData.idCardReady = (value === 'yes');
            if (value === 'yes') {
                updateChecklist('idCard', true);
            }
            state.step = 4;
            askPhotoReceipt();
            break;
            
        case 4: // 照片回执
            state.userData.photoReceipt = value;
            if (value === 'A') {
                updateChecklist('photo', true);
                askApplicationForm();
            } else {
                addAgentMessage('请问您是否已生成带条形码的回执？', [
                    { text: '是', value: 'yes' },
                    { text: '否', value: 'no' }
                ]);
            }
            state.step = 5;
            break;
            
        case 5: // 照片回执确认
            if (value === 'yes') {
                updateChecklist('photo', true);
            }
            state.step = 6;
            askApplicationForm();
            break;
            
        case 6: // 申请表
            state.userData.applicationForm = value;
            if (value === 'A' || value === 'B') {
                updateChecklist('form', true);
            }
            state.step = 7;
            askAppointment();
            break;
            
        case 7: // 预约
            state.userData.appointment = (value === 'yes');
            if (value === 'yes') {
                updateChecklist('appointment', true);
            }
            generateReport();
            break;
    }
}

// 处理文本输入
function processTextInput(text) {
    const lowerText = text.toLowerCase();
    
    // 关键词识别
    if (lowerText.includes('预约') || lowerText.includes('怎么预约')) {
        showAppointmentHelp();
    } else if (lowerText.includes('签注')) {
        showEndorsementInfo();
    } else if (lowerText.includes('重新') || lowerText.includes('开始')) {
        resetChat();
    } else if (lowerText.includes('是') || lowerText.includes('yes')) {
        processAnswer('yes', text);
    } else if (lowerText.includes('否') || lowerText.includes('no')) {
        processAnswer('no', text);
    } else {
        addAgentMessage('抱歉，我不太理解您的意思。请您选择上面的选项按钮，或者输入"是"、"否"、"A"、"B"等简单回答。');
    }
}

// 询问申请类型
function askApplicationType() {
    addAgentMessage(
        '<strong>请问本次申请是「首次办理」、「续签/换证」还是「补办（丢失）」？</strong>',
        [
            { text: '首次办理', value: 'first' },
            { text: '续签/换证', value: 'renew' },
            { text: '补办', value: 'replace' }
        ]
    );
}

// 询问年龄
function askAge() {
    addAgentMessage(
        '<strong>请问申请人是否已满16周岁？</strong>',
        [
            { text: '是', value: 'yes' },
            { text: '否', value: 'no' }
        ]
    );
}

// 询问身份证
function askIdCard() {
    addAgentMessage(
        '<strong>第一项：居民身份证原件</strong><br><br>请问您是否持有有效期内的居民身份证原件？身份证有效期是否在3个月以上？',
        [
            { text: '是', value: 'yes' },
            { text: '否', value: 'no' }
        ]
    );
}

// 询问照片回执
function askPhotoReceipt() {
    addAgentMessage(
        '<strong>第二项：照片回执（出入境证件数字相片采集回执）</strong><br><br>请问您计划如何获取照片回执：',
        [
            { text: 'A. 至大厅现场免费拍摄', value: 'A' },
            { text: 'B. 提前通过App拍摄生成回执', value: 'B' }
        ]
    );
}

// 询问申请表
function askApplicationForm() {
    addAgentMessage(
        '<strong>第三项：《中国公民出入境证件申请表》</strong><br><br>请问您计划：',
        [
            { text: 'A. 至大厅现场领取空白表格填写', value: 'A' },
            { text: 'B. 提前线上填写并打印', value: 'B' }
        ]
    );
}

// 询问预约
function askAppointment() {
    addAgentMessage(
        '<strong>第四项：预约确认（重要）</strong><br><br>龙岗出入境服务大厅实行全预约制，未预约可能无法当日办理。<br><br><strong>请问您是否已完成预约？</strong>',
        [
            { text: '是', value: 'yes' },
            { text: '否', value: 'no' }
        ]
    );
}

// 显示预约帮助
function showAppointmentHelp() {
    addAgentMessage(`
        <strong>📅 预约流程如下：</strong><br><br>
        <strong>方式一：微信小程序「深圳公安」</strong><br>
        1. 微信搜索「深圳公安」小程序并进入<br>
        2. 点击「出入境」→「出入境预约」<br>
        3. 选择「龙岗区出入境服务大厅」<br>
        4. 选择办理日期和时间段<br>
        5. 填写信息，提交预约<br>
        6. <strong>预约成功后请截图保存</strong>，办理当日需出示<br><br>
        <strong>方式二：「移民局12367」App</strong><br>
        1. 应用商店下载「移民局12367」App<br>
        2. 登录后选择「预约办证」<br>
        3. 同样选择龙岗大厅及时间段<br>
        4. 提交并截图保存<br><br>
        请问您是否需要继续材料自查？
    `, [
        { text: '继续', value: 'continue' }
    ]);
}

// 显示签注信息
function showEndorsementInfo() {
    addAgentMessage(`
        <strong>📖 签注说明</strong><br><br>
        <strong>港澳通行证 = 通行证 + 签注</strong><br><br>
        <strong>1️⃣ 通行证（本子/卡片）</strong><br>
        您的「出入资格证明」，工本费约<strong>50元</strong>。<br><br>
        <strong>2️⃣ 签注（许可次数）</strong><br>
        每次去港澳需要有签注，相当于在通行证上盖章。<br><br>
        <strong>常见签注类型：</strong><br>
        • 个人旅游（G签）- 广东户籍可办，自由行<br>
        • 三个月一次 - 约<strong>15元</strong><br>
        • 一年一次 - 约<strong>15元</strong><br>
        • 一年两次 - 约<strong>30元</strong><br><br>
        <strong>💡 建议：</strong>首次办证时可同时申请签注，一起搞定！<br><br>
        请问是否继续材料自查？
    `, [
        { text: '继续', value: 'continue' }
    ]);
}

// 生成报告
function generateReport() {
    setTimeout(() => {
        addAgentMessage(`
            <strong>📋 材料自查报告已生成</strong><br><br>
            所有材料已核查完毕，请查看左侧「材料清单」确认。<br><br>
            <strong>✅ 已准备项：</strong><br>
            ${state.checklist.idCard ? '• 居民身份证原件<br>' : ''}
            ${state.checklist.photo ? '• 照片回执<br>' : ''}
            ${state.checklist.form ? '• 申请表<br>' : ''}
            ${state.checklist.appointment ? '• 预约确认<br>' : ''}
            <br>
            <strong>⚠️ 待确认项：</strong><br>
            • 请确认已保存预约截图<br><br>
            <strong>📍 出行提醒：</strong><br>
            • 地址：深圳市龙岗区德政路6号<br>
            • 时间：周一至周六 9:00-12:00, 14:00-18:00<br>
            • 电话：0755-83195555<br>
            • 费用：工本费约50元，签注约15元/次<br><br>
            祝您办理顺利！如需帮助，请点击「重新开始」。
        `);
        
        // 更新侧边栏步骤
        updateSidebarSteps();
    }, 1000);
}

// 更新材料清单
function updateChecklist(item, checked) {
    state.checklist[item] = checked;
    const element = document.getElementById(`item-${item}`);
    if (element) {
        if (checked) {
            element.classList.add('checked');
            element.querySelector('.checkbox').textContent = '☑';
        } else {
            element.classList.remove('checked');
            element.querySelector('.checkbox').textContent = '☐';
        }
    }
}

// 更新侧边栏步骤
function updateSidebarSteps() {
    const steps = document.querySelectorAll('.guide-item');
    steps.forEach((step, index) => {
        if (index < 3) {
            step.classList.remove('active');
            step.classList.add('completed');
        }
    });
}

// 重置聊天
function resetChat() {
    state.step = 0;
    state.userData = {
        isGuangdong: null,
        applicationType: null,
        age: null,
        idCardReady: null,
        photoReceipt: null,
        applicationForm: null,
        appointment: null
    };
    state.checklist = {
        idCard: false,
        photo: false,
        form: false,
        appointment: false
    };
    
    // 重置材料清单
    ['idCard', 'photo', 'form', 'appointment'].forEach(item => {
        updateChecklist(item, false);
    });
    
    // 重置侧边栏步骤
    const steps = document.querySelectorAll('.guide-item');
    steps.forEach((step, index) => {
        step.classList.remove('completed');
        step.classList.add('active');
    });
    
    initializeChat();
}

// 滚动到底部
function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}

// 发送消息（供HTML调用）
function sendMessage(text) {
    document.getElementById('user-input').value = text;
    sendUserMessage();
}
