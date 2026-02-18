import requests
import re

# --- AYARLAR ---
WORKER_URL = "https://bg-dvr-canli.efomost2.workers.dev"
# Kendi GitHub raw linklerini kontrol et, isimler tam aynı olsun
SIRALAMA_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/main/siralama.txt"
KITAP_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/main/archive.py"

def generate():
    try:
        print("Sıralama ve Kitap çekiliyor...")
        kitap_content = requests.get(KITAP_URL).text
        siralama_content = [line.strip() for line in requests.get(SIRALAMA_URL).text.splitlines() if line.strip()]

        # archive.py içinden Kanal İsmi, ID ve Logo eşleşmesini al
        channels = {}
        # Regex: ID ve Name-Logo çiftini yakalar
        pattern = r'"(\d+)":\s*\{[\s\S]*?"name":\s*"([^"]*)"[\s\S]*?"logo":\s*"([^"]*)"'
        matches = re.findall(pattern, kitap_content)
        
        for cid, cname, clogo in matches:
            channels[cname.strip().lower()] = {"id": cid, "name": cname.strip(), "logo": clogo.strip()}

        with open("canli_tv.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for target_name in siralama_content:
                key = target_name.lower()
                if key in channels:
                    cdata = channels[key]
                    # Link yapısı: workers_url / kanal_id
                    f.write(f'#EXTINF:-1 tvg-logo="{cdata["logo"]}" group-title="CANLI YAYIN",{cdata["name"]}\n')
                    f.write(f"{WORKER_URL}/{cdata['id']}\n")

        print("İşlem Başarılı: canli_tv.m3u güncellendi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    generate()
