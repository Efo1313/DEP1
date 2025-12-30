import requests
import re

# Seyir Sandığı Arşiv Adresi
ARCHIVE_URL = "http://85.11.144.8/archive/"

# Wikipedia SVG linklerini IPTV'nin anlayacağı PNG formatına çevirdik
# Sonuna /512px-... ekleyerek cihazın okuyabileceği hale getirdik.
KANAL_AYARLARI = {
    "2": {
        "isim": "BTV", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/BTV_Bulgaria_logo.svg/512px-BTV_Bulgaria_logo.svg.png"
    },
    "3": {
        "isim": "NOVA TV", 
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d0/Nova_TV_Logo_2011.png/512px-Nova_TV_Logo_2011.png"
    },
    "1932": {
        "isim": "BNT 1", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/BNT_1_logo_2018.svg/512px-BNT_1_logo_2018.svg.png"
    }
}

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l != '../']
    except:
        return []

AYLAR = {"01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran", 
         "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"}

with open("seyir_sandigi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    for k_id, k_bilgi in KANAL_AYARLARI.items():
        folder_url = f"{ARCHIVE_URL}{k_id}/"
        files = get_links(folder_url)
        video_files = sorted([f for f in files if f.endswith('.mpg')], reverse=True)
        
        for video_file in video_files[:48]:
            video_url = folder_url + video_file
            
            try:
                parcalar = video_file.split(".")[0].split("-")
                tarih_ham = parcalar[0]
                saat = parcalar[1]
                gun = tarih_ham[6:8]
                ay_adi = AYLAR.get(tarih_ham[4:6], tarih_ham[4:6])
                display_name = f"{gun} {ay_adi} - Saat {saat}:00"
            except:
                display_name = video_file

            # tvg-logo artık doğrudan .png dosyasına gidiyor.
            f.write(f'#EXTINF:-1 tvg-name="{k_bilgi["isim"]}" tvg-logo="{k_bilgi["logo"]}" group-title="{k_bilgi["isim"]}",{display_name}\n{video_url}\n')

print("Logolar PNG formatına dönüştürüldü ve liste hazır!")
