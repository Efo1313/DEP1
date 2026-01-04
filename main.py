import os
import datetime
import requests
import re

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
print(f"Islem basladi: {now}")

with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
    f.write(f"#EXTM3U\n# Guncelleme: {now}\n")
    
    for channel in channels:
        name, channel_id = channel.split("|")
        # YouTube Video ID'sini bulmak icin embed sayfasini tara
        try:
            url = f"https://www.youtube.com/embed/live_stream?channel={channel_id}"
            # yt-dlp'ye ek parametreler ekleyerek (hls-prefer-native) zorluyoruz
            cmd = f"yt-dlp --geo-bypass --user-agent 'Mozilla/5.0' --no-check-certificate --quiet -g {url}"
            m3u8_link = os.popen(cmd).read().strip()
            
            if m3u8_link and "m3u8" in m3u8_link:
                f.write(f"#EXTINF:-1,{name}\n{m3u8_link}\n")
                print(f"Basarili: {name}")
            else:
                print(f"Uyari: {name} icin link dondurulemedi.")
        except Exception as e:
            print(f"Hata olustu {name}: {e}")

print("Liste guncellendi.")
