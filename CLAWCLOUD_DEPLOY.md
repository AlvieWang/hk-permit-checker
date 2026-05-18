# 🚀 ClawCloud 部署指南

本文档说明如何将后端部署到 ClawCloud（完全免费，无需信用卡）。

## ✅ 为什么选择 ClawCloud？

| 优势 | 说明 |
|------|------|
| **无需信用卡** | ✅ 注册即用，零风险 |
| **免费配置高** | ✅ 4核CPU + 8G内存 + 10G磁盘 |
| **支持内地访问** | ✅ 国内网络可正常访问 |
| **永久免费** | ✅ 不是试用期，是真正永久免费 |
| **支持Docker** | ✅ 一键部署Docker镜像 |

---

## 📋 部署步骤

### 步骤1：注册 ClawCloud 账号

1. 访问：https://console.claw.cloud/
2. 点击 **"Sign Up"** 注册
3. **推荐使用 GitHub 账号登录**（无需信用卡！）
4. 完成邮箱验证

### 步骤2：创建应用

1. 登录后，进入控制台
2. 点击 **"Create App"** 或 **"Create Service"**
3. 选择部署方式：**"Deploy from Dockerfile"**

### 步骤3：上传代码

**方法A：连接 GitHub（推荐）**

1. 在 ClawCloud 中连接你的 GitHub 账号
2. 选择仓库：`AlvieWang/hk-permit-checker`
3. 选择分支：`main`
4. 设置根目录：`server/`

**方法B：手动上传（备选）**

1. 将 `server/` 目录打包成 zip
2. 在 ClawCloud 中选择 "Upload"
3. 上传 zip 文件

### 步骤4：配置应用

在 ClawCloud 控制台填写：

| 配置项 | 值 |
|--------|------|
| **App Name** | `hk-permit-checker` |
| **Port** | `5000` |
| **Region** | `US West`（美西，免费额度更高） |
| **Build Command** | （留空，自动识别 Dockerfile） |
| **Run Command** | （留空，使用 Dockerfile 中的 CMD） |

### 步骤5：部署

1. 点击 **"Create"** 或 **"Deploy"**
2. 等待构建（约 2-3 分钟）
3. 查看构建日志，确保无错误
4. 部署成功后，获得访问地址

示例地址：
```
https://hk-permit-checker-xxxxxx.clawcloud.dev
```

---

## 🔧 测试后端

部署成功后，测试API是否正常：

### 1. 健康检查

在浏览器访问：
```
https://your-app-url.clawcloud.dev/api/health
```

应返回：
```json
{
  "status": "ok",
  "service": "hk-permit-checker-api"
}
```

### 2. 测试对话API

使用 curl 或 Postman 测试：

```bash
curl -X POST https://your-app-url.clawcloud.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "test123"}'
```

应返回：
```json
{
  "reply": "您好，欢迎咨询港澳通行证办理业务...",
  "options": ["是", "否"],
  "progress": 10
}
```

---

## 🔗 连接前端

获得后端地址后，需要修改前端配置：

### 1. 修改 `script.js`

打开 `script.js`，找到第 8 行：

```javascript
const CONFIG = {
    API_URL: window.location.origin + '/api/chat',  // 需要修改
    SESSION_ID: 'user_' + Date.now()
};
```

改为你的后端地址：

```javascript
const CONFIG = {
    API_URL: 'https://hk-permit-checker-xxxxxx.clawcloud.dev/api/chat',  // 改这里
    SESSION_ID: 'user_' + Date.now()
};
```

### 2. 提交并推送

```bash
cd /Users/alvie/WorkBuddy/20260427142912/hk-permit-checker
git add script.js
git commit -m "config: 更新后端API地址为ClawCloud"
git push origin main
```

### 3. 等待 GitHub Pages 重新构建

- 约 1-5 分钟后，GitHub Pages 会自动重新构建
- 访问：https://alviewang.github.io/hk-permit-checker/ 测试

---

## 🐛 故障排除

### 问题1：构建失败

**可能原因：**
- Dockerfile 语法错误
- requirements.txt 中的包不存在
- 端口配置错误

**解决方法：**
1. 查看 ClawCloud 的构建日志
2. 确保在 Dockerfile 中暴露了端口 5000
3. 确保 `app.py` 监听 `0.0.0.0:5000`

### 问题2：前端无法连接后端

**可能原因：**
- CORS 配置错误
- 后端地址配置错误
- 后端服务未正常运行

**解决方法：**
1. 检查 `app.py` 中是否有 `CORS(app)`
2. 确认前端 `CONFIG.API_URL` 配置正确
3. 访问 `/api/health` 端点检查后端状态

### 问题3：访问速度慢

**原因：** ClawCloud 免费版可能在海外，内地访问较慢

**解决方法：**
- 选择 Region 为 `US West`（相对较快）
- 或考虑使用国内平台（如腾讯云云开发）

---

## 📝 补充说明

### 免费额度限制

ClawCloud 免费版有以下限制：
- **CPU**：4 核
- **内存**：8GB
- **磁盘**：10GB
- **流量**：每月 10GB
- **休眠策略**：15 分钟无活动后可能休眠（访问时自动唤醒）

### 自定义域名（可选）

如果想使用自己的域名：
1. 在 ClawCloud 控制台添加域名
2. 添加 CNAME 记录指向 ClawCloud 提供的地址
3. 等待 DNS 生效（约 10 分钟）

---

## ✅ 部署检查清单

- [ ] ClawCloud 账号已注册
- [ ] 应用已创建并部署成功
- [ ] `/api/health` 端点可正常访问
- [ ] `/api/chat` 端点可正常对话
- [ ] 前端 `script.js` 已更新后端地址
- [ ] 代码已推送到 GitHub
- [ ] GitHub Pages 已重新构建
- [ ] 访问网页可正常与 AI 对话

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 ClawCloud 的部署日志
2. 在 GitHub 仓库提 Issue
3. 联系项目负责人

---

**🎉 祝你部署顺利！**

部署完成后，任何人都可以访问你的网页，与 AI Agent 对话完成港澳通行证材料自查！
