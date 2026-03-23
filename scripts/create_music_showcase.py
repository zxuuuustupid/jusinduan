#!/usr/bin/env python3
"""获取歌曲封面图片并创建 showcase 文件"""

import json
import urllib.request
import os

# 用户提供的15首歌曲 ID
SONGS = [
    "30031110",
    "2097485077",
    "1815313772",
    "459717345",
    "2070095457",
    "2007052448",
    "28547513",
    "1325896851",
    "31081202",
    "33469880",
    "1960847105",
    "2745026895",
    "2685944153",
    "2034742057",
    "31967343",
]

API_URL = "https://music.163.com/api/song/detail/?ids=[{}]"


def get_song_info(song_id: str) -> dict:
    """通过网易云 API 获取歌曲信息"""
    url = API_URL.format(song_id)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    songs = data.get("songs", [])
    if songs:
        song = songs[0]
        return {
            "id": song_id,
            "name": song.get("name", "Unknown"),
            "artist": "/".join([a["name"] for a in song.get("artists", [])]),
            "cover": song["album"]["picUrl"],
        }
    return None


def create_showcase_md(filepath: str, song_id: str, cover_url: str, index: int, song_name: str = ""):
    """创建 showcase markdown 文件"""
    # 降序日期，保持和 song1-3 一致的格式
    date_offset = 12 - index  # song4 -> 8, song5 -> 7, ...

    content = f"""---
show: true
width: 2
date: 2024-01-{date_offset:02d} 00:01:00 +0800
group: Music
class: ""
---
<div>
<a href="https://music.163.com/song?id={song_id}" target="_blank">
    <img src="{cover_url}" class="img-fluid rounded-xl" alt="Album Cover">
</a>
</div>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print(f"Fetching {len(SONGS)} songs from NetEase Music...\n")

    music_dir = "_showcase/music"
    os.makedirs(music_dir, exist_ok=True)

    for i, song_id in enumerate(SONGS, start=4):
        filename = f"song{i}.md"
        filepath = os.path.join(music_dir, filename)

        print(f"[{i-3}/{len(SONGS)}] Song ID: {song_id}")

        try:
            info = get_song_info(song_id)
            if info:
                create_showcase_md(filepath, info["id"], info["cover"], i, info["name"])
                print(f"  Name: {info['name']}")
                print(f"  Artist: {info['artist']}")
                print(f"  Created: {filename}")
            else:
                print(f"  Failed: No song found")
        except Exception as e:
            print(f"  Error: {e}")

        print()

    print("=" * 50)
    print(f"Done! Created song4.md to song18.md")
    print(f"Total songs in _showcase/music/: 18")


if __name__ == "__main__":
    main()
