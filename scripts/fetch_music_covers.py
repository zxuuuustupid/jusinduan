#!/usr/bin/env python3
"""获取网易云音乐封面图片并更新 showcase 文件"""

import json
import urllib.request
import re

# 歌曲 ID 列表
SONGS = [
    ("1823028083", "song1.md"),
    ("1996929972", "song2.md"),
    ("1907751319", "song3.md"),
]

API_URL = "https://music.163.com/api/song/detail/?ids=[{}]"


def get_cover_url(song_id: str) -> str:
    """通过网易云 API 获取歌曲封面 URL"""
    url = API_URL.format(song_id)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    songs = data.get("songs", [])
    if songs:
        return songs[0]["album"]["picUrl"]
    return None


def update_markdown_file(filepath: str, cover_url: str):
    """更新 markdown 文件中的封面 URL"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换 COVER_URL_X 为实际 URL
    new_content = re.sub(r'COVER_URL_\d+', cover_url, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated: {filepath}")
    print(f"  Cover URL: {cover_url}")


def main():
    print("Fetching album covers from NetEase Music...\n")

    for song_id, filename in SONGS:
        filepath = f"_showcase/music/{filename}"
        print(f"Song ID: {song_id}")

        try:
            cover_url = get_cover_url(song_id)
            if cover_url:
                update_markdown_file(filepath, cover_url)
                print()
            else:
                print(f"  Failed: No songs found for ID {song_id}\n")
        except Exception as e:
            print(f"  Error: {e}\n")

    print("Done!")


if __name__ == "__main__":
    main()
