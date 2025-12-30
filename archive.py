import requests
import re

# Seyir Sandığı Arşiv Adresi
ARCHIVE_URL = "http://85.11.144.8/archive/"

# Kanal Bilgileri ve Logoları (Senin istediğin grup isimleri)
KANAL_AYARLARI = {
    "2": {"isim": "BTV", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/BTV_logo_2013.svg/200px-BTV_logo_2013.svg.png"},
    "3": {"isim": "NOVA TV", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Nova_TV_Logo_2011.png/200px-Nova_TV_Logo_2011.png"},
    "1932": {"isim": "BNT 1", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/BNT_1_logo_2018.svg/200px-BNT_1_logo_2018.svg.png"}
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
        
        # MPG dosyalarını bul ve tarihe göre ters sırala (En yeni en üstte)
        video_files = sorted([f for f in files if f.endswith('.mpg')], reverse=True)
        
        # Her kanaldan son 48 saatlik kaydı alalım
        for video_file in video_files[:48]:
            video_url = folder_url + video_file
            
            try:
                # 20251230-23.mpg -> Parçalara ayır
                parcalar = video_file.split(".")[0].split("-")
                tarih_ham = parcalar[0]
                saat = parcalar[1]
                
                gun = tarih_ham[6:8]
                ay_adi = AYLAR.get(tarih_ham[4:6], tarih_ham[4:6])
                
                # Senin istediğin format: "30 Aralık - Saat 23:00"
                kanal_gorunumu = f"{gun} {ay_adi} - Saat {saat}:00"
            except:
                kanal_gorunumu = video_file

            # M3U satırını senin örneğine tam uyacak şekilde yazıyoruz
            f.write(f'#EXTINF:-1 tvg-logo="{k_bilgi["logo"]}" group-title="{k_bilgi["isim"]}",{kanal_gorunumu}\n{video_url}\n')

print("Liste senin örneğine göre düzenlendi!")
