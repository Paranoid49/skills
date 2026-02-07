# 安装指南

## 方法一：通过 Claude Plugin Marketplace 安装（推荐）

### 1. 添加 Marketplace 源

在 Claude Code 中执行：

```bash
/plugin marketplace add https://github.com/yourusername/codePartner
```

### 2. 安装插件

```bash
/plugin install code-partner
```

### 3. 验证安装

安装成功后，在执行任何代码任务时，`code-partner` skill 会自动触发并进行技术益害评估。

---

## 方法二：手动安装

### 步骤 1：下载 Skill 文件

从 [GitHub Releases](https://github.com/yourusername/codePartner/releases) 下载最新的 `code-partner.skill` 文件。

### 步骤 2：安装 Skill

**Windows:**
```bash
mkdir %USERPROFILE%\.claude\skills\code-partner
expand code-partner.skill -F:* %USERPROFILE%\.claude\skills\code-partner\
```

**Linux/Mac:**
```bash
mkdir -p ~/.claude/skills/code-partner
unzip code-partner.skill -d ~/.claude/skills/code-partner
```

### 步骤 3：验证安装

```bash
ls ~/.claude/skills/code-partner/SKILL.md
# 或 Windows: dir %USERPROFILE%\.claude\skills\code-partner\SKILL.md
```

---

## 方法三：从源码安装

### 步骤 1：克隆仓库

```bash
git clone https://github.com/yourusername/codePartner.git
cd codePartner
```

### 步骤 2：复制 Skill 目录

**Windows:**
```bash
xcopy /E /I skills\code-partner %USERPROFILE%\.claude\skills\code-partner
```

**Linux/Mac:**
```bash
cp -r skills/code-partner ~/.claude/skills/
```

### 步骤 3：设置权限（Linux/Mac）

```bash
chmod +x ~/.claude/skills/code-partner/scripts/*.py
```

---

## 安装后配置

### 1. 创建日志目录

```bash
mkdir -p project_logs/optimization
```

### 2. 测试日志脚本

```bash
python skills/code-partner/scripts/log_change.py \
  --type "测试" \
  --purpose "测试安装是否成功"
```

### 3. 查看日志

```bash
cat project_logs/optimization/$(date +%Y-%m-%d).md
```

---

## 验证安装成功

安装完成后，在 Claude Code 中测试：

```
用户：帮我优化这个函数的性能
```

Claude 应该会自动响应类似：

```
【技术益害评估】
益处：提升性能
风险：🟢 低风险

正在执行优化...
```

---

## 卸载

### 通过 Plugin Marketplace

```bash
/plugin uninstall code-partner
```

### 手动卸载

```bash
# Windows
rmdir /S /Q %USERPROFILE%\.claude\skills\code-partner

# Linux/Mac
rm -rf ~/.claude/skills/code-partner
```

---

## 常见问题

### Q1: 安装后 skill 没有自动触发？

**A**: 检查以下几点：
1. 确认 `SKILL.md` 文件存在且格式正确
2. 检查 description 字段是否明确描述了触发场景
3. 重启 Claude Code

### Q2: marketplace add 失败？

**A**: 确保：
1. GitHub 仓库是公开的
2. `.claude-plugin/marketplace.json` 文件存在且格式正确
3. 网络连接正常

### Q3: 如何更新到最新版本？

**A**:
```bash
/plugin update code-partner
```

或手动下载最新版本覆盖安装。

---

## 下一步

安装完成后，建议阅读：
- [使用指南](usage.md)
- [使用示例](../examples/simple-optimization.md)
