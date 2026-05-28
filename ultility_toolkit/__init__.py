__version__ = "0.1.0"
__description__ = "多功能Python实用工具集，支持文件处理、数据可视化、网络工具、文本转LaTeX"

__all__ = [
    "FileRenamer", "FileConverter", "FileSearcher",
    "DataPlotter", "DataAnalyzer",
    "IPQuery", "PortScanner", "URLChecker",
    "Text2LaTeXConverter"
]

_EXPORTS = {
    "FileRenamer": ("file_tools", "FileRenamer"),
    "FileConverter": ("file_tools", "FileConverter"),
    "FileSearcher": ("file_tools", "FileSearcher"),
    "DataPlotter": ("data_viz", "DataPlotter"),
    "DataAnalyzer": ("data_viz", "DataAnalyzer"),
    "IPQuery": ("network_tools", "IPQuery"),
    "PortScanner": ("network_tools", "PortScanner"),
    "URLChecker": ("network_tools", "URLChecker"),
    "Text2LaTeXConverter": ("latex_converter", "Text2LaTeXConverter"),
}


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = _EXPORTS[name]
    module = __import__(f"{__name__}.{module_name}", fromlist=[attr_name])
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
