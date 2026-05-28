import re
from typing import Optional, TextIO, List

class Text2LaTeXConverter:
    SPECIAL_CHARS = {
        '#': r'\#', '$': r'\$', '%': r'\%', '&': r'\&', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}', '\\': r'\textbackslash{}',
        '<': r'\textless{}', '>': r'\textgreater{}'
    }

    UNORDERED_LIST_PATTERN = re.compile(r'^\s*[-*+]\s+(.*)$')
    ORDERED_LIST_PATTERN = re.compile(r'^\s*\d+\.\s+(.*)$')
    HEADING_PATTERN = re.compile(r'^\s*(#{1,6})\s+(.*)$')
    CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)
    BOLD_PATTERN = re.compile(r'\*\*(.*?)\*\*')
    ITALIC_PATTERN = re.compile(r'\*(.*?)\*')

    def __init__(self):
        self.converted_content = ""

    def _escape_special_chars(self, text: str) -> str:
        for char, escaped in self.SPECIAL_CHARS.items():
            text = text.replace(char, escaped)
        return text

    def _format_inline_style(self, text: str) -> str:
        text = self.BOLD_PATTERN.sub(r'\textbf{\1}', text)
        text = self.ITALIC_PATTERN.sub(r'\textit{\1}', text)
        return text

    def _format_line(self, line: str) -> str:
        ul_match = self.UNORDERED_LIST_PATTERN.match(line)
        if ul_match:
            content = self._format_inline_style(self._escape_special_chars(ul_match.group(1)))
            return f"\\item {content}"

        ol_match = self.ORDERED_LIST_PATTERN.match(line)
        if ol_match:
            content = self._format_inline_style(self._escape_special_chars(ol_match.group(1)))
            return f"\\item {content}"

        h_match = self.HEADING_PATTERN.match(line)
        if h_match:
            level = len(h_match.group(1))
            title = self._format_inline_style(self._escape_special_chars(h_match.group(2)))
            if level == 1:
                return f"\\section{{{title}}}"
            elif level == 2:
                return f"\\subsection{{{title}}}"
            elif level == 3:
                return f"\\subsubsection{{{title}}}"
            elif level == 4:
                return f"\\paragraph{{{title}}}"
            else:
                return f"\\subparagraph{{{title}}}"

        line = self._format_inline_style(self._escape_special_chars(line))
        return line

    def _format_code_blocks(self, text: str) -> str:
        def replace_code_block(match):
            code = match.group(2)
            return f"\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}"
        return self.CODE_BLOCK_PATTERN.sub(replace_code_block, text)

    def convert(self, text: str, add_document_env: bool = True) -> str:
        code_blocks = []

        def stash_code_block(match):
            token = f"LATEXCODEBLOCK{len(code_blocks)}TOKEN"
            code_blocks.append(self._format_code_blocks(match.group(0)))
            return token

        text = self.CODE_BLOCK_PATTERN.sub(stash_code_block, text)
        lines = text.split('\n')
        converted_lines = []
        in_ul_list = False
        in_ol_list = False

        for line in lines:
            if line in {f"LATEXCODEBLOCK{i}TOKEN" for i in range(len(code_blocks))}:
                if in_ul_list:
                    converted_lines.append("\\end{itemize}")
                    in_ul_list = False
                if in_ol_list:
                    converted_lines.append("\\end{enumerate}")
                    in_ol_list = False
                index = int(line.removeprefix("LATEXCODEBLOCK").removesuffix("TOKEN"))
                converted_lines.append(code_blocks[index])
                continue

            if line.strip() == "":
                if in_ul_list:
                    converted_lines.append("\\end{itemize}")
                    in_ul_list = False
                if in_ol_list:
                    converted_lines.append("\\end{enumerate}")
                    in_ol_list = False
                converted_lines.append("")
                continue

            ul_match = self.UNORDERED_LIST_PATTERN.match(line)
            ol_match = self.ORDERED_LIST_PATTERN.match(line)

            if ul_match:
                if not in_ul_list:
                    converted_lines.append("\\begin{itemize}")
                    in_ul_list = True
                    in_ol_list = False
                converted_lines.append(self._format_line(line))
            elif ol_match:
                if not in_ol_list:
                    converted_lines.append("\\begin{enumerate}")
                    in_ol_list = True
                    in_ul_list = False
                converted_lines.append(self._format_line(line))
            else:
                if in_ul_list:
                    converted_lines.append("\\end{itemize}")
                    in_ul_list = False
                if in_ol_list:
                    converted_lines.append("\\end{enumerate}")
                    in_ol_list = False
                converted_lines.append(self._format_line(line))

        if in_ul_list:
            converted_lines.append("\\end{itemize}")
        if in_ol_list:
            converted_lines.append("\\end{enumerate}")

        body = '\n'.join(converted_lines)
        if add_document_env:
            self.converted_content = f"""\\documentclass{{article}}
\\usepackage[UTF8]{{ctex}}
\\usepackage{{verbatim}}
\\usepackage{{geometry}}
\\usepackage{{amsmath,amssymb}}
\\geometry{{a4paper, margin=1in}}

\\begin{{document}}
{body}
\\end{{document}}"""
        else:
            self.converted_content = body

        return self.converted_content

    def save_to_file(self, filepath: str):
        if not self.converted_content:
            raise ValueError("请先调用convert()方法完成转换")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.converted_content)

    @classmethod
    def from_file(cls, input_file: str, output_file: Optional[str] = None, add_document_env: bool = True) -> str:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        converter = cls()
        latex_content = converter.convert(text, add_document_env)
        if output_file:
            converter.save_to_file(output_file)
        return latex_content
