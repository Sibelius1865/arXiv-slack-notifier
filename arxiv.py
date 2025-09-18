import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def search_arxiv(keywords: str, categories: str):
    """arXiv APIで過去24時間の新着論文を取得"""
    keywords = [
        f'(ti:"{k.strip()}" OR abs:"{k.strip()}")'
        for k in keywords.split(",")
    ]
    keyword_query = f"({' OR '.join(keywords)})"

    query = keyword_query
    if categories and categories.lower() != "all":
        categories = [f'cat:{c.strip()}' for c in categories.split(",")]
        query += f" AND ({' OR '.join(categories)})"

    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 30,
    }

    response = requests.get("http://export.arxiv.org/api/query", params=params, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)

    papers = []
    for entry in root.findall("atom:entry", ns):
        published_str = entry.find("atom:published", ns).text
        published_dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        if published_dt > yesterday:
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            papers.append(
                {
                    "id": arxiv_id,
                    "title": entry.find("atom:title", ns).text.strip(),
                    "summary": entry.find("atom:summary", ns).text.strip(),
                    "authors": [
                        a.find("atom:name", ns).text
                        for a in entry.findall("atom:author", ns)
                    ],
                    "link": f"https://arxiv.org/abs/{arxiv_id}",
                    "published": published_dt.strftime("%Y-%m-%d %H:%M UTC"),
                }
            )
    return papers

