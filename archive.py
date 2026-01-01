import requests
import re
import os

ARCHIVE_URL = "http://85.11.144.8/archive/"

# Logoların alınacağı ana adres (GitHub logo arşivi örneği)
LOGO_BASE = "https://raw.githubusercontent.com/vignis/LyngSat-Logo/master/logos/"

# Kanal isimleri ve Logo dosyaları (Örnek eşleşmeler)
CHANNEL_DATA = {
    "2": {"name": "bTV", "logo": "btv-bg.png"},
    "3": {"name": "Nova", "logo": "nova-tv-bg.png"},
    "4": {"name": "bTV Cinema", "logo": "btv-cinema.png"},
    "5": {"name": "Diema", "logo": "diema.png"},
    "89": {"name": "TV 1000", "logo": "tv-1000.png"},
    "1932": {"name": "BNT 1", "logo": "bnt-1.png"}
    # Diğerlerini de bu mantıkla doldurabiliriz
}

def get_links(url):
    try:
        response = requests.get(url, timeout=15)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l not in ['../', './']]
    except:
        return []

output_file = "seyir_sandigi.m3u"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    found_folders = get_links(ARCHIVE_URL)
    
    for folder in found_folders:
        channel_id = folder.replace("/", "")
        data = CHANNEL_DATA.get(channel_id, {"name": f"Channel {channel_id}", "logo": ""})
        
        channel_url = ARCHIVE_URL + folder
        video_files = get_links(channel_url)
        
        if video_files:
            video_files.reverse() 
            
            for video_file in video_files:
                video_url = channel_url + video_file
                time_label = video_file.split('-')[-1].replace('.mpg', '')
                
                # LOGO BURAYA EKLENİYOR (tvg-logo etiketiyle)
                logo_url = LOGO_BASE + data["logo"] if data["logo"] else ""
                
                f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{data["name"]}", {data["name"]} - Saat {time_label}:00\n')
                f.write(f"{video_url}\n")
