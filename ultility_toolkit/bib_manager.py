from pathlib import Path

import requests


class BibFetchError(RuntimeError):
    """Raised when a DOI cannot be converted to BibTeX."""


def normalize_doi(doi: str) -> str:
    """Return a DOI without common URL prefixes or surrounding whitespace."""
    doi = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            return doi[len(prefix):].strip()
    return doi


def get_bibtex_from_doi(doi: str, timeout: int = 15) -> str:
    """Fetch a BibTeX entry from Crossref for the given DOI."""
    normalized_doi = normalize_doi(doi)
    if not normalized_doi:
        raise ValueError("DOI不能为空")

    url = f"https://api.crossref.org/works/{normalized_doi}/transform/application/x-bibtex"
    headers = {
        "Accept": "application/x-bibtex",
        "User-Agent": "LaTeX-Converter/0.1.0 (https://github.com/hope-sun123/LaTeX-Converter)",
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException as exc:
        raise BibFetchError(f"网络连接失败：{exc}") from exc

    if response.status_code == 404:
        raise BibFetchError(f"未找到 DOI：{normalized_doi}")
    if response.status_code != 200:
        raise BibFetchError(f"Crossref 返回状态码：{response.status_code}")

    bibtex = response.text.strip()
    if not bibtex.startswith("@"):
        raise BibFetchError("Crossref 返回的内容不是有效的 BibTeX 条目")
    return bibtex


def append_to_bib_file(content: str, filepath: str = "references.bib") -> str:
    """Append a BibTeX entry to a .bib file."""
    if not content.strip().startswith("@"):
        raise ValueError("内容不是有效的 BibTeX 条目，未写入文件")

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write("\n" + content.strip() + "\n")
    return f"成功！内容已追加到 {path}"
