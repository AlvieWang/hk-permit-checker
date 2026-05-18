# PythonAnywhere 部署指南

本文档说明如何将后端部署到 PythonAnywhere（完全免费，无需信用卡）。

## ✅ 为什么选择 PythonAnywhere？

| 优势 | 说明 |
|------|------|
| **无需信用卡** | ✅ 注册即用，零风险 |
| **免费套餐** | ✅ 支持1个Web应用，永久免费 |
| **支持内地访问** | ✅ 国内网络可正常访问 |
| **部署简单** | ✅ 图形界面，无需命令行 |
| **支持Flask** | ✅ 原生支持Python WSGI应用 |

---

## 🚀 部署步骤（15分钟完成）

### 步骤1：注册 PythonAnywhere 账号

1. 访问：https://www.pythonanywhere.com/
2. 点击 **"Create a Beginner account"**（免费版）
3. 填写信息：
   - **Username**: 你的用户名
   - **Email**: 邮箱（用于验证）
   - **Password**: 密码
4. 验证邮箱
5. 登录控制台

---

### 步骤2：上传代码

**方法A：通过Web界面上传（推荐新手）**

1. 访问：https://www.pythonanywhere.com/
2. 登录后，进入 **"Files"** 选项卡
3. 点击 **"Upload a file"**
4. 将以下文件打包成 `server.zip` 并上传：
   - `app.py`
   - `requirements.txt`
5. 上传后，在Files选项卡中解压zip文件

**方法B：通过Bash控制台上传（推荐）**

1. 进入 **"Consoles"** 选项卡
2. 点击 **"Start a new console"** → 选择 **"Bash"**
3. 在Bash中执行：

```bash
# 克隆GitHub仓库
cd ~
git clone https://github.com/AlvieWang/hk-permit-checker.git

# 进入server目录
cd hk-permit-checker/server
```

---

### 步骤3：安装依赖

在 **Bash控制台** 中执行：

```bash
# 进入项目目录
cd ~/hk-permit-checker/server

# 安装依赖（使用清华镜像源，速度快）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

---

### 步骤4：创建Web应用

1. 进入 **"Web"** 选项卡
2. 点击 **"Add a new web app"**
3. 点击 **"Next"**
4. 选择 **"Flask"**
5. 选择 **Python版本**：`Python 3.9`
6. 配置WSGI文件：
   - **Source code**: `/home/你的用户名/hk-permit-checker/server`
   - **WSGI configuration file**: 保持默认
7. 点击 **"Next"**

---

### 步骤5：配置 WSGI 文件

1. 在 **"Web"** 选项卡中，找到 **"WSGI configuration file"**
2. 点击链接（通常是 `/var/www/你的用户名_pythonanywhere_com_wsgi.py`）
3. 修改这个文件，替换为以下内容：

```python
import sys
import os

# 添加项目路径到sys.path
project_home = '/home/你的用户名/hk-permit-checker/server'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入app
from app import app as application  # Flask的app对象

# 用于调试
if __name__ == '__main__':
    application.run()
```

**注意：** 将 `你的用户名` 替换为你的PythonAnywhere用户名！

4. 点击 **"Save"**

---

### 步骤6：修改 app.py（适配 PythonAnywhere）

PythonAnywhere不支持动态端口，需要修改 `app.py`：

在文件末尾，将：

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

改为：

```python
if __name__ == '__main__':
    # PythonAnywhere 会自动处理端口
    app.run()
```

---

### 步骤7：启动 Web 应用

1. 回到 **"Web"** 选项卡
2. 点击 **"Reload 你的用户名.pythonanywhere.com"**
3. 等待10-20秒
4. 点击页面中的链接，例如：
   ```
   http://你的用户名.pythonanywhere.com
   ```

---

### 步骤8：测试后端 API

访问以下URL测试：

#### 1. 健康检查

在浏览器访问：
```
http://你的用户名.pythonanywhere.com/api/health
```

应返回：
```json
{
  "status": "ok",
  "service": "hk-permit-checker-api"
}
```

#### 2. 测试对话 API

使用 curl 或 Postman 测试：

```bash
curl -X POST http://你的用户名.pythonanywhere.com/api/chat \
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

获得后端地址后，需要修改前端的 `script.js`：

### 1. 修改配置

打开 `script.js`，找到第8行：

```javascript
const CONFIG = {
    API_URL: window.location.origin + '/api/chat',  // 需要修改
    SESSION_ID: 'user_' + Date.now()
};
```

改为你的后端地址：

```javascript
const CONFIG = {
    API_URL: 'http://你的用户名.pythonanywhere.com/api/chat',  // 改这里
    SESSION_ID: 'user_' + Date.now()
};
```

### 2. 提交并推送

```bash
cd /Users/alvie/WorkBuddy/20260427142912/hk-permit-checker
git add script.js
git commit -m "config: 更新后端API地址为PythonAnywhere"
git push origin main
```

### 3. 等待 GitHub Pages 重新构建

- 约1-5分钟后，GitHub Pages会自动重新构建
- 访问：https://alviewang.github.io/hk-permit-checker/ 测试

---

## 🐛 故障排除

### 问题1：访问后端显示 404

**原因：** WSGI配置错误

**解决：**
1. 检查WSGI文件中的项目路径是否正确
2. 确保 `from app import app as application` 这行没有错误
3. 查看 **"Web"** 选项卡中的 **"Error log"**

### 问题2：依赖安装失败

**原因：** 网络问题或包不存在

**解决：**
1. 使用清华镜像源：
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```
2. 检查 `requirements.txt` 中的包名是否正确

### 问题3：前端无法连接后端（CORS错误）

**原因：** CORS配置错误

**解决：**
1. 确保 `app.py` 中有 `CORS(app)`
2. 如果还有问题，可以尝试允许所有域名：
   ```python
   CORS(app, resources={r"/*": {"origins": "*"}})
   ```

### 问题4：修改代码后不生效

**原因：** 没有重新加载Web应用

**解决：**
1. 进入 **"Web"** 选项卡
2. 点击 **"Reload"** 按钮

---

## 📝 补充说明

### 免费版限制

PythonAnywhere 免费版有以下限制：
- **Web应用数量**：1个
- **CPU时间**：每天100秒
- **存储空间**：500MB
- **数据库**：MySQL 100MB（可选）

**对于你的项目，这些限制完全够用！**

### 自定义域名（可选）

如果想使用自己的域名：
1. 在 **"Web"** 选项卡中找到 **"Domains"** 部分
2. 添加你的域名
3. 在域名服务商处添加 CNAME 记录

---

## ✅ 部署检查清单

- [ ] PythonAnywhere 账号已注册
- [ ] 代码已上传到 PythonAnywhere
- [ ] 依赖已成功安装（无错误）
- [ ] Web应用已创建
- [ ] WSGI文件已正确配置
- [ ] `/api/health` 端点可正常访问
- [ ] `/api/chat` 端点可正常对话
- [ ] 前端 `script.js` 已更新后端地址
- [ ] 代码已推送到 GitHub
- [ ] GitHub Pages 已重新构建
- [ ] 访问网页可正常与 AI 对话

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 PythonAnywhere 的 **"Error log"**
2. 查看 [PythonAnywhere 官方文档](https://help.pythonanywhere.com/)
3. 在GitHub仓库提 Issue

---

**🎉 祝你部署顺利！**

部署完成后，任何人都可以访问你的网页，与 AI Agent 对话完成港澳通行证材料自查！
