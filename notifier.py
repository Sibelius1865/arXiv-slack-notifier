import requests

def post_to_slack(papers, webhook_url: str):
    """
    papers: list of dict (id, title, summary, authors, link, published)
    webhook_url: Slack Incoming Webhook URL
    """
    for p in papers:
        text = (
            f"*{p['title']}*\n"
            f"Authors: {', '.join(p['authors'])}\n"
            f"Published: {p['published']}\n"
            f"<{p['link']}|arXiv Link>\n\n"
            f"{p['summary'][:400]}..."  # 400文字だけサマリー表示
        )
        payload = {"text": text}
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            # ステータスコード確認
            if response.status_code == 200 and response.text.strip() == "ok":
                print(f"✅ Slack通知成功: {p['title']}")
            else:
                print(f"⚠️ Slack通知失敗: {response.status_code}, {response.text}")
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Slack通知エラー: {e}")
