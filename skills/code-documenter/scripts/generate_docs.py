#!/usr/bin/env python3
"""
文档生成脚本 - 基于项目分析结果生成学习文档
"""

import os
import sys
import io
import json
from pathlib import Path
from typing import Dict, List, Any

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class DocumentationGenerator:
    """文档生成器"""

    def __init__(self, project_root: str, analysis_file: str = None):
        self.project_root = Path(project_root)
        if analysis_file:
            self.analysis = self._load_analysis(analysis_file)
        else:
            self.analysis = self._load_analysis(
                self.project_root / '.claude' / 'project_analysis.json'
            )

    def _load_analysis(self, analysis_file: Path) -> Dict[str, Any]:
        """加载项目分析结果"""
        with open(analysis_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate(self, output_file: str = None) -> str:
        """生成完整的学习文档"""
        if output_file is None:
            output_file = self.project_root / 'docs' / 'PROJECT_LEARNING_GUIDE.md'

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = []
        lines.append(f"# {self.project_root.name} - 项目学习指南\n")

        # 第一部分：项目概览
        lines.extend(self._generate_overview())

        # 第二部分：整体架构
        lines.extend(self._generate_architecture())

        # 第三部分：主要工作流程
        lines.extend(self._generate_main_workflow())

        # 第四部分：模块详解
        lines.extend(self._generate_module_details())

        # 第五部分：依赖关系
        lines.extend(self._generate_dependencies())

        content = '\n'.join(lines)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _generate_overview(self) -> List[str]:
        """生成项目概览部分"""
        lines = [
            "## 第一部分：项目概览\n",
            "### 1.1 项目简介",
            f"- **项目名称**: {self.project_root.name}",
            f"- **总文件数**: {self.analysis['total_files']} 个Python文件",
            f"- **模块数**: {len(self.analysis['modules'])} 个模块",
            "",
            "### 1.2 项目结构",
            "```",
            self._generate_tree_structure(),
            "```",
            ""
        ]
        return lines

    def _generate_tree_structure(self) -> str:
        """生成项目目录树结构"""
        # 简化的目录树
        lines = [f"{self.project_root.name}/"]

        # 按目录分组
        dirs = {}
        for file_info in self.analysis['files']:
            path_parts = Path(file_info['path']).parts
            if len(path_parts) > 1:
                dir_name = path_parts[0]
                if dir_name not in dirs:
                    dirs[dir_name] = []
                dirs[dir_name].append(path_parts[-1])
            else:
                dirs[''] = dirs.get('', []) + [path_parts[0]]

        # 输出树结构
        for dir_name, files in sorted(dirs.items()):
            if dir_name:
                lines.append(f"├── {dir_name}/")
                for file in sorted(files)[:5]:  # 限制显示数量
                    lines.append(f"│   ├── {file}")
                if len(files) > 5:
                    lines.append(f"│   └── ... ({len(files) - 5} more files)")
            else:
                for file in sorted(files):
                    lines.append(f"├── {file}")

        return '\n'.join(lines)

    def _generate_architecture(self) -> List[str]:
        """生成整体架构部分"""
        lines = [
            "### 1.3 整体架构",
            "",
            "```mermaid",
            "graph TD",
            "    A[项目入口]",
        ]

        # 添加主要模块
        modules = list(self.analysis['modules'].keys())[:10]
        for i, module in enumerate(modules):
            clean_name = module.split('.')[-1]
            lines.append(f"    A --> M{i+1}[{clean_name}]")

        lines.extend([
            "```",
            "",
            "**架构说明**：",
            "- 上图展示了项目的主要模块组织结构",
            "- 模块之间的调用关系见下文依赖分析",
            ""
        ])
        return lines

    def _generate_main_workflow(self) -> List[str]:
        """生成主要工作流程部分"""
        lines = [
            "### 1.4 主要工作流程",
            "",
            "**待补充**: 需要根据实际代码逻辑补充主流程图",
            "",
            "```mermaid",
            "flowchart TD",
            "    Start([开始]) --> Step1[步骤1]",
            "    Step1 --> Step2[步骤2]",
            "    Step2 --> End([结束])",
            "```",
            "",
            "**流程说明**：",
            "- 此流程图需要人工根据实际代码逻辑补充完整",
            "- 建议从入口点开始追踪代码执行路径",
            ""
        ]
        return lines

    def _generate_module_details(self) -> List[str]:
        """生成模块详解部分"""
        lines = [
            "## 第二部分：模块详解\n"
        ]

        for module_name, module_info in sorted(self.analysis['modules'].items()):
            lines.extend(self._generate_single_module(module_name, module_info))

        return lines

    def _generate_single_module(self, module_name: str, module_info: Dict) -> List[str]:
        """生成单个模块的详细说明"""
        clean_name = module_name.split('.')[-1]
        lines = [
            f"### 模块: {clean_name}",
            f"**模块路径**: `{module_info['path']}`",
            ""
        ]

        # 背景与目标
        lines.extend([
            "#### 背景与目标",
            "**待补充**:",
            "- 为什么需要这个模块？",
            "- 解决了什么问题？",
            ""
        ])

        # 类说明
        if module_info['classes']:
            lines.extend([
                "#### 类定义",
                ""
            ])
            for cls in module_info['classes']:
                lines.append(f"**类名**: `{cls['name']}`")
                if cls['docstring']:
                    lines.append(f"> {cls['docstring']}")
                if cls['methods']:
                    lines.append(f"**方法**: {', '.join(f'`{m}`' for m in cls['methods'])}")
                lines.append("")

        # 函数说明
        if module_info['functions']:
            lines.extend([
                "#### 函数定义",
                ""
            ])
            for func in module_info['functions']:
                lines.append(f"**函数名**: `{func['name']}`")
                if func['docstring']:
                    lines.append(f"> {func['docstring']}")
                lines.append("")

        # 设计决策
        lines.extend([
            "#### 设计决策",
            "**待补充**:",
            "- 为什么选择这种实现方式？",
            "- 考虑过的替代方案？",
            "- 技术难点和解决方案",
            ""
        ])

        return lines

    def _generate_dependencies(self) -> List[str]:
        """生成依赖关系部分"""
        lines = [
            "## 第三部分：依赖关系\n",
            "### 3.1 模块依赖图",
            "",
            "```mermaid",
            "graph LR",
        ]

        # 显示部分依赖关系
        count = 0
        for module, imports in self.analysis['imports_graph'].items():
            if count >= 20:  # 限制数量
                break
            module_short = module.split('.')[-1]
            for imp in imports[:3]:  # 每个模块最多显示3个导入
                imp_short = imp.split('.')[-1]
                lines.append(f"    {module_short}[{module_short}] --> {imp_short}[{imp_short}]")
                count += 1

        lines.extend([
            "```",
            ""
        ])

        return lines


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python generate_docs.py <project-root> [--output output-file.md]")
        sys.exit(1)

    project_root = sys.argv[1]
    output_file = None

    if len(sys.argv) >= 4 and sys.argv[2] == '--output':
        output_file = sys.argv[3]

    generator = DocumentationGenerator(project_root)
    output_path = generator.generate(output_file)

    print(f"✅ 学习文档已生成: {output_path}")
    print(f"⚠️  请注意: 自动生成的文档需要人工审核和补充！")
    print(f"📋 特别需要补充:")
    print(f"   - 设计决策和背景信息")
    print(f"   - 实际使用示例")
    print(f"   - 流程图和架构图的准确性")


if __name__ == '__main__':
    main()
