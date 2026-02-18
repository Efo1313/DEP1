import requests
import re

# --- AYARLAR ---
# Senin kurduğun Workers adresi
WORKER_URL = "https://bg-dvr-canli.efomost2.workers.dev"
# Verilerin çekileceği raw linkler
SIRALAMA_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/refs/heads/main/siralama.txt"
KITAP_URL = "https://raw.githubusercontent.com/Efo1313/DEP1/refs/heads/main/archive.py"

def generate():
    try:
        print("Sıralama ve Kitap çekiliyor...")
        # 1. Kaynakları internet üzerinden çek (en güncel hali için)
        kitap_content = requests.get(KITAP_URL).text
        siralama_content = requests.get(SIRALAMA_URL).text.splitlines()

        # 2. Kitaptan (archive.py) ID, İsim ve Logoları ayıkla
        # archive.py içindeki "ID": {"name": "...", "logo": "..."} yapısını yakalar
        channels = {}
        pattern = r'"(\d+)":\s*{\s*"name":\s*"([^"]*)",\s*"logo":\s*"([^"]*)"'
        matches = re.findall(pattern, kitap_content)
        
        for cid, cname, clogo in matches:
            # Eşleşmeyi kolaylaştırmak için kanal ismini küçük harfe çevirip kaydediyoruz
            channels[cname.strip().lower()] = {"id": cid, "name": cname, "logo": clogo}

        # 3. M3U Dosyasını Oluştur
        print(f"Sözlükte {len(channels)} kanal bulundu. canli_tv.m3u oluşturuluyor...")
        with open("canli_tv.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for line in siralama_content:
                target_name = line.strip()
                if not target_name: continue
                
                # Sıralamadaki ismi 'kitap' verisiyle karşılaştır
                key = target_name.lower()
                if key in channels:
                    cdata = channels[key]
                    # M3U Formatı: Logo, Grup ve Kanal İsmi
                    f.write(f'#EXTINF:-1 tvg-logo="{cdata["logo"]}" group-title="CANLI YAYIN",{cdata["name"]}\n')
                    # Link: Workers adresi + Kanal ID
                    f.write(f"{WORKER_URL}/{cdata['id']}\n")
                else:
                    print(f"Uyarı: '{target_name}' ismi archive.py içinde tam eşleşmedi.")

        print("İşlem Başarılı: canli_tv.m3u dosyası hazırlandı.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    generate()
