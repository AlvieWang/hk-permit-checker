// 港澳通行证材料自查系统 - 智能对话版
// 调用后端Agent API实现真正的人工智能对话

// 配置
const CONFIG = {
    API_URL: 'http://alviewang.pythonanywhere.com/api/chat',  // 后端API地址（PythonAnywhere）
    SESSION_ID: 'user_' + Date.now()  // 生成唯一会话ID
};

// 状态管理
const state = {
    step: 0,
    checklist: {
        idCard: false,
        photo: false,
        form: false,
        appointment: false
    },
    isWaiting: false  // 是否正在等待AI回复
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
    const timeElem = document.getElementById('current-time');
    if (timeElem) {
        timeElem.textContent = timeStr;
    }
}

// 初始化
window.onload = function() {
    updateTime();
    setInterval(updateTime, 1000);
    initializeChat();
};

// 初始化聊天
async function initializeChat() {
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        messagesContainer.innerHTML = '';
    }
    
    // 显示加载动画
    showTypingIndicator();
    
    // 调用AI Agent获取欢迎消息
    try {
        const response = await callAgentAPI('你好');
        hideTypingIndicator();
        addAgentMessage(response.reply, response.options, response.progress);
    } catch (error) {
        hideTypingIndicator();
        // 如果API调用失败，使用默认欢迎消息
        addAgentMessage(
            '您好，欢迎咨询港澳通行证办理业务。我将通过几个问题帮助您核查所需材料是否齐全。请您回答以下问题：<br><br><strong>请问您的户籍所在地是否为广东省？</strong>',
            ['是', '否']
        );
    }
}

// 调用Agent API
async function callAgentAPI(message) {
    try {
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: CONFIG.SESSION_ID
            })
        });
        
        if (!response.ok) {
            throw new Error('API调用失败');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API调用错误：', error);
        throw error;
    }
}

// 添加Agent消息
function addAgentMessage(text, options = null, progress = 0) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    let optionsHTML = '';
    if (options && options.length > 0) {
        optionsHTML = '<div class="message-options">';
        options.forEach(opt => {
            optionsHTML += `<button class="option-btn" onclick="handleOption('${opt}')">${opt}</button>`;
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
    
    // 更新进度条
    if (progress > 0) {
        updateProgress(progress);
    }
}

// 添加用户消息
function addUserMessage(text) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
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
async function handleOption(value) {
    addUserMessage(value);
    
    // 禁用所有按钮，防止重复点击
    disableOptionButtons();
    
    // 显示AI正在输入
    showTypingIndicator();
    state.isWaiting = true;
    
    try {
        // 调用AI Agent
        const response = await callAgentAPI(value);
        
        // 隐藏输入指示器
        hideTypingIndicator();
        state.isWaiting = false;
        
        // 显示AI回复
        addAgentMessage(response.reply, response.options, response.progress);
        
        // 更新材料清单（根据AI回复内容智能判断）
        updateChecklistFromReply(response.reply);
        
    } catch (error) {
        hideTypingIndicator();
        state.isWaiting = false;
        
        // 显示错误信息
        addAgentMessage('抱歉，系统暂时无法连接，请稍后再试。', ['重新开始']);
        console.error('Agent调用失败：', error);
    }
}

// 处理文本输入
async function sendUserMessage() {
    const input = document.getElementById('user-input');
    if (!input) return;
    
    const text = input.value.trim();
    if (!text || state.isWaiting) return;
    
    addUserMessage(text);
    input.value = '';
    
    // 显示AI正在输入
    showTypingIndicator();
    state.isWaiting = true;
    
    try {
        // 调用AI Agent
        const response = await callAgentAPI(text);
        
        // 隐藏输入指示器
        hideTypingIndicator();
        state.isWaiting = false;
        
        // 显示AI回复
        addAgentMessage(response.reply, response.options, response.progress);
        
        // 更新材料清单
        updateChecklistFromReply(response.reply);
        
    } catch (error) {
        hideTypingIndicator();
        state.isWaiting = false;
        
        addAgentMessage('抱歉，系统暂时无法连接，请稍后再试。', ['重新开始']);
        console.error('Agent调用失败：', error);
    }
}

// 回车发送
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendUserMessage();
    }
}

// 快捷操作
async function quickAction(action) {
    await handleOption(action);
}

// 显示输入指示器
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const typingHTML = `
        <div class="message agent-message" id="typing-indicator">
            <div class="message-avatar">🧑💼</div>
            <div class="message-content">
                <div class="message-header">
                    <strong>出入境业务助手</strong>
                    <span class="time">正在输入...</span>
                </div>
                <div class="message-text">
                    <div class="typing-animation">
                        <span>.</span><span>.</span><span>.</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    messagesContainer.insertAdjacentHTML('beforeend', typingHTML);
    scrollToBottom();
}

// 隐藏输入指示器
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// 禁用选项按钮
function disableOptionButtons() {
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.5';
        btn.style.cursor = 'not-allowed';
    });
}

// 更新材料清单（根据AI回复智能判断）
function updateChecklistFromReply(reply) {
    // 身份证
    if (reply.includes('身份证') && (reply.includes('✅') || reply.includes('已准备'))) {
        updateChecklist('idCard', true);
    }
    
    // 照片回执
    if (reply.includes('照片回执') && (reply.includes('✅') || reply.includes('已准备'))) {
        updateChecklist('photo', true);
    }
    
    // 申请表
    if (reply.includes('申请表') && (reply.includes('✅') || reply.includes('已准备'))) {
        updateChecklist('form', true);
    }
    
    // 预约
    if (reply.includes('预约') && (reply.includes('✅') || reply.includes('已准备'))) {
        updateChecklist('appointment', true);
    }
}

// 更新材料清单显示
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

// 更新进度条
function updateProgress(progress) {
    // 可以在这里添加进度条更新逻辑
    console.log('当前进度：', progress + '%');
}

// 滚动到底部
function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }
}

// 发送消息（供HTML调用）
function sendMessage(text) {
    const input = document.getElementById('user-input');
    if (input) {
        input.value = text;
        sendUserMessage();
    }
}
