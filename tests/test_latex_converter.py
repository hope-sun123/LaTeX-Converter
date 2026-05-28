import unittest

from ultility_toolkit.latex_converter import Text2LaTeXConverter


class Text2LaTeXConverterTests(unittest.TestCase):
    def test_heading_and_list_conversion(self):
        source = "# Title\n\n- item one\n- item two"

        result = Text2LaTeXConverter().convert(source, add_document_env=False)

        self.assertIn(r"\section{Title}", result)
        self.assertIn(r"\begin{itemize}", result)
        self.assertIn(r"\item item one", result)
        self.assertIn(r"\end{itemize}", result)

    def test_code_block_uses_verbatim_without_text_escaping(self):
        source = "```python\nprint(a_b & c)\n```"

        result = Text2LaTeXConverter().convert(source, add_document_env=False)

        self.assertEqual(
            result,
            "\\begin{verbatim}\nprint(a_b & c)\n\\end{verbatim}",
        )


if __name__ == "__main__":
    unittest.main()
