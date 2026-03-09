import requests

import requests

def get_bibtex_from_doi(doi):
    """通过 DOI 获取 BibTeX 文本（加强版）"""
    # 1. 清理输入的 DOI 字符串
    doi = doi.replace("https://doi.org/", "").strip()
    
    # 2. 使用 Crossref API 获取 BibTeX
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    
    # 3. 设置请求头（模拟浏览器）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.text.strip()
        elif response.status_code == 404:
            return f"错误：在该数据库中未找到 DOI {doi}，请检查编号。"
        else:
            return f"错误：服务器返回状态码 {response.status_code}"
    except Exception as e:
        return f"网络连接失败：{str(e)}"

def append_to_bib_file(content, filepath="references.bib"):
    """将获取到的内容追加到 .bib 文件中"""
    # 简单检查内容是否有效
    if "错误" in content or "失败" in content:
        return "由于获取内容失败，未写入文件。"
        
    # 以追加模式 ('a') 打开文件
    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n" + content + "\n")
    return f"成功！内容已追加到项目根目录下的 {filepath}"