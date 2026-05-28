# LaTeX-Converter

LaTeX-Converter 是一个面向学习和轻量写作场景的 Python 工具，目前主要支持将纯文本、Markdown 风格文本转换为 LaTeX，并提供一个可视化 LaTeX 表格代码生成器。

> 当前版本仍处于早期阶段。README 会尽量只描述已经实现的能力，避免把未来计划写成现有功能。

## 功能

- 文本 / Markdown 风格内容转 LaTeX
  - 支持标题、无序列表、有序列表、加粗、斜体、代码块和常见 LaTeX 特殊字符转义
  - 可生成完整 `.tex` 文档，也可只生成可插入现有文档的片段
- LaTeX 表格可视化设计器
  - 支持设置行列数、对齐方式、边框
  - 支持编辑单元格并生成 `tabular` 代码
- 附带实用工具
  - 文件重命名、简单文件格式转换、文件搜索
  - CSV / Excel 数据绘图与统计分析
  - URL 检测、IP 查询、端口扫描

## 安装

### 环境要求

- Python 3.8+
- pip

### 从源码运行

```bash
git clone https://github.com/hope-sun123/LaTeX-Converter.git
cd LaTeX-Converter
python -m pip install -r requirements.txt
```

也可以用可编辑模式安装命令行入口：

```bash
python -m pip install -e .
```

安装后可以使用：

```bash
latex-converter --help
```

## 使用方法

### 启动图形界面

不带参数运行会启动文本转 LaTeX GUI：

```bash
python cli.py
```

### 命令行转换文本为 LaTeX

生成完整 LaTeX 文档：

```bash
python cli.py latex-convert --input example.md --output example.tex
```

只生成片段：

```bash
python cli.py latex-convert --input example.md --output fragment.tex --no-env
```

从标准输入读取：

```bash
echo "# 标题" | python cli.py latex-convert --no-env
```

### 启动表格设计器

```bash
python cli.py latex-table
```

### 查看全部子命令

```bash
python cli.py --help
```

## 已知限制

- 当前还不支持 Word `.docx` 与 LaTeX 的双向转换。
- 当前还不支持完整 Markdown 语法，例如复杂表格、脚注、任务列表、嵌套列表等。
- 当前 LaTeX 转换器适合轻量文本，不适合处理复杂宏包、自定义命令或 TikZ 等高级 LaTeX 内容。
- 数据可视化和网络工具依赖第三方库，使用前请先安装 `requirements.txt`。

## 开发与测试

运行单元测试：

```bash
python -m unittest discover -s tests
```

检查命令行入口：

```bash
python cli.py --help
```

## 后续计划

- 使用 Markdown AST 解析器替代大部分正则转换逻辑
- 增加 Markdown 表格到 LaTeX `tabular` 的转换
- 增加更多测试样例，覆盖中文、公式、代码块和列表嵌套
- 整理包名，将 `ultility_toolkit` 逐步迁移为更清晰的模块命名
- 如果要支持 Word 转换，再单独引入 `python-docx` / Pandoc 等方案

## 反馈

如果遇到问题或有功能建议，欢迎在 GitHub Issues 中提交反馈。
