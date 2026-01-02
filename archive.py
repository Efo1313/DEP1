# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"
LOGO_BASE = "https://www.seirsanduk.net/images/tvlogo/"

# TÜM KANAL İSİMLERİ VE LOGO EŞLEŞTİRMELERİ
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
    "12": {"name": "Diema Family", "logo": "diema-family.png"},
    "13": {"name": "Disney Channel", "logo": "disney-channel.png"},
    "14": {"name": "Cartoon Network", "logo": "cartoon-network.png"},
    "15": {"name": "Nickelodeon", "logo": "nickelodeon.png"},
    "17": {"name": "Fox", "logo": "fox.png"},
    "18": {"name": "Fox Life", "logo": "fox-life.png"},
    "19": {"name": "Fox Crime", "logo": "fox-crime.png"},
    "22": {"name": "National Geographic", "logo": "nat-geo.png"},
    "23": {"name": "Nat Geo Wild", "logo": "nat-geo-wild.png"},
    "24": {"name": "Discovery Channel", "logo": "discovery.png"},
    "25": {"name": "Animal Planet", "logo": "animal-planet.png"},
    "26": {"name": "TLC", "logo": "tlc.png"},
    "27": {"name": "Viasat Explore", "logo": "viasat-explore.png"},
    "28": {"name": "Viasat History", "logo": "viasat-history.png"},
    "29": {"name": "Viasat Nature", "logo": "viasat-nature.png"},
    "59": {"name": "HBO", "logo": "hbo.png"},
    "60": {"name": "HBO 2", "logo": "hbo-2.png"},
    "61": {"name": "Cinemax", "logo": "cinemax.png"},
    "62": {"name": "Cinemax 2", "logo": "cinemax-2.png"},
    "485": {"name": "Diema Sport HD", "logo": "diema-sport-hd.png"},
    "486": {"name": "Diema Sport 2 HD", "logo": "diema-sport-2-hd.png"},
    "487": {"name": "Diema Sport 3 HD", "logo": "diema-sport-3-hd.png"},
    "1049": {"name": "MAX Sport 1 HD", "logo": "max-sport-1-hd.png"},
    "1050": {"name": "MAX Sport 2 HD", "logo": "max-sport-2-hd.png"},
    "1051": {"name": "MAX Sport 3 HD", "logo": "max-sport-3-hd.png"},
    "1052": {"name": "MAX Sport 4 HD", "logo": "max-sport-4-hd.png"},
    "1053": {"name": "EuroSport 1 HD", "logo": "eurosport-1-hd.png"},
    "1054": {"name": "EuroSport 2 HD", "logo": "eurosport-2-hd.png"},
    "1932": {"name": "BNT 1 HD", "logo": "bnt-1-hd.png"},
    "1933": {"name": "BNT 2", "logo": "bnt-2.png"},
    "1934": {"name": "BNT 3 HD", "logo": "bnt-3-hd.png"}
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
    
    all_folders = get_links(ARCHIVE_URL)
    
    for folder in all_folders:
        channel_id = folder.strip("/")
        
        # Listede varsa ismi ve logosunu al, yoksa "Kanal [ID]" yap
        if channel_id in CHANNEL_DATA:
            ch_name = CHANNEL_DATA[channel_id]["name"]
            ch_logo = LOGO_BASE + CHANNEL_DATA[channel_id]["logo"]
        else:
            ch_name = f"Kanal {channel_id}"
            ch_logo = ""
            
        channel_url = ARCHIVE_URL + folder
        video_files = get_links(channel_url)
        video_files = [v for v in video_files if v.endswith('.mpg')]
        
        if video_files:
            video_files.sort(reverse=True)
            
            for video_file in video_files:
                video_full_url = channel_url + video_file
                raw_time = video_file.split('-')[-1].replace('.mpg', '')
                time_only = "".join(filter(str.isdigit, raw_time))
                
                if not time_only: continue
                
                # İSTEDİĞİN GÖRÜNÜM: Kanal Adı (Saat:00 - Tarih)
                display_name = f"{ch_name} ({time_only}:00 - {bugun})"
                
                f.write(f'#EXTINF:-1 tvg-logo="{ch_logo}" group-title="{ch_name}",{display_name}\n')
                f.write(f"{video_full_url}\n")
