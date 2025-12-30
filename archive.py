import requests
import re

# Arşiv Adresi
ARCHIVE_URL = "http://85.11.144.8/archive/"

# ÖĞRENDİĞİMİZ KANAL LİSTESİ
KANAL_ISIMLERI = {
    "2": "BTV",
    "3": "NOVA TV",
    "1932": "BNT 1"
}

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l != '../']
    except:
        return []

with open("seyir_sandigi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    folders = get_links(ARCHIVE_URL)
    
    for folder in folders:
        folder_id = folder.replace("/", "")
        
        # Sadece bildiğimiz veya listede olan kanalları ekleyelim
        if folder_id in KANAL_ISIMLERI:
            channel_name = KANAL_ISIMLERI[folder_id]
            folder_url = ARCHIVE_URL + folder
            files = get_links(folder_url)
            
            # .mpg ve .ts dosyalarını ara
            video_files = [f for f in files if f.endswith(('.mpg', '.ts'))]
            
            # Her kanaldan en yeni 10 kaydı ekle
            for video_file in video_files[-10:]:
                video_url = folder_url + video_file
                
                # Tarih ve saat ayıklama (Örn: 20251230-22.mpg)
                try:
                    tarih_saat = video_file.split(".")[0].split("-")
                    tarih_ham = tarih_saat[0] # 20251230
                    saat_ham = tarih_saat[1]  # 22
                    
                    gun = tarih_ham[6:8]
                    ay = tarih_ham[4:6]
                    etiket = f"{gun}/{ay} - {saat_ham}:00"
                except:
                    etiket = video_file
                
                f.write(f'#EXTINF:-1 group-title="BULGARİSTAN ARŞİV", {channel_name} ({etiket})\n{video_url}\n')

print("Arşiv listesi Nova TV ve BNT 1 ile güncellendi!")
