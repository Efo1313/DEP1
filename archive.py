# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime
import os

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"

# YENİ LOGO LİSTESİ
CHANNEL_DATA = {
    "1932": {"name": "BNT 1", "logo": "https://i.hizliresim.com/2ub474j.png"},
    "16": {"name": "BNT 2", "logo": "https://i.hizliresim.com/rk2853y.png"},
    "54": {"name": "BNT 3", "logo": "https://i.hizliresim.com/39lts6a.png"},
    "17": {"name": "BNT 4", "logo": "https://i.hizliresim.com/8tz6ugw.png"},
    "3": {"name": "Nova", "logo": "https://i.hizliresim.com/2bq59u9.png"},
    "43": {"name": "Nova News", "logo": "https://i.hizliresim.com/s1g6ly9.png"},
    "2": {"name": "bTV", "logo": "https://i.hizliresim.com/otlg64v.png"},
    "18": {"name": "Bulgaria ON AIR", "logo": "https://i.hizliresim.com/66jre4l.png"},
    "87": {"name": "Euronews", "logo": "https://i.hizliresim.com/fco0mxc.png"},
    "11": {"name": "bTV Action", "logo": "https://i.hizliresim.com/ge6news.png"},
    "4": {"name": "bTV Cinema", "logo": "https://i.hizliresim.com/9b6i9by.png"},
    "6": {"name": "bTV Comedy", "logo": "https://i.hizliresim.com/streq9v.png"},
    "13": {"name": "bTV Story", "logo": "https://i.hizliresim.com/86a7ix8.png"},
    "5": {"name": "Diema", "logo": "https://i.hizliresim.com/tpuby2q.png"},
    "12": {"name": "Diema Family", "logo": "https://i.hizliresim.com/s6j1299.png"},
    "9": {"name": "Kino Nova", "logo": "https://i.hizliresim.com/8z6j0zq.png"},
    "57": {"name": "STAR Crime", "logo": "https://i.hizliresim.com/ci9hsbx.png"},
    "56": {"name": "STAR Channel", "logo": "https://i.hizliresim.com/8t89vy4.png"},
    "58": {"name": "STAR Life", "logo": "https://i.hizliresim.com/nk4g37t.png"},
    "8": {"name": "AXN", "logo": "https://i.hizliresim.com/k5wyvth.png"},
    "14": {"name": "AXN Black", "logo": "https://i.hizliresim.com/ovngoqt.png"},
    "15": {"name": "AXN White", "logo": "https://i.hizliresim.com/1jgzk8r.png"},
    "66": {"name": "Nat Geo", "logo": "https://i.hizliresim.com/417bgpy.png"},
    "65": {"name": "Nat Geo Wild", "logo": "https://i.hizliresim.com/dvw80ug.png"},
    "38": {"name": "Discovery", "logo": "https://i.hizliresim.com/sif2sjf.png"},
    "746": {"name": "24 Kitchen", "logo": "https://i.hizliresim.com/34ti4tu.png"},
    "86": {"name": "TLC", "logo": "https://i.hizliresim.com/jwzxbvd.png"},
    "47": {"name": "Eurosport 1", "logo": "https://i.hizliresim.com/hj1h57y.png"},
    "48": {"name": "Eurosport 2", "logo": "https://i.hizliresim.com/qx6mrva.png"},
    "485": {"name": "Diema Sport", "logo": "https://i.hizliresim.com/aeofcfr.png"},
    "592": {"name": "Diema Sport 2", "logo": "https://i.hizliresim.com/ad8uhas.png"},
    "1380": {"name": "Diema Sport 3", "logo": "https://i.hizliresim.com/6s0zh2x.png"},
    "1049": {"name": "MAX Sport 1", "logo": "https://i.hizliresim.com/6mz83ad.png"},
    "1498": {"name": "MAX Sport 2", "logo": "https://i.hizliresim.com/18djvhy.png"},
    "1721": {"name": "MAX Sport 3", "logo": "https://i.hizliresim.com/kayjpc2.png"},
    "1752": {"name": "MAX Sport 4", "logo": "https://i.hizliresim.com/45c5pf1.png"},
    "76": {"name": "Ring", "logo": "https://i.hizliresim.com/palwmce.png"},
    "10": {"name": "Nova Sport", "logo": "https://i.hizliresim.com/jr6z84f.png"},
    "49": {"name": "Evrokom", "logo": "https://i.hizliresim.com/ovtv2we.png"},
    "197": {"name": "7/8 TV", "logo": "https://i.hizliresim.com/4w9htsr.png"},
    "80": {"name": "Skat TV", "logo": "https://i.hizliresim.com/bzp729r.png"},
    "34": {"name": "Cartoon Network", "logo": "https://i.hizliresim.com/tsuodvd.png"},
    "1931": {"name": "Disney Channel", "logo": "https://i.hizliresim.com/1uphxzl.png"},
    "46": {"name": "EKids", "logo": "https://i.hizliresim.com/pwo6mmu.png"},
    "192": {"name": "Nick Jr", "logo": "https://i.hizliresim.com/r7lznoh.png"},
    "209": {"name": "Nickelodeon", "logo": "https://i.hizliresim.com/9iw8age.png"},
    "7": {"name": "HBO 3", "logo": "https://i.hizliresim.com/d5qdqb3.png"},
    "59": {"name": "HBO", "logo": "https://i.hizliresim.com/ea7kaop.png"},
    "137": {"name": "HBO 2", "logo": "https://i.hizliresim.com/g4v1cop.png"},
    "20": {"name": "ALFA Ataka", "logo": "https://i.hizliresim.com/ka3h7hz.png"},
    "21": {"name": "Animal Planet", "logo": "https://i.hizliresim.com/95spf00.png"},
    "29": {"name": "Cartoonito", "logo": "https://i.hizliresim.com/8tvmxda.png"},
    "89": {"name": "TV 1000", "logo": "https://i.hizliresim.com/j9obm2h.png"},
    "92": {"name": "TVT", "logo": "https://i.hizliresim.com/6fxoukd.png"},
    "94": {"name": "Viasat Explore", "logo": "https://i.hizliresim.com/s2403gs.png"},
    "95": {"name": "Viasat History", "logo": "https://i.hizliresim.com/lb9mlqx.png"},
    "96": {"name": "Viasat Nature", "logo": "https://i.hizliresim.com/aolr613.png"},
    "114": {"name": "Agro TV", "logo": "https://i.hizliresim.com/31ifmd8.png"}
}

