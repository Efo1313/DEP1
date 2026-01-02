# -*- coding: utf-8 -*-
import requests
import re
import os
from datetime import datetime

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"
LOGO_BASE = "https://www.seirsanduk.net/images/tvlogo/"

# Özel Logolu Kanallar
CHANNEL_DATA = {
    "2": {"name": "bTV HD", "logo": "btv-hd.png"},
    "3": {"name": "Nova TV HD", "logo": "nova-tv-hd.png"},
    "4": {"name": "bTV Cinema", "logo": "btv-cinema.png"},
    "5": {"name": "Diema", "logo": "diema.png"},
    "6": {"name": "bTV Comedy HD", "logo": "btv-comedy-hd.png"},
    "7": {"name": "HBO 3", "logo": "hbo-3.png"},
    "8": {"name": "AXN", "logo": "axn.png"},
    "9": {"name": "Kino Nova", "logo": "kino-nova.png"},
    "10": {"name": "Nova Sport HD", "logo": "nova-sport-hd.png"},
    "11": {"name": "bTV Action HD", "logo": "btv-action-hd.png"},
    "59": {"name": "HBO", "logo": "hbo.png"},
    "485": {"name": "Diema Sport HD", "logo": "diema-sport-hd.png"},
    "1049": {"name": "MAX Sport 1 HD", "logo": "max-sport-1-hd.png"},
    "1932": {"name": "BNT 1 HD", "logo": "bnt-1-hd.png"}
}

def get_links(url):
    try:
        response = requests.get(url, timeout=15)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l not in ['../', './']]
    except:
        return []

output_file = "seyir_sandigi.m3u"
bugun = datetime.now().strftime("%d.%m")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    found_folders = get_links(ARCHIVE_URL)
    
    for folder in found_folders:
        channel_id = folder.strip("/")
        
        # Kanal ismi belirleme
        if channel_id in CHANNEL_DATA:
            name = CHANNEL_DATA[channel_id]["name"]
            logo = LOGO_BASE + CHANNEL_DATA[channel_id]["logo"]
        else:
            name = f"Kanal {channel_id}"
            logo = ""
        
        channel_url = ARCHIVE_URL + folder
        video_files = get_links(channel_url)
        
        if video_files:
            video_files.reverse() 
            
            for video_file in video_files:
                if not video_file.endswith('.mpg'):
                    continue
                    
                video_url = channel_url + video_file
                
                # Saati temizle ve sadece rakamları al
                raw_time = video_file.split('-')[-1].replace('.mpg', '')
                time_label = "".join(filter(str.isdigit, raw_time))
                
                if not time_label: continue
                
                # YENİ GÖRÜNÜM: Saat başa, tarih sona (Örn: 18:00 - 02.01)
                display_name = f"{name} ({time_label}:00 - {bugun})"
                
                # M3U Yazımı
                f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{name}",{display_name}\n')
                f.write(f"{video_url}\n")
