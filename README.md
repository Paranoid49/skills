# Code Skills - Claude 代码助手技能集合

> Claude Code 技能插件集合，包含 code-partner 和 code-documenter 两个独立技能。

> ⚠️ **注意**：本项目仅在 Windows 11 下测试通过。

## 📦 技能列表

### 1. code-partner - 资深编程伙伴

让 Claude 成为项目的"守门员"，对代码变更进行技术益害评估，维护优化日志。

- **技术益害评估**：每次变更前自动进行益处检查和风险评估
- **风险预警机制**：对潜在隐患发出警告并提供替代方案
- **优化日志系统**：自动记录所有变更，包含目的、内容和验证标准
- **版本管理**：自动递增版本号，追踪每次修改

### 2. code-documenter - 项目文档生成器

自动分析项目代码和文档，生成结构化的学习文档。

- **项目分析**：自动扫描代码结构，识别模块依赖关系
- **文档生成**：生成包含架构图、流程图、模块详解的学习文档
- **可视化图表**：使用 Mermaid 生成清晰的流程图和架构图

## 📁 项目结构

```
codePartner/
├── skills/
│   ├── code-partner/            # 资深编程伙伴技能
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── RISK_ASSESSMENT.md
│   │   │   └── LOG_TEMPLATE.md
│   │   └── scripts/
│   │       └── log_change.py
│   │
│   └── code-documenter/         # 文档生成器技能
│       ├── SKILL.md
│       ├── references/
│       │   ├── DOCUMENT_TEMPLATE.md
│       │   └── DIAGRAM_STYLES.md
│       └── scripts/
│           ├── analyze_project.py
│           └── generate_docs.py
│
├── examples/                    # code-partner 使用示例
├── docs/                        # 详细文档
├── project_logs/                # code-partner 运行时日志目录
└── README.md
```

## 🚀 快速开始

### 通过 Claude Plugin Marketplace 安装（推荐）

```bash
# 1. 添加 Marketplace 源
/plugin marketplace add Paranoid49/skills

# 2. 安装技能（可单独安装或全部安装）
/plugin install code-partner      # 资深编程伙伴
/plugin install code-documenter   # 文档生成器
```

## 📚 详细文档

### code-partner

- [完整使用指南](docs/usage.md)
- [风险评估详解](docs/risk_assessment.md)
- [日志格式规范](docs/log_format.md)
- [使用示例](examples/)

### code-documenter

- [技能说明](skills/code-documenter/SKILL.md)
- [文档模板](skills/code-documenter/references/DOCUMENT_TEMPLATE.md)
- [图表样式指南](skills/code-documenter/references/DIAGRAM_STYLES.md)

## 🎓 code-partner 工作流程

```
任务请求 → 技术益害评估 → 风险判断
                                ↓
                    ┌───────────┴───────────┐
                    ↓                       ↓
               直接执行              警告 + 替代方案
                    ↓                       ↓
               优化日志记录 ←────────────────┘
                    ↓
              单元测试 (覆盖率 >70%)
                    ↓
              核心功能验证
                    ↓
                 ✅ 完成
```

## 📋 日志示例

code-partner 生成的日志会记录到 `project_logs/optimization/YYYY-MM-DD.md`：

```markdown
### 【优化日志条目】

**变更类型**：优化
**时间戳**：2026-02-07 14:30:00
**版本号**：v1.2.1
**负责人**：Claude

#### 变更目的
**问题描述**：数据库查询存在N+1问题，导致API响应时间过长
**影响范围**：用户列表页、搜索功能
**根本原因分析**：循环中逐个查询关联数据，未使用JOIN或批量查询

#### 变更内容
- **具体修改**：使用 SQLAlchemy 的 selectinload() 预加载
- **涉及模块**：user_service, database
- **实施方法**：批量预加载关联数据

#### 验证标准
- **成功指标**：API 响应时间 < 150ms
- **测试方案**：单元测试覆盖率 > 70%
- **风险评估**：需监控内存占用
```

## 🛡️ 风险评估指南

code-partner 内置完整的风险评估参考，覆盖：

- 🏗️ 架构风险（单例模式、循环依赖、紧耦合）
- ⚡ 并发风险（竞态条件、死锁、资源泄漏）
- 📊 性能风险（API成本、内存爆炸、延迟增加）
- 🔧 可维护性风险（技术债务、测试盲区）
- 🔒 安全风险（注入攻击、敏感数据）

详见 [docs/risk_assessment.md](docs/risk_assessment.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
