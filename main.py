import os
import datetime
import requests

# Kanal listesi
channels = [
    "CNN Turk|UCV6zcRug6Hqp1UX_FdyUeBg",
    "Haber Turk|UCn6dNfiRE_Xunu7iMyvD7AA",
    "NTV|UC9TDTjbOjFB9jADmPhSAPsw",
    "Haber Global|UCtc-a9ZUIg0_5HpsPxEO7Qg",
    "TRT Haber|UCBgTP2LOFVPmq15W-RH-WXA",
    "A Spor|UCJElRTCNEmLemgirqvsW63Q",
    "Now Spor|UCHowoDxzhyCPQBzhOpeP4-w",
    "CNBC-e|UCaO-M1dXacMwtyg0Pvovk4w",
    "Bein Sport Haber|UCPe9vNjHF1kEExT5kHwc7aw",
    "TJK TV|UC_8NgeVv0Ccl96U6C7E_fSg"
]

now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
    f.write(f"#EXTM3U\n# Guncelleme: {now}\n")
    
    for channel in channels:
        name, channel_id = channel.split("|")
        # YONTEM 1: YouTube Video ID uzerinden dogrudan çekme
        try:
            # Önce kanalın canlı yayın video ID'sini bulalım
            search_url = f"https://www.youtube.com/embed/live_stream?channel={channel_id}"
            response = requests.get(search_url, timeout=10)
            
            # yt-dlp ile en yuksek kalite m3u8 linkini alalım
            cmd = f"yt-dlp --geo-bypass --no-warnings -g {search_url}"
            m3u8_link = os.popen(cmd).read().strip()
            
            if m3u8_link and "m3u8" in m3u8_link:
                f.write(f"#EXTINF:-1,{name}\n{m3u8_link}\n")
                print(f"BAŞARILI: {name}")
            else:
                print(f"HATA: {name} için m3u8 bulunamadı.")
        except Exception as e:
            print(f"Sistem Hatası: {name} -> {e}")

print("Islem bitti. Listeyi kontrol et.")
