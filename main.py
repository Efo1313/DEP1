import os

# Linkleri daha basit ve alternatif formatta çekmeyi deniyoruz
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
            # yt-dlp'ye 'geobypass' (coğrafi engeli aş) ve 'flat-playlist' komutları ekliyoruz
            cmd = f'yt-dlp -g --geo-bypass --no-check-certificate --format "best[ext=mp4]/best" {url}'
            m3u8_url = os.popen(cmd).read().strip()
            
            if m3u8_url:
                f.write(f"#EXTINF:-1, {name}\n{m3u8_url}\n")
                print(f"Başarılı: {name}")
            else:
                # Eğer link boşsa, IPTV oynatıcıların bazen çözebildiği ham linki ekle
                f.write(f"#EXTINF:-1, {name} (Alternatif)\n{url}\n")
        except:
            continue
