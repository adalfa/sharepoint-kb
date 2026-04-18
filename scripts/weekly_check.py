#!/usr/bin/env python3
"""Weekly SPSE CU knowledge-base check.

Runs from GitHub Actions (full egress, not Cloudflare-blocked). Fetches
Stefan Gossner's blog via RSS, compares against a small state file, and:
- opens a PR (tagged to @adalfa) when facts change
- posts a heartbeat comment to the 'SPSE weekly heartbeat' issue otherwise
"""
import json
import os
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / ".weekly-state.json"
UA = "Mozilla/5.0 (compatible; sharepoint-kb-weekly/1.0; +https://github.com/adalfa/sharepoint-kb)"
HEARTBEAT_TITLE = "SPSE weekly heartbeat"
APR_POST = "https://blog.stefan-gossner.com/2026/04/14/april-2026-cu-for-sharepoint-server-subscription-edition-is-available-for-download"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_items(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out = []
    for item in root.iter("item"):
        out.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "pubDate": (item.findtext("pubDate") or "").strip(),
        })
    return out


def gh(*args: str) -> str:
    r = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return r.stdout


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def heartbeat_issue_number() -> int:
    out = gh("issue", "list", "--state", "all", "--search",
             f"{HEARTBEAT_TITLE} in:title", "--json", "number,title")
    for issue in json.loads(out):
        if issue["title"] == HEARTBEAT_TITLE:
            return issue["number"]
    url = gh("issue", "create",
             "--title", HEARTBEAT_TITLE,
             "--body", "Weekly heartbeat comments from the scheduled SPSE CU check.",
             "--assignee", "adalfa").strip()
    return int(url.rsplit("/", 1)[-1])


def post_heartbeat(body: str) -> None:
    n = heartbeat_issue_number()
    gh("issue", "comment", str(n), "--body", body)


def main() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        feed = parse_items(fetch("https://blog.stefan-gossner.com/feed/"))
        newest = feed[0] if feed else None
        apr_comments = len(parse_items(fetch(APR_POST + "/feed/")))
    except Exception as exc:
        post_heartbeat(f"Heartbeat {today} UTC: fetch error — {type(exc).__name__}: {exc}")
        return 0

    prev = json.loads(STATE.read_text()) if STATE.exists() else {}
    current = {
        "newest_post_link": newest["link"] if newest else "",
        "newest_post_title": newest["title"] if newest else "",
        "newest_post_pubDate": newest["pubDate"] if newest else "",
        "apr2026_comment_count": apr_comments,
    }

    deltas = []
    if prev:
        if current["newest_post_link"] != prev.get("newest_post_link"):
            deltas.append(f"New post: **{current['newest_post_title']}** ({current['newest_post_pubDate']}) — {current['newest_post_link']}")
        if current["apr2026_comment_count"] != prev.get("apr2026_comment_count"):
            deltas.append(f"Apr 2026 CU comment count: {prev.get('apr2026_comment_count')} → {current['apr2026_comment_count']}")

    if deltas:
        branch = f"spse-weekly-{today}"
        git("config", "user.email", "action@github.com")
        git("config", "user.name", "spse-weekly-bot")
        git("checkout", "-b", branch)
        STATE.write_text(json.dumps(current, indent=2) + "\n")
        git("add", str(STATE))
        git("commit", "-m", f"Weekly check {today}: " + "; ".join(deltas))
        git("push", "-u", "origin", branch)
        body = "## Deltas detected\n\n" + "\n".join(f"- {d}" for d in deltas) + \
               "\n\nReview and extend `sharepoint-se-cu-kb.md` / `.json` as needed."
        gh("pr", "create",
           "--base", "main",
           "--head", branch,
           "--title", f"Weekly SPSE CU check — {today}",
           "--body", body,
           "--assignee", "adalfa",
           "--reviewer", "adalfa")
        return 0

    if current != prev:
        git("config", "user.email", "action@github.com")
        git("config", "user.name", "spse-weekly-bot")
        STATE.write_text(json.dumps(current, indent=2) + "\n")
        git("add", str(STATE))
        git("commit", "-m", f"Baseline state {today}")
        git("push")

    post_heartbeat(
        f"Heartbeat {today} UTC: no change. "
        f"Newest post: {current['newest_post_title']} ({current['newest_post_pubDate']}). "
        f"Apr 2026 CU comment count: {current['apr2026_comment_count']}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
