import os

# İzlemek istediğin kanalların isimlerini ve YouTube linklerini buraya ekle
channels = [
    "NTV|https://www.youtube.com/watch?v=XWq5kBlakcQ",
    "HALK TV|https://www.youtube.com/watch?v=na_jT2Q1rfA",
    "HABERTURK|https://www.youtube.com/watch?v=ppS_P4lU_2E",
    "TRT HABER|https://www.youtube.com/watch?v=6I_mNoV9Yog",
    "SZC TV|https://www.youtube.com/watch?v=t6_fI-N5YhU"
]

def get_live_link(url):
    try:
        # En hızlı ve sade çekme komutu
        command = f'yt-dlp -g --format "best[ext=mp4]/best" --geo-bypass {url}'
        result = os.popen(command).read().strip()
        return result
    except:
        return None

# Dosyayı oluşturmaya başlıyoruz
with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    for channel in channels:
        name, url = channel.split("|")
        m3u8_url = get_live_link(url)
        
        if m3u8_url and "googlevideo" in m3u8_url:
            # Eğer gerçek linki bulduysak yazıyoruz
            f.write(f"#EXTINF:-1, {name}\n{m3u8_url}\n")
            print(f"Başarılı: {name}")
        else:
            # Bulamazsak, IPTV oynatıcının şansını denemesi için ana linki yazıyoruz
            f.write(f"#EXTINF:-1, {name} (YouTube Link)\n{url}\n")
            print(f"Uyarı: {name} için m3u8 alınamadı, ana link eklendi.")

print("İşlem başarıyla tamamlandı.")
