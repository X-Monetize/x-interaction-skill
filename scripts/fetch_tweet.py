#!/usr/bin/env python3
"""免费读取一条推文及其回复，输出精简 JSON。

数据源按顺序尝试：FxTwitter → VxTwitter → X 官方嵌入接口。
全部免登录、免 API Key，不涉及任何 X 账号。

用法：
    python3 fetch_tweet.py <推文链接或ID> [--replies N]
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

UA = "x-interaction-skill/1.0"
TIMEOUT = 15


def parse_id(arg):
    m = re.search(r"/status(?:es)?/(\d+)", arg)
    if m:
        return m.group(1)
    if arg.isdigit():
        return arg
    sys.exit(f"无法从输入中解析推文 ID：{arg}")


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def slim_fx(s):
    if not s:
        return None
    author = s.get("author") or {}
    quote = s.get("quote")
    media = s.get("media") or {}
    return {
        "url": s.get("url"),
        "text": s.get("text"),
        "created_at": s.get("created_at"),
        "lang": s.get("lang"),
        "author": {
            "screen_name": author.get("screen_name"),
            "name": author.get("name"),
            "followers": author.get("followers"),
            "description": author.get("description"),
        },
        "stats": {
            "likes": s.get("likes"),
            "replies": s.get("replies"),
            "reposts": s.get("reposts"),
            "quotes": s.get("quotes"),
            "views": s.get("views"),
        },
        "media": [m.get("type") for m in media.get("all") or []],
        "quoted": slim_fx(quote) if quote else None,
        "article_title": (s.get("article") or {}).get("title"),
    }


def from_fxtwitter(tid, n):
    d = get_json(f"https://api.fxtwitter.com/2/conversation/{tid}")
    status = d.get("status")
    if not status:
        raise ValueError(f"code={d.get('code')}")
    replies = []
    for r in (d.get("replies") or [])[:n]:
        replies.append({
            "author": (r.get("author") or {}).get("screen_name"),
            "text": r.get("text"),
            "likes": r.get("likes"),
        })
    return {
        "source": "fxtwitter",
        "tweet": slim_fx(status),
        "thread": [t.get("text") for t in d.get("thread") or [] if t.get("id") != tid],
        "replies": replies,
    }


def from_vxtwitter(tid, _n):
    d = get_json(f"https://api.vxtwitter.com/i/status/{tid}")
    return {
        "source": "vxtwitter",
        "tweet": {
            "url": d.get("tweetURL"),
            "text": d.get("text"),
            "created_at": d.get("date"),
            "lang": d.get("lang"),
            "author": {"screen_name": d.get("user_screen_name"), "name": d.get("user_name")},
            "stats": {"likes": d.get("likes"), "replies": d.get("replies"), "reposts": d.get("retweets")},
            "media": [m.get("type") for m in d.get("media_extended") or []],
        },
        "thread": [],
        "replies": [],
    }


def from_syndication(tid, _n):
    d = get_json(f"https://cdn.syndication.twimg.com/tweet-result?id={tid}&token=a")
    user = d.get("user") or {}
    return {
        "source": "syndication",
        "tweet": {
            "url": f"https://x.com/{user.get('screen_name')}/status/{tid}",
            "text": d.get("text"),
            "created_at": d.get("created_at"),
            "lang": d.get("lang"),
            "author": {"screen_name": user.get("screen_name"), "name": user.get("name")},
            "stats": {"likes": d.get("favorite_count"), "replies": d.get("conversation_count")},
        },
        "thread": [],
        "replies": [],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("target", help="推文链接或 ID")
    p.add_argument("--replies", type=int, default=15, help="最多返回几条回复（默认 15）")
    args = p.parse_args()

    tid = parse_id(args.target)
    errors = []
    for fetch in (from_fxtwitter, from_vxtwitter, from_syndication):
        try:
            result = fetch(tid, args.replies)
            if result["tweet"].get("text"):
                result["errors"] = errors
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return
            errors.append(f"{fetch.__name__}: 返回内容为空")
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError, TimeoutError) as e:
            errors.append(f"{fetch.__name__}: {e}")
    print(json.dumps({"error": "所有数据源都失败", "details": errors}, ensure_ascii=False, indent=2))
    sys.exit(1)


if __name__ == "__main__":
    main()
