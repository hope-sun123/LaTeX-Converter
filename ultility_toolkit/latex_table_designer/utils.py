#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""表格设计器辅助工具"""

def validate_table_params(rows, cols):
    """校验行列数是否合法"""
    if not isinstance(rows, int) or rows < 1:
        raise ValueError("行数必须是≥1的整数")
    if not isinstance(cols, int) or cols < 1:
        raise ValueError("列数必须是≥1的整数")
    return True

def clean_cell_content(content):
    """清理单元格内容（转义LaTeX特殊字符）"""
    special_chars = {
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}"
    }
    for char, escape_char in special_chars.items():
        content = content.replace(char, escape_char)
    return content