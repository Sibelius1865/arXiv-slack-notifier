from config import SEARCH_KEYWORDS, SEARCH_CATEGORY, SLACK_WEBHOOK_URL
from arxiv import search_arxiv
from notifier import post_to_slack

if __name__ == "__main__":
    papers = search_arxiv(SEARCH_KEYWORDS, SEARCH_CATEGORY)
    print(f"{len(papers)} 件の新着論文")
    post_to_slack(papers, SLACK_WEBHOOK_URL)
