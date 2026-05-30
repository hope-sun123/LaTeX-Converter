
"""LaTeX表格代码生成核心逻辑（独立无依赖）"""

class LaTeXTableGenerator:
    def __init__(self):
        self.rows = 2  
        self.cols = 2  
        self.align = "c" 
        self.has_border = True 
        self.cells = [["单元格1", "单元格2"], ["单元格3", "单元格4"]]  

    def update_config(self, rows=None, cols=None, align=None, has_border=None):
        """更新表格配置（支持部分参数更新）"""
        if rows is not None and rows >= 1:
            self.rows = rows
        
            if len(self.cells) < self.rows:
                for _ in range(self.rows - len(self.cells)):
                    self.cells.append(["" for _ in range(self.cols)])
            else:
                self.cells = self.cells[:self.rows]
        
        if cols is not None and cols >= 1:
            self.cols = cols
            
            for i in range(len(self.cells)):
                if len(self.cells[i]) < self.cols:
                    self.cells[i].extend(["" for _ in range(self.cols - len(self.cells[i]))])
                else:
                    self.cells[i] = self.cells[i][:self.cols]
        
        if align is not None and align in ["c", "l", "r"]:
            self.align = align
        
        if has_border is not None:
            self.has_border = has_border

    def update_cell(self, row_idx, col_idx, value):
        """更新单个单元格内容"""
        if 0 <= row_idx < self.rows and 0 <= col_idx < self.cols:
            self.cells[row_idx][col_idx] = value

    def generate_code(self):
        """生成最终的LaTeX tabular代码"""
       
        col_format = self.align * self.cols
        if self.has_border:
            col_format = "|" + "|".join(list(col_format)) + "|"
        
      
        latex_code = f"\\begin{{tabular}}{{{col_format}}}\n"
        if self.has_border:
            latex_code += "    \\hline\n"
        
       
        for i, row in enumerate(self.cells):
            row_content = "    " + " & ".join(row) + " \\\\"
            latex_code += row_content + "\n"
            
            if self.has_border and i < self.rows - 1:
                latex_code += "    \\hline\n"
        
        
        if self.has_border:
            latex_code += "    \\hline\n"
        latex_code += "\\end{tabular}"
        
        return latex_code
