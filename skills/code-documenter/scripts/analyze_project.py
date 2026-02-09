#!/usr/bin/env python3
"""
项目分析脚本 - 扫描项目结构并提取关键信息
"""

import os
import ast
import sys
import io
from pathlib import Path
from typing import Dict, List, Any
import json

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ProjectAnalyzer:
    """项目分析器"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.files_info = []
        self.imports_graph = {}
        self.modules = {}

    def analyze(self) -> Dict[str, Any]:
        """执行完整的项目分析"""
        print(f"🔍 分析项目: {self.project_root}")

        # 扫描所有Python文件
        python_files = self._find_python_files()
        print(f"📁 找到 {len(python_files)} 个Python文件")

        # 分析每个文件
        for file_path in python_files:
            self._analyze_file(file_path)

        # 构建依赖关系图
        self._build_dependency_graph()

        # 识别主要入口点
        entry_points = self._identify_entry_points()

        return {
            "project_root": str(self.project_root),
            "total_files": len(python_files),
            "modules": self.modules,
            "imports_graph": self.imports_graph,
            "entry_points": entry_points,
            "files": self.files_info
        }

    def _find_python_files(self) -> List[Path]:
        """查找所有Python文件"""
        exclude_dirs = {'.git', '__pycache__', 'venv', '.venv', 'node_modules',
                       'dist', 'build', '.tox', '.pytest_cache'}

        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # 过滤掉不需要的目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        return python_files

    def _analyze_file(self, file_path: Path):
        """分析单个Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(file_path))

            relative_path = file_path.relative_to(self.project_root)
            module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')

            # 提取类和函数
            classes = []
            functions = []
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        "docstring": ast.get_docstring(node)
                    })
                elif isinstance(node, ast.FunctionDef):
                    # 只记录顶层函数
                    if hasattr(tree, 'body') and node in tree.body:
                        functions.append({
                            "name": node.name,
                            "docstring": ast.get_docstring(node)
                        })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        imports.append(alias.name)

            self.files_info.append({
                "path": str(relative_path),
                "module": module_name,
                "classes": classes,
                "functions": functions,
                "imports": imports
            })

            self.modules[module_name] = {
                "path": str(relative_path),
                "classes": classes,
                "functions": functions,
                "imports": imports
            }

        except SyntaxError as e:
            print(f"⚠️  语法错误 {file_path}: {e}")
        except Exception as e:
            print(f"⚠️  分析错误 {file_path}: {e}")

    def _build_dependency_graph(self):
        """构建模块依赖关系图"""
        for module_name, module_info in self.modules.items():
            self.imports_graph[module_name] = [
                imp for imp in module_info["imports"]
                if not imp.startswith('.')
            ]

    def _identify_entry_points(self) -> List[str]:
        """识别项目入口点"""
        entry_points = []

        # 查找常见的入口文件
        common_entries = ['__main__.py', 'main.py', 'app.py', 'run.py']
        for entry in common_entries:
            for module in self.modules:
                if module.endswith(entry.replace('.py', '')):
                    entry_points.append(module)

        # 查找 if __name__ == '__main__' 块
        for file_info in self.files_info:
            file_path = self.project_root / file_info["path"]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '__main__' in content:
                        entry_points.append(file_info["module"])
            except:
                pass

        return entry_points


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python analyze_project.py <project-root>")
        sys.exit(1)

    project_root = sys.argv[1]
    analyzer = ProjectAnalyzer(project_root)
    result = analyzer.analyze()

    # 输出结果
    output_file = Path(project_root) / '.claude' / 'project_analysis.json'
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 分析完成！结果保存到: {output_file}")
    print(f"📊 统计:")
    print(f"   - 总文件数: {result['total_files']}")
    print(f"   - 模块数: {len(result['modules'])}")
    print(f"   - 入口点: {', '.join(result['entry_points']) or '未检测到'}")


if __name__ == '__main__':
    main()
