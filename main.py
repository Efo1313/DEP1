import os

# Kanal listeniz - Buraya istediğiniz kanalı ekleyebilirsiniz
channels = [
    "NTV|https://www.youtube.com/watch?v=pqq5c6k70kk",
    "Halk TV|https://www.youtube.com/watch?v=na_jT2Q1rfA"
]

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for channel in channels:
        name, url = channel.split("|")
        # YouTube linkini otomatik olarak m3u8 formatına çevirir
        m3u8_url = os.popen(f"yt-dlp -g {url}").read().strip()
        if m3u8_url:
            f.write(f"#EXTINF:-1,{name}\n{m3u8_url}\n")
