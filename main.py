import os
import datetime
import requests

# Zaman damgası
now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

def get_fallback_links():
    """Eğer YouTube engellerse, internetteki açık kaynaklı m3u8 linklerini çekmeye çalışır."""
    try:
        # Örnek bir açık kaynaklı liste (Alternatif kanal havuzu)
        url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except:
        return ""
    return ""

print(f"İşlem başladı: {now}")

with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
    f.write(f"#EXTM3U\n# Guncelleme: {now}\n")
    
    # Kendi kanal listemizi de eklemeye çalışalım
    channels = [
        "CNN Turk|UCV6zcRug6Hqp1UX_FdyUeBg",
        "Haber Turk|UCn6dNfiRE_Xunu7iMyvD7AA",
        "NTV|UC9TDTjbOjFB9jADmPhSAPsw",
        "TRT Haber|UCBgTP2LOFVPmq15W-RH-WXA",
        "A Spor|UCJElRTCNEmLemgirqvsW63Q"
    ]

    for channel in channels:
        name, channel_id = channel.split("|")
        url = f"https://www.youtube.com/embed/live_stream?channel={channel_id}"
        cmd = f"yt-dlp --geo-bypass -g {url}"
        m3u8_link = os.popen(cmd).read().strip()
        
        if m3u8_link and "m3u8" in m3u8_link:
            f.write(f"#EXTINF:-1,{name}\n{m3u8_link}\n")
            print(f"Başarılı: {name}")

    # Eğer YouTube engellediyse ve liste çok kısaysa yedek havuzdan ekleme yap
    f.write("\n# --- YEDEK KANALLAR ---\n")
    f.write(get_fallback_links())

print("Liste güncellendi.")
