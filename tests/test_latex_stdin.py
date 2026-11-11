import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cli


class LatexConvertStdinTests(unittest.TestCase):
    """Piped stdin must be converted, not eaten by the mode prompt."""

    def run_latex_convert(self, stdin_text):
        stdin = io.StringIO(stdin_text)
        with patch.object(sys, "argv", ["cli.py", "latex-convert"]), patch.object(
            sys, "stdin", stdin
        ):
            buf = io.StringIO()
            with redirect_stdout(buf):
                result = cli.main()
        return result, buf.getvalue()

    def test_piped_stdin_converts_to_full_document(self):
        result, out = self.run_latex_convert("# Hello\n")
        self.assertIsNone(result)
        self.assertIn("\\section{Hello}", out)
        self.assertIn("\\documentclass", out)

    def test_explicit_no_env_still_yields_fragment(self):
        stdin = io.StringIO("Hello world\n")
        argv = ["cli.py", "latex-convert", "--no-env"]
        with patch.object(sys, "argv", argv), patch.object(sys, "stdin", stdin):
            buf = io.StringIO()
            with redirect_stdout(buf):
                result = cli.main()
        self.assertIsNone(result)
        self.assertIn("Hello world", buf.getvalue())
        self.assertNotIn("\\documentclass", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
