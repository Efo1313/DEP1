import re

def logolari_yerlestir(m3u_dosyasi):
    # Kanal ismi ve karşılık gelen logo linkleri
    kanal_logolari = {
        "BNT 1": "https://i.hizliresim.com/2ub474j.png",
        "BNT 2": "https://i.hizliresim.com/rk2853y.png",
        "BNT 3": "https://i.hizliresim.com/39lts6a.png",
        "BTV Story": "https://i.hizliresim.com/86a7ix8.png", # Uzun isimli olanı üste aldım (çakışma olmaması için)
        "BTV Sinema": "https://i.hizliresim.com/9b6i9by.png",
        "BTV Lady": "https://i.hizliresim.com/6312te1.png",
        "BTV Comedy": "https://i.hizliresim.com/streq9v.png",
        "BTV Action": "https://i.hizliresim.com/ge6news.png",
        "BTV": "https://i.hizliresim.com/otlg64v.png",
        "Nova News": "https://i.hizliresim.com/s1g6ly9.png",
        "Nova Sport": "https://i.hizliresim.com/jr6z84f.png",
        "Nova tv": "https://i.hizliresim.com/2bq59u9.png",
        "Kino Nova": "https://i.hizliresim.com/8z6j0zq.png",
        "Diema Family": "https://i.hizliresim.com/s6j1299.png",
        "Diema Sport 2": "https://i.hizliresim.com/ad8uhas.png",
        "Diema Sport 3": "https://i.hizliresim.com/6s0zh2x.png",
        "Diema Sport": "https://i.hizliresim.com/aeofcfr.png",
        "Diema": "https://i.hizliresim.com/tpuby2q.png",
        "HBO 2": "https://i.hizliresim.com/g4v1cop.png",
        "HBO 3": "https://i.hizliresim.com/d5qdqb3.png",
        "HBO": "https://i.hizliresim.com/ea7kaop.png",
        "AXN Black": "https://i.hizliresim.com/ovngoqt.png",
        "AXN White": "https://i.hizliresim.com/1jgzk8r.png",
        "AXN": "https://i.hizliresim.com/k5wyvth.png",
        "Bulgaria ON AIR": "https://i.hizliresim.com/66jre4l.png",
        "ALFA Ataka": "https://i.hizliresim.com/ka3h7hz.png",
        "Cartoon Network": "https://i.hizliresim.com/tsuodvd.png",
        "Animal Planet": "https://i.hizliresim.com/95spf00.png",
        "Discovery": "https://i.hizliresim.com/sif2sjf.png",
        "EKids": "https://i.hizliresim.com/pwo6mmu.png",
        "Eurosport 1": "https://i.hizliresim.com/hj1h57y.png",
        "Eurosport 2": "https://i.hizliresim.com/qx6mrva.png",
        "Evrokom": "https://i.hizliresim.com/ovtv2we.png",
        "STAR Chanel": "https://i.hizliresim.com/8t89vy4.png",
        "STAR Crime": "https://i.hizliresim.com/ci9hsbx.png",
        "STAR Life": "https://i.hizliresim.com/nk4g37t.png",
        "NatGeo Wild": "https://i.hizliresim.com/dvw80ug.png",
        "National Geographic": "https://i.hizliresim.com/417bgpy.png",
        "Love Nature": "https://i.hizliresim.com/7m3xtg9.png",
        "Ring": "https://i.hizliresim.com/palwmce.png",
        "Rus 1": "https://i.hizliresim.com/6xjbls3.png",
        "Skat TV": "https://i.hizliresim.com/bzp729r.png",
        "TLC": "https://i.hizliresim.com/jwzxbvd.png",
        "Euronews": "https://i.hizliresim.com/fco0mxc.png",
        "TV 1000": "https://i.hizliresim.com/j9obm2h.png",
        "Viasat History": "https://i.hizliresim.com/lb9mlqx.png",
        "Viasat Explore": "https://i.hizliresim.com/s2403gs.png",
        "Viasat Nature": "https://i.hizliresim.com/aolr613.png",
        "TVT": "https://i.hizliresim.com/6fxoukd.png",
        "Agro TV": "https://i.hizliresim.com/31ifmd8.png",
        "Nick Jr": "https://i.hizliresim.com/r7lznoh.png",
        "7/8 TV": "https://i.hizliresim.com/4w9htsr.png",
        "Nickelodeon": "https://i.hizliresim.com/9iw8age.png",
        "24 Kitchen": "https://i.hizliresim.com/34ti4tu.png",
        "MAX Sport 1": "https://i.hizliresim.com/6mz83ad.png",
        "MAX Sport 2": "https://i.hizliresim.com/18djvhy.png",
        "MAX Sport 3": "https://i.hizliresim.com/kayjpc2.png",
        "MAX Sport 4": "https://i.hizliresim.com/45c5pf1.png",
        "Disney Channel": "https://i.hizliresim.com/1uphxzl.png"
    }

    try:
        with open(m3u_dosyasi, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.startswith("#EXTINF"):
                # Kanal ismini satırın sonundan alıyoruz
                for kanal, logo_url in kanal_logolari.items():
                    # Büyük/küçük harf duyarlılığı olmadan kontrol et
                    if kanal.lower() in line.lower():
                        # Eğer zaten bir tvg-logo varsa değiştir, yoksa ekle
                        if 'tvg-logo="' in line:
                            line = re.sub(r'tvg-logo=".*?"', f'tvg-logo="{logo_url}"', line)
                        else:
                            line = line.replace('#EXTINF:-1', f'#EXTINF:-1 tvg-logo="{logo_url}"')
                        break # Logoyu bulduk, diğerlerini kontrol etmeye gerek yok
            new_lines.append(line)

        with open(m3u_dosyasi, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"İşlem tamam! {m3u_dosyasi} içindeki logolar güncellendi.")

    except FileNotFoundError:
        print("Dosya bulunamadı. Lütfen 'seyir_sandigi.m3u' dosyasının script ile aynı klasörde olduğundan emin ol.")

# Çalıştır
logolari_yerlestir("seyir_sandigi.m3u")
