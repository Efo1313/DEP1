import requests
import re

# Arşivin ana adresi
ARCHIVE_URL = "http://85.11.144.8/archive/"

# Kanal isim eşleşmeleri
CHANNEL_NAMES = {
    "2": "bTV", "3": "Nova", "4": "bTV Cinema", "5": "Diema", "6": "bTV Comedy",
    "7": "HBO 3", "8": "AXN", "9": "Kino NOVA", "10": "Nova Sport", "11": "bTV Action",
    "12": "Diema Family", "13": "bTV Story", "14": "AXN Black", "15": "AXN White",
    "16": "BNT 2", "17": "BNT 4", "18": "ON AIR", "20": "ALFA Ataka", "21": "Animal Planet",
    "29": "Cartoonito", "34": "CN Cartoon", "38": "Discovery", "43": "Nova News",
    "46": "EKids", "47": "Eurosport 1", "48": "Eurosport 2", "49": "Evrokom",
    "54": "BNT 3", "56": "Star Channel", "57": "Star Crime", "58": "Star Life",
    "59": "HBO", "65": "NatGeo Wild", "66": "National Geographic", "76": "Ring",
    "80": "Skat", "86": "TLC", "87": "Euro News", "89": "TV 1000", "94": "Viasat Explore",
    "95": "Viasat History", "96": "Viasat Nature", "114": "Agro TV", "137": "HBO 2",
    "192": "NCKJR", "197": "7/8 TV", "209": "Nickelodeon", "485": "Diema Sport",
    "592": "Diema Sport 2", "746": "24 Kitchen", "1049": "Max Sport 1",
    "1380": "Diema Sport 3", "1498": "Max Sport 2", "1721": "Max Sport 3",
    "1752": "Max Sport 4", "1931": "Disney Channel", "1932": "BNT 1"
}

def get_links(url):
    try:
        response = requests.get(url, timeout=15)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l not in ['../', './']]
    except:
        return []

with open("seyir_sandigi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    print("Kanallar taranıyor...")
    found_folders = get_links(ARCHIVE_URL)
    
    for folder in found_folders:
        channel_id = folder.replace("/", "")
        display_name = CHANNEL_NAMES.get(channel_id, f"Channel {channel_id}")
        
        channel_url = ARCHIVE_URL + folder
        video_files = get_links(channel_url)
        
        if video_files:
            latest_videos = video_files[-5:] 
            
            for video_file in latest_videos:
                video_url = channel_url + video_file
                
                # --- DÜZELTİLEN KISIM BURASI ---
                # Dosya adındaki tarihi temizleyip sadece saati alıyoruz (Örn: 20260101-18.mpg -> 18:00)
                time_label = video_file.split('-')[-1].replace('.mpg', '')
                
                # group-title ekleyerek klasör yapıyoruz
                f.write(f'#EXTINF:-1 group-title="{display_name} Arşivi", {display_name} - Saat {time_label}:00\n')
                f.write(f"{video_url}\n")
                # ------------------------------

print("Tam liste düzenli ve klasörlü halde oluşturuldu: seyir_sandigi.m3u")
