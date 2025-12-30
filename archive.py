import requests
import re

# Seyir Sandığı Arşiv Adresi
ARCHIVE_URL = "http://85.11.144.8/archive/"

# Kanal ID'lerini ve Görünecek İsimlerini Tanımla
KANAL_AYARLARI = {
    "2": {"isim": "BTV ARŞİV", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/BTV_logo_2013.svg/200px-BTV_logo_2013.svg.png"},
    "3": {"isim": "NOVA TV ARŞİV", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Nova_TV_Logo_2011.png/200px-Nova_TV_Logo_2011.png"},
    "1932": {"isim": "BNT 1 ARŞİV", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/BNT_1_logo_2018.svg/200px-BNT_1_logo_2018.svg.png"}
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
        
        # Sadece .mpg uzantılı video dosyalarını al ve tarihe göre ters sırala (en yeni en üstte)
        video_files = sorted([f for f in files if f.endswith('.mpg')], reverse=True)
        
        # Her kanaldan son 24 saati (24 dosyayı) listeye ekle
        for video_file in video_files[:24]:
            video_url = folder_url + video_file
            
            try:
                # Örnek dosya: 20251230-22.mpg
                parcalar = video_file.split(".")[0].split("-")
                tarih = parcalar[0]
                saat = parcalar[1]
                
                gun = tarih[6:8]
                ay = AYLAR.get(tarih[4:6], tarih[4:6])
                
                ekran_ismi = f"{gun} {ay} - Saat {saat}:00"
            except:
                ekran_ismi = video_file

            # tvg-logo: Kanalın resmi görünür
            # group-title: Klasörleme yapar (BTV ARŞİV gibi)
            f.write(f'#EXTINF:-1 tvg-logo="{k_bilgi["logo"]}" group-title="{k_bilgi["isim"]}", {k_bilgi["isim"]} - {ekran_ismi}\n{video_url}\n')

print("Grup bazlı liste oluşturuldu!")
