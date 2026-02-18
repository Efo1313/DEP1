import requests
import re

# --- AYARLAR ---
WORKER_URL = "https://bg-dvr-canli.efomost2.workers.dev"
SIRALAMA_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/refs/heads/main/siralama.txt"
KITAP_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/refs/heads/main/archive.py"

def generate():
    try:
        print("Sıralama ve Kitap çekiliyor...")
        kitap_content = requests.get(KITAP_URL).text
        # Satır sonu karakterlerini temizleyerek sıralamayı al
        siralama_content = [line.strip() for line in requests.get(SIRALAMA_URL).text.splitlines() if line.strip()]

        # archive.py içindeki yapıyı yakalamak için daha esnek regex
        channels = {}
        # Bu regex: "ID": { "name": "Kanal", "logo": "Link" } yapısını her türlü boşlukta yakalar
        pattern = r'"(\d+)":\s*\{[\s\S]*?"name":\s*"([^"]*)"[\s\S]*?"logo":\s*"([^"]*)"'
        matches = re.findall(pattern, kitap_content)
        
        for cid, cname, clogo in matches:
            channels[cname.strip().lower()] = {"id": cid, "name": cname.strip(), "logo": clogo.strip()}

        print(f"Sözlükte {len(channels)} kanal tanımlı bulundu.")
        
        with open("canli_tv.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            bulunan_sayisi = 0
            for target_name in siralama_content:
                key = target_name.lower()
                if key in channels:
                    cdata = channels[key]
                    f.write(f'#EXTINF:-1 tvg-logo="{cdata["logo"]}" group-title="CANLI YAYIN",{cdata["name"]}\n')
                    f.write(f"{WORKER_URL}/{cdata['id']}\n")
                    bulunan_sayisi += 1
                else:
                    print(f"Uyarı: '{target_name}' ismi archive.py içinde bulunamadı.")

        print(f"İşlem Başarılı: {bulunan_sayisi} kanal ile 'canli_tv.m3u' hazırlandı.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    generate()
