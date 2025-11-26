import feedparser
for header, items in sections.items():
formatted = f"*{header}*\n"
for i in items:
formatted += f"• <{i['link']}|{i['title']}> — {i['summary'][:180]}...\n"
chunks.append(formatted)
return "\n\n".join(chunks)


# Main
if __name__ == "__main__":
cfg = load_config()


sections = {}


# Brainfood
bf_items = []
for url in cfg["sources"]["brainfood"]["urls"]:
bf_items.extend(fetch_rss(url))
sections["Recruiting Brainfood"] = bf_items[: cfg["limits"]["max_items"]]


# Pragmatic Engineer
pe_items = []
for url in cfg["sources"]["pragmatic_engineer"]["urls"]:
pe_items.extend(fetch_rss(url))
sections["The Pragmatic Engineer"] = pe_items[: cfg["limits"]["max_items"]]


# Layoffs
layoffs_items = [
fetch_simple_page(url) for url in cfg["sources"]["layoffs_fyi"]["urls"]
]
sections["Layoffs"] = layoffs_items


# Optional LinkedIn curated sheet
sheet_url = cfg["sources"]["linkedin_curated"].get("google_sheet_url")
if sheet_url:
res = requests.get(sheet_url)
lines = res.text.splitlines()[1:]
li_items = []
for line in lines:
cols = line.split(",")
if len(cols) >= 3:
li_items.append({
"title": cols[0],
"link": cols[1],
"summary": cols[2],
"date": ""
})
sections["LinkedIn Highlights"] = li_items[: cfg["limits"]["max_items"]]


# Build digest
digest_text = make_digest(sections)


# Send to Slack
webhook = os.environ.get(cfg["slack"]["webhook_env"])
post_to_slack(webhook, digest_text)
