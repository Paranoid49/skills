# 使用示例

## 示例 1：数据库查询优化

### 需求
用户列表页加载缓慢，存在 N+1 查询问题。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ API 响应时间从 800ms 降至 150ms<br>✅ 数据库负载降低 80%<br>✅ 用户体验显著提升 |
| **风险** | 🟡 中风险 - 预加载可能增加内存占用<br>🟡 需要修改现有查询逻辑 |

### 决策
✅ **执行优化**，同时监控内存使用

### 实施变更

```bash
python skills/code-partner/scripts/log_change.py \
  --type "优化" \
  --purpose "解决用户列表 N+1 查询问题" \
  --modules "user_service, database" \
  --changes "使用 selectinload() 预加载用户关联数据" \
  --method "SQLAlchemy ORM 批量预加载" \
  --metrics "- API响应时间 < 150ms
- 查询次数从 N+1 降至 2 次" \
  --test "单元测试: tests/test_user_service.py
性能基准测试: 1000 用户数据集" \
  --risk "中风险 - 内存占用可能增加 20%，已添加监控" \
  --impact "其他列表查询可参考此方案" \
  --todos "- 审查所有循环查询代码
- 添加查询性能监控告警"
```

### 结果
```
✅ 变更已记录至优化日志 v1.2.3
📄 日志文件: project_logs/optimization/2026-02-07.md
```

---

## 示例 2：引入缓存系统

### 需求
频繁查询的配置数据导致数据库压力大。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ 数据库负载降低 90%<br>✅ 响应时间降至 10ms |
| **风险** | 🔴 高风险 - 引入新组件 Redis<br>🔴 增加系统复杂度<br>🔴 可能出现缓存一致性问题<br>🔴 需要额外运维成本 |

### 决策
⚠️ **警告** - 建议先考虑更轻量的方案

### 替代方案

1. **方案 A（推荐）**：使用 Python 内存缓存（`functools.lru_cache`）
   - 优点：零依赖，简单高效
   - 缺点：单机缓存，重启丢失

2. **方案 B**：引入 Redis
   - 优点：分布式缓存，持久化
   - 缺点：增加依赖和复杂度

### 用户选择方案 A

```bash
python skills/code-partner/scripts/log_change.py \
  --type "优化" \
  --purpose "为配置数据添加内存缓存" \
  --modules "config_service" \
  --changes "使用 lru_cache 缓存配置查询结果" \
  --method "Python functools.lru_cache" \
  --metrics "- 缓存命中率 > 90%
- 响应时间 < 10ms" \
  --test "单元测试验证缓存功能" \
  --risk "低风险 - 单机缓存，重启丢失" \
  --impact "无需额外运维成本" \
  --todos "- 监控缓存命中率
- 评估后续是否需要分布式缓存"
```

---

## 示例 3：架构重构

### 需求
当前代码存在循环依赖问题。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ 解决循环依赖<br>✅ 提高代码可维护性<br>✅ 便于单元测试 |
| **风险** | 🟡 中风险 - 影响多个模块<br>🟡 需要全面回归测试<br>🟡 可能引入新的 Bug |

### 决策
✅ **执行重构**，需要充分测试

### 实施变更

```bash
python skills/code-partner/scripts/log_change.py \
  --type "优化" \
  --purpose "解耦 service 层和 repository 层的循环依赖" \
  --modules "user_service, order_service, repository" \
  --changes "引入依赖注入容器，通过接口抽象解耦" \
  --method "使用 dependency-injector 库" \
  --metrics "- 消除所有循环引用
- 所有模块可独立测试" \
  --test "全量回归测试 + 循环依赖检测工具" \
  --risk "中风险 - 需要全面测试，可能影响现有功能" \
  --impact "需同步更新相关模块的依赖注入配置" \
  --todos "- 更新架构文档
- 团队培训依赖注入模式
- 监控生产环境异常"
```

---

## 示例 4：新功能开发

### 需求
添加用户头像上传功能。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ 提升用户体验<br>✅ 增强产品功能 |
| **风险** | 🟡 中风险 - 需要文件存储服务<br>🟡 需要处理文件安全（大小、类型）<br>🟡 需要图片处理（压缩、裁剪） |

### 决策
✅ **执行开发**，注意安全处理

### 实施变更

```bash
python skills/code-partner/scripts/log_change.py \
  --type "需求" \
  --purpose "实现用户头像上传功能" \
  --modules "user_api, storage_service" \
  --changes "- 添加文件上传 API 接口
- 集成 OSS 存储
- 实现图片压缩和裁剪" \
  --method "Flask file upload + Pillow + 阿里云 OSS" \
  --metrics "- 支持 jpg/png 格式
- 文件大小限制 2MB
- 自动压缩至 200KB 以下" \
  --test "单元测试 + 文件安全测试" \
  --risk "中风险 - 需严格校验文件类型和大小" \
  --impact "需要配置 OSS 访问权限" \
  --todos "- 添加图片鉴黄服务
- 实现图片 CDN 加速
- 更新用户文档"
```

---

## 示例 5：Bug 修复

### 需求
在高并发场景下，订单库存出现超卖。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ 修复严重 Bug<br>✅ 避免业务损失 |
| **风险** | 🔴 高风险 - 并发逻辑复杂<br>🔴 修改可能影响性能<br>🔴 需要充分测试 |

### 决策
✅ **立即修复**，但需要充分测试

### 实施变更

```bash
python skills/code-partner/scripts/log_change.py \
  --type "Bug修复" \
  --purpose "修复高并发下库存超卖问题" \
  --modules "order_service, inventory" \
  --changes "使用数据库乐观锁 + Redis 原子操作" \
  --method "SELECT FOR UPDATE + Redis INCR" \
  --metrics "- 无超卖现象
- 压测 1000 TPS 无错误" \
  --test "并发压力测试 + 边界条件测试" \
  --risk "高风险 - 并发逻辑需要严格测试
- 可能增加响应时间 50ms" \
  --impact "需要监控库存接口性能" \
  --todos "- 添加库存告警机制
- 补偿异常订单数据"
```

---

## 示例 6：引入第三方依赖

### 需求
使用 Elasticsearch 替换数据库全文搜索。

### 技术益害评估

| 维度 | 分析 |
|------|------|
| **益处** | ✅ 搜索性能提升 10 倍<br>✅ 支持更丰富的查询语法 |
| **风险** | 🔴 高风险 - 引入新组件 ES<br>🔴 增加部署复杂度<br>🔴 需要数据同步机制<br>🔴 运维成本增加 |

### 决策
⚠️ **强烈警告** - 建议先评估现有数据库搜索是否够用

### 替代方案

1. **方案 A**：优化数据库搜索（添加全文索引）
   - 成本低，无需新组件
   - 性能提升有限

2. **方案 B**：引入 Elasticsearch
   - 性能大幅提升
   - 但显著增加复杂度

### 用户仍选择方案 B

```bash
python skills/code-partner/scripts/log_change.py \
  --type "需求" \
  --purpose "引入 Elasticsearch 实现全文搜索" \
  --modules "search_service, sync_worker" \
  --changes "- 集成 Elasticsearch 客户端
- 实现 DB 到 ES 的数据同步
- 添加搜索 API" \
  --method "Elasticsearch-py + Logstash" \
  --metrics "- 搜索响应时间 < 100ms
- 支持中文分词" \
  --test "功能测试 + 搜索性能测试" \
  --risk "高风险 - 需要维护 ES 集群
- 数据同步可能延迟" \
  --impact "需要运维团队支持" \
  --todos "- 配置 ES 集群监控
- 制定数据一致性检查方案
- 团队培训 ES 使用"
```
