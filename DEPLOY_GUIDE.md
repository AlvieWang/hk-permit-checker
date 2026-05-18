# 港澳通行证材料自查系统 - 部署指南

## 📚 系统版本说明

本项目提供**两个版本**的后端API：

### 1. 离线版本（`app_offline.py`） - 推荐使用
- ✅ **完全免费**，无需API密钥
- ✅ **不依赖网络**，稳定可靠
- ✅ **响应快速**，基于规则引擎
- ✅ **功能完善**，覆盖常见办理场景

### 2. AI版本（`app_ai.py`）
- 🤖 使用**Groq免费API**（需注册获取密钥）
- 🧠 **更智能**，可理解复杂问题
- 🌐 **依赖网络**，需要API调用
- 💰 免费额度足够个人使用

---

## 🚀 快速部署（离线版本 - 推荐）

### 步骤1：在PythonAnywhere上部署

1. **登录PythonAnywhere**：https://www.pythonanywhere.com/

2. **打开Bash控制台**，执行以下命令：
```bash
# 进入主目录
cd ~

# 克隆代码仓库
git clone https://github.com/AlvieWang/hk-permit-checker.git

# 进入后端目录
cd hk-permit-checker/server

# 检查Flask是否已安装（应该已预装）
python3 -c "import flask; print(flask.__version__)"
# 如果显示版本号（如3.0.3），说明已安装

# 如果Flask未安装，运行：
# pip install --user flask
```

3. **创建Web应用**：
   - 进入 **Web** 选项卡
   - 点击 **Add a new web app**
   - 选择 **Manual configuration**
   - 选择 **Python 3.9** 或更高版本
   - 点击 **Next**

4. **配置WSGI文件**：
   - 在Web应用配置页面，找到 **Code** 部分
   - 点击 **WSGI configuration file** 的链接（通常像 `/var/www/你的用户名_pythonanywhere_com_wsgi.py`）
   - 删除原有内容，替换为以下代码：

```python
import sys
import os

# 添加项目路径到Python路径
path = '/home/你的用户名/hk-permit-checker/server'
if path not in sys.path:
    sys.path.append(path)

# 设置环境变量（可选，如果需要使用AI版本）
# os.environ['GROQ_API_KEY'] = '你的Groq_API密钥'

# 导入Flask应用（离线版本）
from app_offline import app as application

# 如果需要使用AI版本，改为：
# from app_ai import app as application
```

**注意**：将代码中的`你的用户名`替换为你的PythonAnywhere用户名（如`alviewang`）

5. **设置虚拟环境（可选）**：
   - 在Web应用配置页面，找到 **Virtualenv** 部分
   - 如果Flask已安装在用户目录，可以留空
   - 如果需要独立环境，点击 **Enter a virtualenv** 并创建

6. **重新加载Web应用**：
   - 滚动到页面顶部
   - 点击 **Reload** 按钮（绿色按钮）
   - 等待10-30秒

7. **测试API是否正常**：
```bash
curl http://你的用户名.pythonanywhere.com/api/health
```
应该返回：
```json
{
  "status": "ok",
  "service": "hk-permit-checker-api-offline",
  "version": "2.0-offline"
}
```

### 步骤2：更新前端配置

1. **修改`script.js`**：
   打开`script.js`文件，确认API_URL配置正确：
```javascript
const CONFIG = {
    API_URL: 'http://你的用户名.pythonanywhere.com/api/chat',
    SESSION_ID: 'user_' + Date.now()
};
```

2. **提交并推送**：
```bash
cd /path/to/hk-permit-checker
git add script.js
git commit -m "config: 更新API地址"
git push origin main
```

3. **等待GitHub Pages部署**（约1-5分钟）

### 步骤3：测试完整功能

1. **访问前端页面**：
   ```
   https://你的GitHub用户名.github.io/hk-permit-checker/
   ```

2. **测试对话功能**：
   - 打开页面，应该看到欢迎消息
   - 点击"是"按钮
   - 继续对话，检查是否正常响应

