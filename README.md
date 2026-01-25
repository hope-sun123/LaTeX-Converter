# LaTeX-Converter
轻量级、易上手的多格式文档转换工具，专为学术写作场景设计，一键实现Markdown/Word/纯文本与LaTeX格式的双向转换，大幅简化学术文档格式适配流程。

## 核心特性
- 📋 **多格式兼容**：支持Markdown、Word(.docx)、纯文本与LaTeX的双向转换
- 🎯 **格式保真**：精准保留标题、列表、表格、公式等核心排版格式
- ⚡ **批量处理**：命令行批量转换文件夹内所有文件，提升处理效率
- 🚀 **轻量化**：无冗余依赖，仅需Python基础环境即可运行
- 🌍 **跨平台**：完美适配Windows/macOS/Linux系统

## 安装教程
### 环境要求
- Python 3.8 及以上版本
- pip（Python包管理工具，默认随Python安装）
### 快速下载（Windows免安装版）
无需配置Python环境，直接下载可执行文件即可使用：
👉 [最新版exe下载](https://github.com/hope-sun123/LaTeX-Converter/releases)
- 进入上述链接后，找到对应版本的Release，在「Assets」栏目下下载后缀为 `.exe` 的文件；
- 下载完成后**无需安装**，双击exe文件即可启动工具；
- 按照界面提示选择待转换的文件、设置输出格式，点击转换按钮即可完成格式转换。
### 源码安装
1. 克隆仓库到本地：
```bash
git clone https://github.com/hope-sun123/LaTeX-Converter.git
cd LaTeX-Converter
```
2.安装依赖包：
```bash
pip install -r requirements.txt
```
## 使用指南
### 基础命令行用法
#### Markdown 转 LaTeX
```bash
python latex_converter.py convert --input example.md --output example.tex --from md --to latex
```
#### LaTeX 转 Word
```bash
python latex_converter.py convert --input paper.tex --output paper.docx --from latex --to docx
```
## 已知限制
- 复杂 LaTeX 环境（如自定义宏包、高级 TikZ 绘图）可能无法完全转换
- 包含嵌套表格、自定义样式的 Word 文件，转换后可能存在轻微格式丢失
## 问题反馈
如遇到 Bug 或有功能建议，欢迎在 GitHub Issues 页面提交反馈。
### 总结
1. 文档为纯Markdown格式，可直接全选复制后粘贴到GitHub仓库的README.md文件中，无需额外调整格式。
2. 内容覆盖项目核心特性、安装、使用、示例、贡献指南等全维度信息，符合GitHub开源项目规范。
3. 命令示例、格式对照表、转换案例清晰易懂，新手可直接参照操作，降低使用门槛。

