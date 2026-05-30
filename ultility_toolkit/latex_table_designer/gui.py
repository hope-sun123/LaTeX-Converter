
"""LaTeX表格设计器可视化界面（基于tkinter，Python内置，无需额外依赖）"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox, simpledialog
import pyperclip  
from .core import LaTeXTableGenerator
from .utils import validate_table_params, clean_cell_content

class LaTeXTableDesignerGUI:
    def __init__(self):
        self.generator = LaTeXTableGenerator()
        self.root = tk.Tk()
        self.root.title("LaTeX 表格可视化设计器")
        self.root.geometry("900x600")
      
        self._setup_chinese_font()
     
        self._build_ui()

    def _setup_chinese_font(self):
        """设置中文显示字体（兼容所有Python版本）"""
        try:
          
            default_font = tkfont.nametofont("TkDefaultFont")
            
            font_family = "SimHei" if tk.TkVersion < 8.6 else ("Microsoft YaHei", "SimHei")[0]
            default_font.configure(family=font_family, size=10)
            self.root.option_add("*Font", default_font)
        except Exception as e:
            
            print(f"⚠️  中文显示字体设置失败（不影响功能）：{str(e)}")
            pass

    def _build_ui(self):
        """构建可视化界面"""
       
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

       
        ttk.Label(top_frame, text="行数：").grid(row=0, column=0, padx=5)
        self.row_var = tk.StringVar(value=str(self.generator.rows))
        row_entry = ttk.Entry(top_frame, textvariable=self.row_var, width=5)
        row_entry.grid(row=0, column=1, padx=5)

        ttk.Label(top_frame, text="列数：").grid(row=0, column=2, padx=5)
        self.col_var = tk.StringVar(value=str(self.generator.cols))
        col_entry = ttk.Entry(top_frame, textvariable=self.col_var, width=5)
        col_entry.grid(row=0, column=3, padx=5)

       
        ttk.Button(top_frame, text="应用行列", command=self._apply_rows_cols).grid(row=0, column=4, padx=5)

       
        ttk.Label(top_frame, text="对齐：").grid(row=0, column=5, padx=5)
        self.align_var = tk.StringVar(value=self.generator.align)
        align_combo = ttk.Combobox(top_frame, textvariable=self.align_var, values=["c", "l", "r"], width=5)
        align_combo.grid(row=0, column=6, padx=5)
        ttk.Button(top_frame, text="应用对齐", command=self._apply_align).grid(row=0, column=7, padx=5)

       
        self.border_var = tk.BooleanVar(value=self.generator.has_border)
        ttk.Checkbutton(top_frame, text="显示边框", variable=self.border_var, command=self._toggle_border).grid(row=0, column=8, padx=5)

        
        mid_frame = ttk.Frame(self.root)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

       
        edit_frame = ttk.LabelFrame(mid_frame, text="表格编辑")
        edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
       
        self.table = ttk.Treeview(edit_frame, show="headings")
        self._refresh_table()  
       
        self.table.bind("<Double-1>", self._edit_cell)
        
        v_scroll = ttk.Scrollbar(edit_frame, orient=tk.VERTICAL, command=self.table.yview)
        h_scroll = ttk.Scrollbar(edit_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

       
        preview_frame = ttk.LabelFrame(mid_frame, text="LaTeX 代码预览")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
       
        self.code_text = tk.Text(preview_frame, font=("Consolas", 11))
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Button(preview_frame, text="复制代码", command=self._copy_code).pack(side=tk.RIGHT, padx=5, pady=5)
       
        ttk.Button(preview_frame, text="刷新预览", command=self._refresh_preview).pack(side=tk.RIGHT, padx=5, pady=5)

      
        self._refresh_preview()

    def _refresh_table(self):
        """刷新表格编辑区"""
        
        for item in self.table.get_children():
            self.table.delete(item)
        
        self.table["columns"] = [f"col{i}" for i in range(self.generator.cols)]
        for i in range(self.generator.cols):
            self.table.heading(f"col{i}", text=f"列{i+1}")
            self.table.column(f"col{i}", width=100)
       
        for i, row in enumerate(self.generator.cells):
            self.table.insert("", tk.END, iid=i, values=row)

    def _apply_rows_cols(self):
        """应用行列数设置"""
        try:
            rows = int(self.row_var.get())
            cols = int(self.col_var.get())
            validate_table_params(rows, cols)
            self.generator.update_config(rows=rows, cols=cols)
            self._refresh_table()
            self._refresh_preview()
        except ValueError as e:
            messagebox.showerror("错误", f"参数非法：{str(e)}")

    def _apply_align(self):
        """应用对齐方式"""
        align = self.align_var.get()
        if align not in ["c", "l", "r"]:
            messagebox.warning("警告", "对齐方式仅支持 c(居中)/l(左)/r(右)")
            return
        self.generator.update_config(align=align)
        self._refresh_preview()

    def _toggle_border(self):
        """切换边框显示"""
        self.generator.update_config(has_border=self.border_var.get())
        self._refresh_preview()

    def _edit_cell(self, event):
        """编辑单元格内容"""
        try:
            item = self.table.selection()[0]
            col = self.table.identify_column(event.x)
            col_idx = int(col.replace("#", "")) - 1
            row_idx = int(item)
            
            current_content = self.generator.cells[row_idx][col_idx]
            
            new_content = simpledialog.askstring("编辑单元格", f"行{row_idx+1}列{col_idx+1}", initialvalue=current_content)
            if new_content is not None:
               
                new_content = clean_cell_content(new_content)
                self.generator.update_cell(row_idx, col_idx, new_content)
               
                self.table.set(item, f"col{col_idx}", new_content)
                self._refresh_preview()
        except IndexError:
            messagebox.warning("提示", "请选择要编辑的单元格")

    def _refresh_preview(self):
        """刷新代码预览区"""
        code = self.generator.generate_code()
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, code)

    def _copy_code(self):
        """复制代码到剪贴板"""
        code = self.code_text.get(1.0, tk.END).strip()
        pyperclip.copy(code)
        messagebox.showinfo("成功", "LaTeX表格代码已复制到剪贴板！")

    def run(self):
        """启动GUI界面"""
        self.root.mainloop()


if __name__ == "__main__":
    app = LaTeXTableDesignerGUI()
    app.run()
