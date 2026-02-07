# 发布到 GitHub Marketplace 指南

## 前置准备

### 1. 修改配置信息

在发布前，需要修改以下文件中的占位符信息：

#### `.claude-plugin/marketplace.json`

```json
{
  "owner": {
    "name": "Your Name",           // ← 改为你的名字
    "email": "your.email@example.com"  // ← 改为你的邮箱
  },
  "metadata": {
    "homepage": "https://github.com/yourusername/codePartner",  // ← 改为你的仓库地址
    "repository": "https://github.com/yourusername/codePartner"  // ← 改为你的仓库地址
  }
}
```

#### `README.md`

将所有 `yourusername` 替换为你的 GitHub 用户名。

#### `LICENSE`

可选：更新版权所有者信息。

---

## 发布步骤

### 步骤 1：推送到 GitHub

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Code Partner Skill"

# 添加远程仓库
git remote add origin https://github.com/yourusername/codePartner.git

# 推送
git push -u origin main
```

### 步骤 2：创建 Release

1. 访问你的 GitHub 仓库
2. 点击 **Releases** → **Create a new release**
3. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `Code Partner v1.0.0`
   - **Description**: 复制以下内容：

```markdown
## Code Partner v1.0.0

首个正式发布！

### 功能特性
- ✅ 技术益害评估（益处检查 + 风险评估）
- ✅ 三级风险预警机制（🟢低 / 🟡中 / 🔴高）
- ✅ 自动化优化日志系统
- ✅ 版本自动管理
- ✅ 完整的参考文档和示例

### 安装方式

#### 通过 Claude Plugin Marketplace（推荐）
```bash
/plugin marketplace add https://github.com/yourusername/codePartner
/plugin install code-partner
```

#### 手动安装
下载 `code-partner.skill` 文件，解压到 `~/.claude/skills/` 目录

### 文档
- [安装指南](https://github.com/yourusername/codePartner/blob/main/docs/installation.md)
- [使用指南](https://github.com/yourusername/codePartner/blob/main/docs/usage.md)
- [使用示例](https://github.com/yourusername/codePartner/blob/main/examples/simple-optimization.md)

### 贡献
欢迎提交 Issue 和 Pull Request！
```

4. 勾选 **Set as the latest release**
5. 点击 **Publish release**

### 步骤 3：验证安装

发布后，测试安装是否正常：

```bash
# 在 Claude Code 中
/plugin marketplace add https://github.com/yourusername/codePartner
/plugin install code-partner
```

---

## 用户安装方式

用户现在可以通过以下方式安装：

### 方式 1：Claude Plugin Marketplace

```bash
/plugin marketplace add https://github.com/yourusername/codePartner
/plugin install code-partner
```

### 方式 2：下载 .skill 文件

1. 访问 [Releases 页面](https://github.com/yourusername/codePartner/releases)
2. 下载 `code-partner.skill`
3. 解压到 `~/.claude/skills/code-partner/`

### 方式 3：从源码安装

```bash
git clone https://github.com/yourusername/codePartner.git
cp -r codePartner/skills/code-partner ~/.claude/skills/
```

---

## 更新版本

### 1. 更新版本号

```bash
# 更新 marketplace.json 中的版本号
# 例如 "version": "1.0.0" → "version": "1.1.0"
```

### 2. 创建新 Release

```bash
git tag v1.1.0
git push origin v1.1.0
```

然后在 GitHub 上创建对应 Release。

### 3. 用户更新

```bash
/plugin update code-partner
```

---

## 推广建议

### 1. 添加合适的 Topics

在 GitHub 仓库设置中添加以下 topics：
- `claude-code`
- `claude-skill`
- `code-quality`
- `development-tools`
- `logging`
- `risk-assessment`

### 2. 完善文档

确保以下文档齐全：
- ✅ README.md（项目首页）
- ✅ LICENSE（开源协议）
- ✅ docs/installation.md（安装指南）
- ✅ docs/usage.md（使用指南）
- ✅ examples/（使用示例）

### 3. 提供截图/演示

可以在 README 中添加：
- 使用演示 GIF
- 日志输出示例
- 工作流程图

### 4. 分享到社区

- Claude Code 官方论坛
- Reddit r/Claude
- 开发者社区

---

## 常见问题

### Q1: marketplace add 后找不到插件？

**A**: 检查以下几点：
1. 仓库是否为公开
2. `.claude-plugin/marketplace.json` 是否存在且格式正确
3. skills 路径是否正确

### Q2: 安装后 skill 没有自动触发？

**A**: 确保 `SKILL.md` 中的 description 清晰描述了触发场景。

### Q3: 如何验证配置正确？

**A**: 可以使用 JSON 验证工具检查 `marketplace.json` 格式：
```bash
cat .claude-plugin/marketplace.json | jq .
```

---

## 下一步

- [ ] 修改所有占位符信息
- [ ] 推送到 GitHub
- [ ] 创建首个 Release
- [ ] 测试安装流程
- [ ] 分享给社区

祝你发布顺利！🎉