3. **检查浏览器控制台**（按F12）：
   - 查看Network选项卡，确认API请求成功（状态码200）
   - 如果有错误，检查CORS配置

---

## 🤖 部署AI版本（可选）

如果您想使用AI版本（需要Groq API密钥）：

### 步骤1：获取免费Groq API密钥

1. 访问 https://console.groq.com/
2. 注册账号（免费）
3. 进入API Keys页面
4. 创建新的API密钥
5. 复制密钥（以`gsk_`开头）

**免费额度**：
- 每分钟30次请求
- 每天14400次请求
- 足够个人使用和测试

### 步骤2：配置API密钥

**方法1：通过环境变量（推荐）**

在PythonAnywhere的 **Web** 选项卡中：
1. 找到 **Environment variables** 部分
2. 添加变量：
   - Name: `GROQ_API_KEY`
   - Value: `你的Groq API密钥`
3. 点击 **Save**，然后 **Reload**

**方法2：通过WSGI文件**

在WSGI文件中添加：
```python
import os
os.environ['GROQ_API_KEY'] = '你的Groq API密钥'
```

### 步骤3：切换到AI版本

修改WSGI文件，将：
```python
from app_offline import app as application
```
改为：
```python
from app_ai import app as application
```

然后点击 **Reload**。

### 步骤4：测试AI版本

访问前端页面，测试对话。AI版本应该能更智能地理解复杂问题。

**注意**：如果API调用失败，系统会自动切换到离线模式。

---

## 🔧 故障排除

### 问题1：API返回404错误

**原因**：WSGI文件配置错误

**解决**：
1. 检查WSGI文件路径是否正确
2. 确认项目已克隆到正确位置（`~/hk-permit-checker/server/`）
3. 检查WSGI文件中的路径是否正确

### 问题2：CORS错误（浏览器控制台显示）

**原因**：跨域请求被阻止

**解决**：
1. 确认`app_offline.py`或`app_ai.py`中已包含CORS处理代码
2. 重新加载Web应用
3. 清除浏览器缓存（Ctrl+Shift+R）

### 问题3：前端无法连接后端

**原因**：API_URL配置错误

**解决**：
1. 检查`script.js`中的API_URL是否正确
2. 确认PythonAnywhere的Web应用已启动（绿色图标）
3. 直接访问API地址，检查是否返回JSON

### 问题4：AI版本不工作

**原因**：API密钥未配置或无效

**解决**：
1. 检查环境变量是否设置正确
2. 访问 `/api/health` 端点，检查`ai_enabled`字段
3. 查看PythonAnywhere的 **Error logs**

---

## 📊 版本对比

| 功能 | 离线版本 | AI版本 |
|------|----------|--------|
| 需要API密钥 | ❌ 不需要 | ✅ 需要（免费） |
| 网络依赖 | ❌ 不依赖 | ✅ 依赖 |
| 回复质量 | ⭐⭐⭐ 基于规则 | ⭐⭐⭐⭐⭐ 智能理解 |
| 响应速度 | ⚡ 快速（<100ms） | 🐢 较慢（1-3秒） |
| 稳定性 | ✅ 高 | ⚠️ 依赖API服务 |
| 推荐场景 | 生产环境 | 测试/演示 |

---

## 🎯 推荐部署方案

**对于生产环境**：
- 使用 **离线版本**（`app_offline.py`）
- 稳定、快速、不依赖外部服务

**对于测试/演示**：
- 使用 **AI版本**（`app_ai.py`）
- 更智能，可以展示AI能力

**混合方案**：
- 主用离线版本
- 在WSGI文件中添加降级逻辑：
```python
try:
    from app_ai import app as application
    print("✅ 使用AI版本")
except Exception as e:
    print(f"⚠️ AI版本加载失败：{e}")
    from app_offline import app as application
    print("✅ 降级到离线版本")
```

---

## 📞 获取帮助

如果遇到问题，可以：
1. 查看PythonAnywhere的 **Error logs**
2. 在GitHub仓库提Issue
3. 检查浏览器控制台错误信息

---

**祝您部署顺利！** 🎉
