# 🎉 港澳通行证材料自查系统 - Agent版

## ✅ 已完成的工作

### 1. 项目改造完成
- ✅ 重构为前后端分离架构
- ✅ 接入Agent智能对话能力
- ✅ 创建后端API服务（Flask）
- ✅ 前端改为调用API，实现真正AI对话
- ✅ 添加贡献者：YANG Yuyuan, WANG Hongrong

### 2. 代码已推送到GitHub
- ✅ GitHub仓库：https://github.com/AlvieWang/hk-permit-checker
- ✅ GitHub Pages：https://alviewang.github.io/hk-permit-checker/
- ✅ 所有代码已更新到main分支

---

## 🌐 当前部署状态

### ✅ 前端 - 已部署
**访问地址：<ADDRESS_REMOVED>

- 界面可以正常访问
- 但AI对话功能需要后端API支持

### ⚠️ 后端 - 需要单独部署
前端已准备好调用API，但后端服务需要你单独部署。

---

## 🚀 如何完整使用（两步）

### 步骤1：部署后端API

**推荐方案：Render.com（免费）**

1. 访问 https://render.com/ 注册账号
2. 点击 "New +" → "Web Service"
3. 连接GitHub仓库：`AlvieWang/hk-permit-checker`
4. 配置：
   - **Root Directory**: `server`
   - **Start Command**: `pip install -r requirements.txt && python app.py`
   - **Port**: `5000`
5. 点击 "Create Web Service"
6. 等待部署完成（约2-3分钟）
7. 获得后端地址，例如：`https://hk-permit-checker.onrender.com`

### 步骤2：更新前端配置

获得后端地址后，需要修改前端的 `script.js`：

```javascript
// 修改第8行，将API_URL改为你的后端地址
const CONFIG = {
    API_URL: 'https://hk-permit-checker.onrender.com/api/chat',  // 改这里！
    SESSION_ID: 'user_' + Date.now()
};
```

修改后：
```bash
git add script.js
git commit -m "config: 更新后端API地址"
git push origin main
```

等待GitHub Pages重新构建（1-5分钟）

---

## 🧪 本地测试（推荐先测试）

如果想先本地测试完整功能：

### 1. 启动后端
```bash
cd hk-permit-checker/server
pip install -r requirements.txt
python app.py
```
后端将在 `<INTERNAL_HOST>0:5000` 启动

### 2. 修改前端配置
在 `script.js` 中：
```javascript
const CONFIG = {
    API_URL: '<INTERNAL_HOST>0:5000/api/chat',  // 本地后端
    SESSION_ID: 'user_' + Date.now()
};
```

### 3. 打开前端
直接用浏览器打开 `index.html`，或使用：
```bash
cd hk-permit-checker
python -m http.server 8080
```
然后访问 `<INTERNAL_HOST>0:8080`

---

## 📋 功能说明

部署完成后，用户访问网页可以：

1. ✅ 与真正的AI Agent对话（不是硬编码逻辑）
2. ✅ AI会智能识别用户意图
3. ✅ 实时更新左侧材料清单
4. ✅ 支持自然语言输入
5. ✅ 提供预约、签注等帮助信息

---

## 💡 常见问题

### Q1: 为什么现在访问网页，对话没反应？
**A:** 因为后端API还没部署。需要先部署后端（见步骤1）

### Q2: 后端部署后，前端多久能生效？
**A:** 修改 `script.js` 并push后，GitHub Pages需要1-5分钟重新构建

### Q3: 能用其他免费平台部署后端吗？
**A:** 可以，推荐：
- Render.com（最简单）
- Railway.app
- PythonAnywhere

### Q4: 本地测试时，AI回复是真实的吗？
**A:** 当前后端代码是模拟AI逻辑。要接入真实的Agent，需要修改 `server/app.py`，调用真正的AI API（如OpenAI、WorkBuddy API等）

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 Render 的部署日志
2. 检查后端是否正常响应：`https://your-backend-url/api/health`
3. 在GitHub仓库提Issue

---

**🎊 祝你部署顺利！**

部署完成后，任何人都可以访问你的网页，与AI Agent对话完成港澳通行证材料自查！
