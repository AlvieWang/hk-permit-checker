# 部署指南

本文档说明如何完整部署港澳通行证材料自查系统（包含前端和后端）。

## 📋 部署架构

```
用户浏览器
    ↓
前端（GitHub Pages）
    ↓ AJAX请求
后端API（需要单独部署）
    ↓
AI Agent处理逻辑
```

## 🌐 前端部署（GitHub Pages）

前端已自动部署到GitHub Pages：
- **访问地址：** https://alviewang.github.io/hk-permit-checker/
- **自动更新：** 每次push到main分支，GitHub会自动重新构建

### 前端配置

在使用前，需要修改 `script.js` 中的API地址：

```javascript
// 方法1：使用环境变量（推荐）
const CONFIG = {
    API_URL: window.location.protocol + '//' + window.location.host + '/api/chat',
    SESSION_ID: 'user_' + Date.now()
};

// 方法2：硬编码后端地址（简单但不灵活）
const CONFIG = {
    API_URL: 'https://your-backend.onrender.com/api/chat',  // 改为你的后端地址
    SESSION_ID: 'user_' + Date.now()
};
```

## 🖥️ 后端部署（选择其一）

### 方案A：Render.com（推荐 - 免费）

1. **注册账号：** https://render.com/
2. **创建Web Service**
   - 连接GitHub仓库：`AlvieWang/hk-permit-checker`
   - 选择 `server` 目录作为根目录
   - 运行命令：`pip install -r requirements.txt && python app.py`
   - 端口：`5000`

3. **环境变量（可选）**
   - `PORT`: `5000`
   - `FLASK_ENV`: `production`

4. **获取后端地址**
   - 部署成功后，Render会提供类似 `https://hk-permit-checker.onrender.com` 的地址
   - 将这个地址填入前端的 `script.js` 中

### 方案B：Railway.app

1. **注册账号：** https://railway.app/
2. **部署**
   - 连接GitHub仓库
   - 选择 `server` 目录
   - Railway会自动检测Flask应用

### 方案C：PythonAnywhere（免费）

1. **注册账号：** https://www.pythonanywhere.com/
2. **上传代码**
   - 使用Files选项卡上传 `server` 目录
   - 或使用Bash控制台git clone

3. **配置Web应用**
   - 进入Web选项卡
   - 添加新Web应用
   - 选择Flask
   - 配置WSGI配置文件

## 🧪 本地测试

### 1. 启动后端
```bash
cd server
pip install -r requirements.txt
python app.py
```
后端将在 `http://localhost:5000` 启动

### 2. 启动前端
**方法1：直接打开**
```bash
open index.html
```

**方法2：使用简单的HTTP服务器**
```bash
# Python 3
python -m http.server 8080

# 然后访问 http://localhost:8080
```

**注意：** 需要修改 `script.js` 中的 `API_URL` 为 `http://localhost:5000/api/chat`

## 🔧 故障排除

### 问题1：前端无法连接后端
**原因：** CORS策略限制
**解决：** 后端已配置CORS，如还有问题，检查后端是否正常运行

### 问题2：GitHub Pages显示404
**原因：** GitHub Pages还在构建中
**解决：** 等待1-5分钟，或检查仓库设置中的Pages配置

### 问题3：后端部署失败
**原因：** 依赖安装失败或端口配置错误
**解决：**
- 检查 `requirements.txt` 是否正确
- 确保监听 `0.0.0.0:5000`（Render需要）
- 查看部署日志

## 📝 完整部署检查清单

- [ ] 后端代码已推送到GitHub
- [ ] 后端已部署到Render/Railway等平台
- [ ] 获得后端公开访问地址
- [ ] 修改前端 `script.js` 中的 `API_URL`
- [ ] 前端已推送到GitHub（触发GitHub Pages重新构建）
- [ ] 等待GitHub Pages构建完成（1-5分钟）
- [ ] 测试完整功能

## 💡 提示

1. **免费后端服务的限制**
   - Render免费版会在15分钟无活动后休眠
   - 第一次访问可能需要等待30秒唤醒

2. **自定义域名**
   - GitHub Pages支持自定义域名
   - Render也支持自定义域名

3. **HTTPS**
   - GitHub Pages自动提供HTTPS
   - Render也自动提供HTTPS

## 📞 需要帮助？

如果遇到部署问题，可以：
1. 查看Render/Railway的部署日志
2. 在GitHub仓库提Issue
3. 联系项目负责人

---
**祝部署顺利！** 🎉
