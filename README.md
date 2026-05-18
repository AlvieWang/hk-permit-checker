# 港澳通行证材料自查系统

模拟深圳公安出入境办事窗口的智能对话系统，帮助用户自助核查办理港澳通行证所需材料。

## 🎯 核心特性

- 🎨 **官方风格界面**：模拟深圳公安出入境服务大厅的视觉风格
- 🤖 **真正AI对话**：接入Agent API，实现智能自然语言对话
- ✅ **实时清单**：左侧边栏实时显示材料准备进度
- 📱 **响应式设计**：支持PC和移动端访问
- 🌐 **前后端分离**：前端纯静态，后端提供AI能力

## 👥 贡献者

- **Alvie Wang** - 项目创建与开发
- **YANG Yuyuan** - 贡献者
- **WANG Hongrong** - 贡献者

## 🚀 在线体验

**GitHub Pages：** https://alviewang.github.io/hk-permit-checker/

## 💡 技术架构

### 前端（GitHub Pages托管）
- HTML5
- CSS3 (Flexbox + 渐变 + 动画)
- 原生JavaScript (调用后端API)

### 后端（需单独部署）
- Python Flask
- REST API
- CORS支持跨域

## 📦 本地开发

### 1. 克隆项目
```bash
git clone https://github.com/AlvieWang/hk-permit-checker.git
cd hk-permit-checker
```

### 2. 启动后端服务
```bash
cd server
pip install -r requirements.txt
python app.py
```

后端将在 `http://localhost:5000` 启动

### 3. 启动前端
直接用浏览器打开 `index.html`，或修改 `script.js` 中的 `API_URL` 指向本地后端：
```javascript
const CONFIG = {
    API_URL: 'http://localhost:5000/api/chat',
    SESSION_ID: 'user_' + Date.now()
};
```

## 🌐 部署方案

### 方案A：纯前端（GitHub Pages）
- 前端直接部署到GitHub Pages
- 需要单独部署后端API服务
- 修改 `script.js` 中的 `API_URL` 指向你的后端地址

### 方案B：全栈部署（推荐）
- 使用Render、Railway、或Heroku部署后端
- 前端部署到GitHub Pages
- 后端提供API服务

### 免费后端托管推荐
- **Render.com** - 免费套餐，支持Flask
- **Railway.app** - 简单易用
- **Vercel** - 也支持后端函数

## 📂 文件结构

```
hk-permit-checker/
├── index.html          # 主页面（前端）
├── style.css           # 样式文件
├── script.js           # 前端逻辑（调用API）
├── README.md           # 说明文档
└── server/             # 后端服务
    ├── app.py          # Flask后端API
    └── requirements.txt # Python依赖
```

## 🎮 使用说明

1. 打开网页后，智能助手会通过AI对话逐步询问
2. 点击选项按钮或输入文字与AI交流
3. 左侧边栏会实时更新材料清单和办事指南
4. AI会根据对话内容智能判断材料准备情况
5. 完成后会生成个人材料自查报告

## 🔧 API接口

### POST /api/chat
**请求：**
```json
{
  "message": "你好",
  "session_id": "user_12345"
}
```

**响应：**
```json
{
  "reply": "您好，欢迎咨询...",
  "options": ["是", "否"],
  "progress": 10
}
```

## ⚠️ 注意事项

- 本系统仅提供材料自查参考，具体以现场要求为准
- 费用信息仅供参考，以现场实际收费为准
- 政策变动请及时关注官方通知
- 后端API需要单独部署，前端才能正常使用AI功能

## 📞 联系方式

- 深圳公安咨询电话：0755-83195555
- 全国出入境服务热线：12367

## 📝 更新日志

### v2.0 (2026-05-19)
- ✅ 接入真正AI Agent对话能力
- ✅ 重构为前后端分离架构
- ✅ 添加后端API服务
- ✅ 优化对话体验，支持自然语言

### v1.0 (2026-05-18)
- ✅ 初始版本发布
- ✅ 基础对话功能
- ✅ 部署到GitHub Pages