def get_links(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=20, headers=headers)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l not in ['../', './']]
    except:
        return []

# --- YENİ SIRALAMA FONKSİYONU ---
def get_sorted_channels(found_folders):
    try:
        with open('siralama.txt', 'r', encoding='utf-8') as f:
            target_order = [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return found_folders

    sorted_folders = []
    # Bulunan klasörleri isimleriyle eşleştirmek için bir harita oluştur
    folder_map = {}
    for folder in found_folders:
        cid = folder.strip("/")
        if cid in CHANNEL_DATA:
            folder_map[CHANNEL_DATA[cid]["name"].lower()] = folder

    # 1. Sıralama dosyasına göre ekle
    for name in target_order:
        if name in folder_map:
            sorted_folders.append(folder_map[name])
            del folder_map[name] # Eklenenleri haritadan sil

    # 2. Dosyada olmayan ama bulunan diğer her şeyi sona ekle
    for remaining_folder in folder_map.values():
        sorted_folders.append(remaining_folder)
        
    return sorted_folders

output_file = "seyir_sandigi.m3u"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    found_folders = get_links(ARCHIVE_URL)
    
    # --- SIRALAMA BURADA DEVREYE GİRİYOR ---
    ordered_folders = get_sorted_channels(found_folders)
    
    for folder in ordered_folders:
        channel_id = folder.strip("/")
        
        if channel_id in CHANNEL_DATA:
            data = CHANNEL_DATA[channel_id]
            channel_url = ARCHIVE_URL + folder
            
            video_files = get_links(channel_url)
            video_files = [v for v in video_files if v.endswith('.mpg')]
            
            if video_files:
                video_files.sort(reverse=True)
                
                # Son 48 saati alalım
                for video_file in video_files[:48]:
                    video_url = channel_url + video_file
                    
                    match = re.search(r'(\d{4})(\d{2})(\d{2})-(\d{2})', video_file)
                    
                    if match:
                        yil, ay, gun, saat = match.groups()
                        v_tarih = f"{gun}.{ay}"
                        v_saat = saat
                    else:
                        continue
                    
                    logo_url = data["logo"]
                    display_name = f"{data['name']} ({v_saat}:00 - {v_tarih})"
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{data["name"]}",{display_name}\n')
                    f.write(f"{video_url}\n")

print(f"Bitti! siralama.txt dosyasına göre {output_file} oluşturuldu.")
