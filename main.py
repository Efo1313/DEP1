import os

# YouTube Canlı Yayın Linkleri (Buraya istediğin kanalları ekle)
channels = [
    "NTV|https://www.youtube.com/watch?v=XWq5kBlakcQ",
    "Halk TV|https://www.youtube.com/watch?v=na_jT2Q1rfA",
    "Habertürk|https://www.youtube.com/watch?v=ppS_P4lU_2E"
]

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for channel in channels:
        try:
            name, url = channel.split("|")
            # yt-dlp ile YouTube linkinden gerçek yayın linkini çekiyoruz
            m3u8_url = os.popen(f"yt-dlp -g {url}").read().strip()
            if m3u8_url:
                f.write(f"#EXTINF:-1, {name}\n{m3u8_url}\n")
                print(f"Eklendi: {name}")
        except Exception as e:
            print(f"Hata oluştu ({channel}): {e}")
