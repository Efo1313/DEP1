import os

# Kanal listesini güncel ve çalışan linklerle dolduralım
channels = [
    "NTV|https://www.youtube.com/watch?v=XWq5kBlakcQ",
    "HALK TV|https://www.youtube.com/watch?v=na_jT2Q1rfA",
    "HABERTURK|https://www.youtube.com/watch?v=ppS_P4lU_2E",
    "TRT HABER|https://www.youtube.com/watch?v=6I_mNoV9Yog"
]

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    # Dosyanın boş kalmaması için bir test satırı ekleyelim
    f.write("#EXTINF:-1, --- YOUTUBE LISTESI --- \nhttp://0.0.0.0\n")
    
    for channel in channels:
        try:
            name, url = channel.split("|")
            # --quiet ve --no-warnings ekleyerek sadece temiz linki alalım
            m3u8_url = os.popen(f"yt-dlp -g --format best --quiet --no-warnings {url}").read().strip()
            
            if m3u8_url and "googlevideo.com" in m3u8_url:
                f.write(f"#EXTINF:-1, {name}\n{m3u8_url}\n")
                print(f"Başarılı: {name}")
            else:
                print(f"Hata: {name} için link alınamadı.")
        except Exception as e:
            print(f"Sistem Hatası: {e}")

print("İşlem tamamlandı.")
