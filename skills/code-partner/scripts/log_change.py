#!/usr/bin/env python3
"""
优化日志自动记录脚本
自动创建/更新当日的优化日志文件
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 项目配置
LOG_DIR = Path("project_logs/optimization")
VERSION_FILE = LOG_DIR / ".version"


def get_next_version():
    """获取下一个版本号"""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, "r") as f:
            major, minor, patch = map(int, f.read().strip().split("."))
        return f"{major}.{minor}.{patch + 1}"
    return "1.0.1"


def update_version(version):
    """更新版本号文件"""
    VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def get_log_path():
    """获取今日日志文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{today}.md"


def create_log_entry(**kwargs):
    """创建日志条目"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version = get_next_version()

    entry = f"""### 【优化日志条目】

**变更类型**：{kwargs.get('change_type', '优化')}

**时间戳**：{timestamp}

**版本号**：v{version}

**负责人**：{kwargs.get('owner', 'Claude')}

---

#### 变更目的

{kwargs.get('purpose', '')}

---

#### 变更内容

- **具体修改**：
{kwargs.get('changes', '  - 待补充')}
- **涉及模块**：{kwargs.get('modules', '待补充')}
- **实施方法**：{kwargs.get('method', '待补充')}

---

#### 验证标准

- **成功指标**：
{kwargs.get('success_metrics', '  - 待补充')}
- **测试方案**：
  - 单元测试：覆盖率 > 70%
{kwargs.get('test_plan', '  - 其他测试：待补充')}
- **风险评估**：{kwargs.get('risk_assessment', '待补充')}

---

#### 后续建议

- **相关影响**：{kwargs.get('impact', '待评估')}
- **待办事项**：
{kwargs.get('todos', '  - 待补充')}

---
"""
    return entry, version


def append_to_log(entry):
    """追加到日志文件"""
    log_path = get_log_path()

    # 如果文件不存在，创建并写入头部
    if not log_path.exists():
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# 优化日志 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        print(f"✅ 创建新日志文件: {log_path}")

    # 追加条目
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

    return log_path


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="记录优化变更日志")
    parser.add_argument("--type", dest="change_type", default="优化",
                        choices=["需求", "优化", "Bug修复"],
                        help="变更类型")
    parser.add_argument("--purpose", required=True, help="变更目的")
    parser.add_argument("--modules", default="待补充", help="涉及模块")
    parser.add_argument("--changes", default="待补充", help="具体修改")
    parser.add_argument("--method", default="待补充", help="实施方法")
    parser.add_argument("--metrics", dest="success_metrics", default="待补充",
                        help="成功指标")
    parser.add_argument("--test", dest="test_plan", default="待补充",
                        help="测试方案")
    parser.add_argument("--risk", dest="risk_assessment", default="低风险",
                        help="风险评估")
    parser.add_argument("--impact", default="待评估", help="相关影响")
    parser.add_argument("--todos", default="待补充", help="待办事项")
    parser.add_argument("--owner", default="Claude", help="负责人")

    args = parser.parse_args()

    # 创建日志条目
    entry, version = create_log_entry(
        change_type=args.change_type,
        purpose=args.purpose,
        modules=args.modules,
        changes=args.changes,
        method=args.method,
        success_metrics=args.success_metrics,
        test_plan=args.test_plan,
        risk_assessment=args.risk_assessment,
        impact=args.impact,
        todos=args.todos,
        owner=args.owner
    )

    # 写入日志
    log_path = append_to_log(entry)

    # 更新版本号
    update_version(version)

    print(f"\n✅ 变更已记录至优化日志 v{version}")
    print(f"📄 日志文件: {log_path}")
    print(f"\n--- 日志内容预览 ---")
    print(entry[:500] + "...")


if __name__ == "__main__":
    main()
