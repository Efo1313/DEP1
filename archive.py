# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"
LOGO_BASE = "https://www.seirsanduk.net/images/tvlogo/"

# TAM KANAL LİSTESİ (63 KANAL)
CHANNEL_DATA = {
    "2": {"name": "bTV", "logo": "btv.png"},
    "3": {"name": "Nova", "logo": "nova.png"},
    "4": {"name": "bTV Cinema", "logo": "btv-cinema.png"},
    "5": {"name": "Diema", "logo": "diema.png"},
    "6": {"name": "bTV Comedy", "logo": "btv-comedy.png"},
    "7": {"name": "HBO 3", "logo": "hbo-3.png"},
    "8": {"name": "AXN", "logo": "axn.png"},
    "9": {"name": "Kino Nova", "logo": "kino-nova.png"},
    "10": {"name": "Nova Sport", "logo": "nova-sport.png"},
    "11": {"name": "bTV Action", "logo": "btv-action.png"},
    "12": {"name": "Diema Family", "logo": "diema-family.png"},
    "13": {"name": "bTV Story", "logo": "btv-story.png"},
    "14": {"name": "AXN Black", "logo": "axn-black.png"},
    "15": {"name": "AXN White", "logo": "axn-white.png"},
    "16": {"name": "BNT 2", "logo": "bnt-2.png"},
    "17": {"name": "BNT 4", "logo": "bnt-4.png"},
    "18": {"name": "Bulgaria ON AIR", "logo": "bulgaria-on-air.png"},
    "20": {"name": "ALFA Ataka", "logo": "alfa.png"},
    "21": {"name": "Animal Planet", "logo": "animal-planet.png"},
    "28": {"name": "28 TV", "logo": ""},
    "29": {"name": "Cartoonito", "logo": "cartoonito.png"},
    "34": {"name": "Cartoon Network", "logo": "cartoon-network.png"},
    "38": {"name": "Discovery", "logo": "discovery.png"},
    "43": {"name": "Nova News", "logo": "nova-news.png"},
    "46": {"name": "EKids", "logo": "ekids.png"},
    "47": {"name": "Eurosport 1", "logo": "eurosport-1.png"},
    "48": {"name": "Eurosport 2", "logo": "eurosport-2.png"},
    "49": {"name": "Evrokom", "logo": "evrokom.png"},
    "54": {"name": "BNT 3", "logo": "bnt-3.png"},
    "56": {"name": "STAR Channel", "logo": "star-channel.png"},
    "57": {"name": "STAR Crime", "logo": "star-crime.png"},
    "58": {"name": "STAR Life", "logo": "star-life.png"},
    "59": {"name": "HBO", "logo": "hbo.png"},
    "65": {"name": "NatGeo Wild", "logo": "nat-geo-wild.png"},
    "66": {"name": "National Geographic", "logo": "nat-geo.png"},
    "76": {"name": "Ring", "logo": "ring.png"},
    "79": {"name": "PULS TV", "logo": ""},
    "80": {"name": "Skat TV", "logo": "skat.png"},
    "86": {"name": "TLC", "logo": "tlc.png"},
    "87": {"name": "Euronews", "logo": "euronews.png"},
    "89": {"name": "TV 1000", "logo": "tv-1000.png"},
    "92": {"name": "TVT", "logo": "tvt.png"},
    "94": {"name": "Viasat Explore", "logo": "viasat-explore.png"},
    "95": {"name": "Viasat History", "logo": "viasat-history.png"},
    "96": {"name": "Viasat Nature", "logo": "viasat-nature.png"},
    "108": {"name": "108 TV", "logo": ""},
    "114": {"name": "Agro TV", "logo": "agro-tv.png"},
    "137": {"name": "HBO 2", "logo": "hbo-2.png"},
    "182": {"name": "182 TV", "logo": ""},
    "192": {"name": "Nick Jr", "logo": "nick-jr.png"},
    "197": {"name": "7/8 TV", "logo": "7-8-tv.png"},
    "209": {"name": "Nickelodeon", "logo": "nickelodeon.png"},
    "485": {"name": "Diema Sport", "logo": "diema-sport.png"},
    "592": {"name": "Diema Sport 2", "logo": "diema-sport-2.png"},
    "746": {"name": "24 Kitchen", "logo": "24-kitchen.png"},
    "1049": {"name": "MAX Sport 1", "logo": "max-sport-1.png"},
    "1380": {"name": "Diema Sport 3", "logo": "diema-sport-3.png"},
    "1498": {"name": "MAX Sport 2", "logo": "max-sport-2.png"},
    "1670": {"name": "1670 TV", "logo": ""},
    "1721": {"name": "MAX Sport 3", "logo": "max-sport-3.png"},
    "1752": {"name": "MAX Sport 4", "logo": "max-sport-4.png"},
    "1931": {"name": "Disney Channel", "logo": "disney.png"},
    "1932": {"name": "BNT 1", "logo": "bnt-1.png"}
}

def get_links(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=20, headers=headers)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l not in ['../', './']]
    except:
        return []

output_file = "seyir_sandigi.m3u"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    # Sunucudaki tüm klasörleri çek
    found_folders = get_links(ARCHIVE_URL)
    
    for folder in found_folders:
        channel_id = folder.strip("/")
        
        # Eğer bu klasör (ID) listemizde varsa işle
        if channel_id in CHANNEL_DATA:
            data = CHANNEL_DATA[channel_id]
            channel_url = ARCHIVE_URL + folder
            
            # Klasör içindeki .mpg dosyalarını al
            video_files = get_links(channel_url)
            video_files = [v for v in video_files if v.endswith('.mpg')]
            
            if video_files:
                # En yeni kayıt en üstte
                video_files.sort(reverse=True)
                
                # Çok fazla dosya olmaması için her kanaldan son 48 saati alalım
                for video_file in video_files[:48]:
                    video_url = channel_url + video_file
                    
                    # Regex ile tarih ve saat ayıkla (Örn: 20260101-14)
                    match = re.search(r'(\d{4})(\d{2})(\d{2})-(\d{2})', video_file)
                    
                    if match:
                        yil, ay, gun, saat = match.groups()
                        v_tarih = f"{gun}.{ay}"
                        v_saat = saat
                    else:
                        continue
                    
                    logo_url = LOGO_BASE + data["logo"] if data["logo"] else ""
                    display_name = f"{data['name']} ({v_saat}:00 - {v_tarih})"
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{data["name"]}",{display_name}\n')
                    f.write(f"{video_url}\n")

print(f"Bitti! 63 kanal için {output_file} dosyası oluşturuldu.")
