from .core import LaTeXTableGenerator

__all__ = ["LaTeXTableGenerator", "LaTeXTableDesignerGUI"]
__version__ = "0.1.0"


def __getattr__(name):
    if name != "LaTeXTableDesignerGUI":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from .gui import LaTeXTableDesignerGUI

    globals()[name] = LaTeXTableDesignerGUI
    return LaTeXTableDesignerGUI
