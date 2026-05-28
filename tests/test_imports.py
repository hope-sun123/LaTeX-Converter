import unittest


class ImportTests(unittest.TestCase):
    def test_table_generator_import_does_not_require_gui_dependencies(self):
        from ultility_toolkit.latex_table_designer import LaTeXTableGenerator

        self.assertEqual(LaTeXTableGenerator().rows, 2)


if __name__ == "__main__":
    unittest.main()
