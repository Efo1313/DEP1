# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"

# YENİ LOGO LİSTESİ (Hizliresim linkleri entegre edildi)
CHANNEL_DATA = {
    "1932": {"name": "BNT 1", "logo": "https://i.hizliresim.com/2ub474j.png"}
    "2": {"name": "bTV", "logo": "https://i.hizliresim.com/otlg64v.png"},
    "3": {"name": "Nova", "logo": "https://i.hizliresim.com/2bq59u9.png"},
    "4": {"name": "bTV Cinema", "logo": "https://i.hizliresim.com/9b6i9by.png"},
    "5": {"name": "Diema", "logo": "https://i.hizliresim.com/tpuby2q.png"},
    "6": {"name": "bTV Comedy", "logo": "https://i.hizliresim.com/streq9v.png"},
    "7": {"name": "HBO 3", "logo": "https://i.hizliresim.com/d5qdqb3.png"},
    "8": {"name": "AXN", "logo": "https://i.hizliresim.com/k5wyvth.png"},
    "9": {"name": "Kino Nova", "logo": "https://i.hizliresim.com/8z6j0zq.png"},
    "10": {"name": "Nova Sport", "logo": "https://i.hizliresim.com/jr6z84f.png"},
    "11": {"name": "bTV Action", "logo": "https://i.hizliresim.com/ge6news.png"},
    "12": {"name": "Diema Family", "logo": "https://i.hizliresim.com/s6j1299.png"},
    "13": {"name": "bTV Story", "logo": "https://i.hizliresim.com/86a7ix8.png"},
    "14": {"name": "AXN Black", "logo": "https://i.hizliresim.com/ovngoqt.png"},
    "15": {"name": "AXN White", "logo": "https://i.hizliresim.com/1jgzk8r.png"},
    "16": {"name": "BNT 2", "logo": "https://i.hizliresim.com/rk2853y.png"},
    "17": {"name": "BNT 4", "logo": "https://i.hizliresim.com/8tz6ugw.png"},
    "18": {"name": "Bulgaria ON AIR", "logo": "https://i.hizliresim.com/66jre4l.png"},
    "20": {"name": "ALFA Ataka", "logo": "https://i.hizliresim.com/ka3h7hz.png"},
    "21": {"name": "Animal Planet", "logo": "https://i.hizliresim.com/95spf00.png"},
    "29": {"name": "Cartoonito", "logo": "https://i.hizliresim.com/8tvmxda.png"},
    "34": {"name": "Cartoon Network", "logo": "https://i.hizliresim.com/tsuodvd.png"},
    "38": {"name": "Discovery", "logo": "https://i.hizliresim.com/sif2sjf.png"},
    "43": {"name": "Nova News", "logo": "https://i.hizliresim.com/s1g6ly9.png"},
    "46": {"name": "EKids", "logo": "https://i.hizliresim.com/pwo6mmu.png"},
    "47": {"name": "Eurosport 1", "logo": "https://i.hizliresim.com/hj1h57y.png"},
    "48": {"name": "Eurosport 2", "logo": "https://i.hizliresim.com/qx6mrva.png"},
    "49": {"name": "Evrokom", "logo": "https://i.hizliresim.com/ovtv2we.png"},
    "54": {"name": "BNT 3", "logo": "https://i.hizliresim.com/39lts6a.png"},
    "56": {"name": "STAR Channel", "logo": "https://i.hizliresim.com/8t89vy4.png"},
    "57": {"name": "STAR Crime", "logo": "https://i.hizliresim.com/ci9hsbx.png"},
    "58": {"name": "STAR Life", "logo": "https://i.hizliresim.com/nk4g37t.png"},
    "59": {"name": "HBO", "logo": "https://i.hizliresim.com/ea7kaop.png"},
    "65": {"name": "Nat Geo Wild", "logo": "https://i.hizliresim.com/dvw80ug.png"},
    "66": {"name": "Nat Geo", "logo": "https://i.hizliresim.com/417bgpy.png"},
    "76": {"name": "Ring", "logo": "https://i.hizliresim.com/palwmce.png"},
    "80": {"name": "Skat TV", "logo": "https://i.hizliresim.com/bzp729r.png"},
    "86": {"name": "TLC", "logo": "https://i.hizliresim.com/jwzxbvd.png"},
    "87": {"name": "Euronews", "logo": "https://i.hizliresim.com/fco0mxc.png"},
    "89": {"name": "TV 1000", "logo": "https://i.hizliresim.com/j9obm2h.png"},
    "92": {"name": "TVT", "logo": "https://i.hizliresim.com/6fxoukd.png"},
    "94": {"name": "Viasat Explore", "logo": "https://i.hizliresim.com/s2403gs.png"},
    "95": {"name": "Viasat History", "logo": "https://i.hizliresim.com/lb9mlqx.png"},
    "96": {"name": "Viasat Nature", "logo": "https://i.hizliresim.com/aolr613.png"},
    "114": {"name": "Agro TV", "logo": "https://i.hizliresim.com/31ifmd8.png"},
    "137": {"name": "HBO 2", "logo": "https://i.hizliresim.com/g4v1cop.png"},
    "192": {"name": "Nick Jr", "logo": "https://i.hizliresim.com/r7lznoh.png"},
    "197": {"name": "7/8 TV", "logo": "https://i.hizliresim.com/4w9htsr.png"},
    "209": {"name": "Nickelodeon", "logo": "https://i.hizliresim.com/9iw8age.png"},
    "485": {"name": "Diema Sport", "logo": "https://i.hizliresim.com/aeofcfr.png"},
    "592": {"name": "Diema Sport 2", "logo": "https://i.hizliresim.com/ad8uhas.png"},
    "746": {"name": "24 Kitchen", "logo": "https://i.hizliresim.com/34ti4tu.png"},
    "1049": {"name": "MAX Sport 1", "logo": "https://i.hizliresim.com/6mz83ad.png"},
    "1380": {"name": "Diema Sport 3", "logo": "https://i.hizliresim.com/6s0zh2x.png"},
    "1498": {"name": "MAX Sport 2", "logo": "https://i.hizliresim.com/18djvhy.png"},
    "1721": {"name": "MAX Sport 3", "logo": "https://i.hizliresim.com/kayjpc2.png"},
    "1752": {"name": "MAX Sport 4", "logo": "https://i.hizliresim.com/45c5pf1.png"},
    "1931": {"name": "Disney Channel", "logo": "https://i.hizliresim.com/1uphxzl.png"},
    "1932": {"name": "BNT 1", "logo": "https://i.hizliresim.com/2ub474j.png"}
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
    
    found_folders = get_links(ARCHIVE_URL)
    
    for folder in found_folders:
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
                    
                    logo_url = data["logo"] # Doğrudan listedeki yeni linki kullanıyoruz
                    display_name = f"{data['name']} ({v_saat}:00 - {v_tarih})"
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{data["name"]}",{display_name}\n')
                    f.write(f"{video_url}\n")

print(f"Bitti! Yeni logolarla {output_file} dosyası oluşturuldu.")
