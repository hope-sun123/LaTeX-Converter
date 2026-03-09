import argparse
import sys
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
# 注意：如果包名拼写错误（ultility_toolkit → utility_toolkit），需同步修改
from ultility_toolkit.file_tools import FileRenamer, FileConverter, FileSearcher
from ultility_toolkit.data_viz import DataPlotter, DataAnalyzer
from ultility_toolkit.network_tools import IPQuery, PortScanner, URLChecker
from ultility_toolkit.latex_converter import Text2LaTeXConverter
from ultility_toolkit.bib_manager import get_bibtex_from_doi, append_to_bib_file

def run_latex_gui():
    """LaTeX转换的GUI入口（左右分栏版）"""
    # 主窗口配置
    root = tk.Tk()
    root.title("文本转LaTeX工具 v0.1.0")
    root.geometry("1000x600")  # 加宽窗口，适配左右分栏
    root.resizable(True, True)

    # ========== 左右分栏布局 ==========
    # 左侧：原始文本输入框
    left_frame = tk.Frame(root, padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tk.Label(left_frame, text="📝 原始文本", font=("微软雅黑", 12)).pack(anchor=tk.NW)
    
    # 带滚动条的文本输入框
    input_text = scrolledtext.ScrolledText(left_frame, width=50, height=25, font=("Consolas", 10))
    input_text.pack(fill=tk.BOTH, expand=True, pady=5)

    # 右侧：转换结果显示框
    right_frame = tk.Frame(root, padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    tk.Label(right_frame, text="✨ 转换结果", font=("微软雅黑", 12)).pack(anchor=tk.NW)
    
    # 带滚动条的结果显示框（只读）
    output_text = scrolledtext.ScrolledText(right_frame, width=50, height=25, font=("Consolas", 10), state=tk.DISABLED)
    output_text.pack(fill=tk.BOTH, expand=True, pady=5)

    # ========== 转换功能函数 ==========
    def convert_full():
        """转换为完整LaTeX文档"""
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "请输入待转换文本！")
            return
        try:
            converter = Text2LaTeXConverter()
            latex_content = converter.convert(text, add_document_env=True)
            # 更新结果框
            output_text.config(state=tk.NORMAL)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", latex_content)
            output_text.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "已转换为完整LaTeX文档！")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")

    def convert_fragment():
        """转换为仅文段片段（无环境）"""
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "请输入待转换文本！")
            return
        try:
            converter = Text2LaTeXConverter()
            latex_content = converter.convert(text, add_document_env=False)
            # 更新结果框
            output_text.config(state=tk.NORMAL)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", latex_content)
            output_text.config(state=tk.DISABLED)
            messagebox.showinfo("成功", "已转换为仅LaTeX文段片段！")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")

    def clear_text():
        """清空输入和结果"""
        input_text.delete("1.0", tk.END)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.config(state=tk.DISABLED)

    # ========== 按钮区域 ==========
    btn_frame = tk.Frame(root, pady=10)
    btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    # 转换按钮
    tk.Button(
        btn_frame, text="📄 转换为完整LaTeX文档", 
        command=convert_full, width=20, height=2, font=("微软雅黑", 10)
    ).pack(side=tk.LEFT, padx=20)
    
    tk.Button(
        btn_frame, text="📝 转换为仅文段片段", 
        command=convert_fragment, width=20, height=2, font=("微软雅黑", 10)
    ).pack(side=tk.LEFT, padx=20)
    
    # 清空按钮
    tk.Button(
        btn_frame, text="🗑️ 清空内容", 
        command=clear_text, width=15, height=2, font=("微软雅黑", 10)
    ).pack(side=tk.LEFT, padx=20)

    # 启动主循环
    root.mainloop()

def choose_latex_mode() -> bool:
    print("\n请选择LaTeX生成模式：")
    print("1 - 完整LaTeX文档（含\\documentclass{}、\\begin{document}等，可直接编译）")
    print("2 - 仅文段片段（无环境，仅转义格式化，便于临时插入）")
    while True:
        user_choice = input("请输入选择（1/2，默认1）：").strip()
        if not user_choice:
            return True
        elif user_choice in ["1", "完整", "文档", "compile"]:
            return True
        elif user_choice in ["2", "片段", "文段", "插入"]:
            return False
        else:
            print(f"输入无效：{user_choice}，请输入1或2！")

