import os

channels = [
    "NTV|https://www.youtube.com/watch?v=XWq5kBlakcQ",
    "HALK TV|https://www.youtube.com/watch?v=na_jT2Q1rfA",
    "HABERTURK|https://www.youtube.com/watch?v=ppS_P4lU_2E",
    "TRT HABER|https://www.youtube.com/watch?v=6I_mNoV9Yog"
]

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    for channel in channels:
        try:
            name, url = channel.split("|")
            # Kendimizi Google Chrome gibi tanıtıyoruz (User-Agent)
            command = f'yt-dlp --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" -g --format best {url}'
            
            m3u8_url = os.popen(command).read().strip()
            
            if m3u8_url and "googlevideo" in m3u8_url:
                f.write(f"#EXTINF:-1, {name}\n{m3u8_url}\n")
                print(f"Başarılı: {name}")
            else:
                print(f"Hata: {name} için link boş döndü.")
        except Exception as e:
            print(f"Sistem Hatası: {e}")