def main():
    # 无命令行参数时启动GUI
    if len(sys.argv) == 1:
        run_latex_gui()
        return
    
    parser = argparse.ArgumentParser(
        prog="ultility-toolkit",
        description="多功能Python实用工具集 v0.1.0 | 支持文件处理/数据可视化/网络工具/文本转LaTeX",
        epilog="项目地址：https://github.com/your-username/python-ultility-toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", help="请选择功能模块")

    # 1. 文件重命名
    rename_parser = subparsers.add_parser("rename", help="文件批量重命名")
    rename_parser.add_argument("--dir", required=True, help="目标目录")
    rename_parser.add_argument("--prefix", help="前缀重命名（如--prefix file_）")
    rename_parser.add_argument("--replace-old", help="替换旧字符串")
    rename_parser.add_argument("--replace-new", help="替换新字符串")
    rename_parser.add_argument("--regex", help="正则匹配模式")
    rename_parser.add_argument("--regex-repl", help="正则替换值")
    rename_parser.add_argument("--ext", help="扩展名过滤（如.txt）")

    # 2. 文件格式转换
    file_conv_parser = subparsers.add_parser("file-conv", help="文件格式转换")
    file_conv_parser.add_argument("--file", help="单个目标文件")
    file_conv_parser.add_argument("--dir", help="目标目录")
    file_conv_parser.add_argument("--type", required=True, choices=["txt2csv", "csv2txt", "change-ext"], help="转换类型")
    file_conv_parser.add_argument("--old-ext", help="原扩展名（change-ext时用）")
    file_conv_parser.add_argument("--new-ext", help="新扩展名（change-ext时用）")
    file_conv_parser.add_argument("--delimiter", default=",", help="分隔符（默认,）")

    # 3. 文件检索
    file_search_parser = subparsers.add_parser("file-search", help="文件内容/名称检索")
    file_search_parser.add_argument("--dir", required=True, help="目标目录")
    file_search_parser.add_argument("--keyword", help="检索关键词（name/content时用）")
    file_search_parser.add_argument("--type", required=True, choices=["name", "content", "size"], help="检索类型")
    file_search_parser.add_argument("--ext", help="扩展名过滤")
    file_search_parser.add_argument("--min-size", type=int, help="最小文件大小(字节)")
    file_search_parser.add_argument("--max-size", type=int, help="最大文件大小(字节)")

    # 4. 数据可视化
    plot_parser = subparsers.add_parser("plot", help="数据可视化绘图")
    plot_parser.add_argument("--file", required=True, help="CSV/Excel数据文件")
    plot_parser.add_argument("--type", required=True, choices=["bar", "line", "pie", "scatter", "hist"], help="图表类型")
    plot_parser.add_argument("--output", default="chart.png", help="输出图片路径")
    plot_parser.add_argument("--title", help="图表标题")
    plot_parser.add_argument("--x-col", help="X轴列名")
    plot_parser.add_argument("--y-col", help="Y轴列名")

    # 5. 数据统计分析
    data_analyze_parser = subparsers.add_parser("data-analyze", help="数据统计分析")
    data_analyze_parser.add_argument("--file", required=True, help="CSV/Excel数据文件")
    data_analyze_parser.add_argument("--type", required=True, choices=["basic", "corr", "missing", "outlier"], help="分析类型")
    data_analyze_parser.add_argument("--col", help="分析列名（outlier时必填）")

    # 6. IP查询
    ip_query_parser = subparsers.add_parser("ip-query", help="IP地址/域名解析")
    ip_query_parser.add_argument("--ip", help="查询IP（默认本机）")
    ip_query_parser.add_argument("--domain", help="解析域名到IP")

    # 7. 端口扫描
    port_scan_parser = subparsers.add_parser("port-scan", help="端口扫描")
    port_scan_parser.add_argument("--host", required=True, help="目标主机/IP")
    port_scan_parser.add_argument("--start", type=int, default=1, help="起始端口")
    port_scan_parser.add_argument("--end", type=int, default=1024, help="结束端口")
    port_scan_parser.add_argument("--common", action="store_true", help="扫描常见端口并显示服务")

    # 8. URL检测
    url_check_parser = subparsers.add_parser("url-check", help="URL有效性检测")
    url_check_parser.add_argument("--url", help="单个检测URL")
    url_check_parser.add_argument("--file", help="批量检测URL文件（每行一个URL）")

    # 9. LaTeX转换
    latex_parser = subparsers.add_parser("latex-convert", help="文本转LaTeX格式")
    latex_parser.add_argument("--input", help="输入文本文件")
    latex_parser.add_argument("--output", help="输出LaTeX文件")
    latex_parser.add_argument("--no-env", action="store_false", dest="add_env", default=True, 
                             help="直接生成无环境的文段片段")

    # 10. 文献BibTeX自动化 (请确认这段话在 args = parser.parse_args() 这一行之前)
    bib_parser = subparsers.add_parser("bib", help="文献BibTeX自动化管理")
    bib_parser.add_argument("--doi", required=True, help="输入文献的DOI号")
    bib_parser.add_argument("--save", action="store_true", help="是否自动保存")

    args = parser.parse_args()

    # 无参数时提示选择功能
    if not args.command:
        print("❌ 错误：请指定要运行的功能模块！")
        parser.print_help()
        sys.exit(1)

    # ========== 各功能逻辑（无修改） ==========
    if args.command == "rename":
        try:
            renamer = FileRenamer(args.dir)
            if args.prefix:
                res = renamer.rename_by_prefix(args.prefix, ext_filter=args.ext)
            elif args.replace_old and args.replace_new:
                res = renamer.rename_by_replace(args.replace_old, args.replace_new, ext_filter=args.ext)
            elif args.regex and args.regex_repl:
                res = renamer.rename_by_regex(args.regex, args.regex_repl)
            else:
                print("错误：请指定重命名模式（--prefix/--replace-old/--regex）")
                sys.exit(1)
            for line in res:
                print(line)
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "file-conv":
        try:
            if not args.file and not args.dir:
                print("错误：请指定--file（单个文件）或--dir（目录）")
                sys.exit(1)
            conv = FileConverter(dir_path=args.dir, file_path=args.file)
            if args.type == "txt2csv":
                res = conv.txt2csv(args.delimiter)
            elif args.type == "csv2txt":
                res = conv.csv2txt(args.delimiter)
            elif args.type == "change-ext":
                if not args.old_ext or not args.new_ext:
                    print("错误：change-ext需指定--old-ext和--new-ext")
                    sys.exit(1)
                res = conv.batch_change_ext(args.old_ext, args.new_ext)
            for line in res:
                print(line)
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "file-search":
        try:
            searcher = FileSearcher(args.dir)
            if args.type == "name":
                if not args.keyword:
                    print("错误：name检索需指定--keyword")
                    sys.exit(1)
                res = searcher.search_by_name(args.keyword, ext_filter=args.ext)
            elif args.type == "content":
                if not args.keyword:
                    print("错误：content检索需指定--keyword")
                    sys.exit(1)
                res = searcher.search_by_content(args.keyword, ext_filter=args.ext)
            elif args.type == "size":
                res = searcher.search_by_size(args.min_size, args.max_size)
            if res:
                for item in res:
                    print(item)
            else:
                print("未找到匹配结果")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "plot":
        try:
            plotter = DataPlotter(args.file)
            title = args.title or f"{args.type}图"
            if args.type == "bar":
                plotter.plot_bar(args.output, args.x_col, args.y_col, title)
            elif args.type == "line":
                plotter.plot_line(args.output, args.x_col, args.y_col, title)
            elif args.type == "pie":
                plotter.plot_pie(args.output, args.x_col, args.y_col, title)
            elif args.type == "scatter":
                plotter.plot_scatter(args.output, args.x_col, args.y_col, title=title)
            elif args.type == "hist":
                plotter.plot_hist(args.output, args.x_col, title=title)
            print(f"图表已保存至：{os.path.abspath(args.output)}")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "data-analyze":
        try:
            analyzer = DataAnalyzer(args.file)
            if args.type == "basic":
                res = analyzer.basic_stats()
            elif args.type == "corr":
                res = analyzer.correlation_analysis()
            elif args.type == "missing":
                res = analyzer.missing_value_analysis()
            elif args.type == "outlier":
                if not args.col:
                    print("错误：outlier分析需指定--col列名")
                    sys.exit(1)
                res = analyzer.outlier_detection(args.col)
            print(res)
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "ip-query":
        try:
            ipq = IPQuery()
            if args.domain:
                res = ipq.domain2ip(args.domain)
                print(f"域名{args.domain}解析结果：{res}")
            else:
                res = ipq.query(args.ip)
                for k, v in res.items():
                    print(f"{k}：{v}")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "port-scan":
        try:
            scanner = PortScanner(args.host)
            if args.common:
                res = scanner.scan_common_ports()
                print(f"主机{args.host}开放的常见端口：")
                for port, service in res:
                    print(f"端口{port}：{service}")
            else:
                res = scanner.scan(args.start, args.end)
                print(f"主机{args.host}端口{args.start}-{args.end}开放的端口：{res}")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "url-check":
        try:
            checker = URLChecker()
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    urls = [l.strip() for l in f if l.strip()]
                res = checker.check_batch(urls)
                for item in res:
                    print(item)
            else:
                if not args.url:
                    print("错误：请指定--url（单个URL）或--file（批量URL文件）")
                    sys.exit(1)
                res = checker.check_single(args.url)
                for k, v in res.items():
                    print(f"{k}：{v}")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)

    elif args.command == "latex-convert":
        try:
            converter = Text2LaTeXConverter()
            add_document_env = args.add_env
            
            # 修复：交互选择逻辑（args.add_env默认是True，仅未传--no-env时弹出选择）
            if args.add_env is None:
                add_document_env = choose_latex_mode()
            else:
                tip = "完整LaTeX文档（含\\documentclass{}环境）" if add_document_env else "仅LaTeX文段片段（无环境）"
                print(f"✅ 已指定：生成{tip}")

            if args.input:
                print(f"\n📂 读取文件：{os.path.abspath(args.input)}")
                latex_content = converter.from_file(args.input, args.output, add_document_env)
            else:
                # 仅当未传--no-env时才弹出模式选择
                if args.add_env:
                    add_document_env = choose_latex_mode()
                print("\n✏️  请输入待转换文本（Ctrl+D/Linux/Ctrl+Z/Windows结束）：")
                text = sys.stdin.read()
                latex_content = converter.convert(text, add_document_env)
                if args.output:
                    converter.save_to_file(latex_content, args.output)

            if not args.output:
                print("\n🎉 转换完成！LaTeX内容：")
                print("="*80)
                print(latex_content)
                print("="*80)
                if add_document_env:
                    print("💡 提示：可直接保存为.tex文件编译")
                else:
                    print("💡 提示：可直接复制插入已有LaTeX文档")
        except Exception as e:
            print(f"失败：{str(e)}")
            sys.exit(1)
    
    elif args.command == "bib":
        try:
            print(f"🔍 正在检索 DOI: {args.doi} ...")
            bib_content = get_bibtex_from_doi(args.doi)
            
            print("\n" + "="*50)
            print("✨ 获取到的 BibTeX 条目：")
            print("-" * 50)
            print(bib_content)
            print("="*50)

            # 如果用户带了 --save 参数，或者手动确认保存
            if args.save:
                msg = append_to_bib_file(bib_content)
                print(f"\n💾 {msg}")
            else:
                choice = input("\n❓ 是否将此条目保存到 references.bib? (y/n): ").strip().lower()
                if choice == 'y':
                    msg = append_to_bib_file(bib_content)
                    print(f"💾 {msg}")
        except Exception as e:
            print(f"❌ 失败：{str(e)}")
            sys.exit(1)
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
