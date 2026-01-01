import os

# Daha önce 3 taneydi, şimdi paylaştığın listedeki tüm kanalları ekliyoruz
channels = [
    # --- HABER KANALLARI ---
    "CNN Turk|UCV6zcRug6Hqp1UX_FdyUeBg",
    "Haber Turk|UCn6dNfiRE_Xunu7iMyvD7AA",
    "NTV|UC9TDTjbOjFB9jADmPhSAPsw",
    "Haber Global|UCtc-a9ZUIg0_5HpsPxEO7Qg",
    "TRT Haber|UCBgTP2LOFVPmq15W-RH-WXA",
    "Ekol Tv|UCccxXUKSuqOrlWQxweZBAQw",
    "TV 100|UCndsdUW_oPLqpQJY9J8oIRg",
    "Halk Tv|UCf_ResXZzE-o18zACUEmyvQ",
    "Sozcu Tv|UCOulx_rep5O4i9y6AyDqVvw",
    "Tele 1|UCoHnRpOS5rL62jTmSDO5Npw",
    "24 TV|UCpS9it_v8Vrs2p_A_m4N6rA",
    "Ulusal Kanal|UCv6mR67Tog_T9E9p0L6XgLg",
    
    # --- SPOR KANALLARI ---
    "A Spor|UCJElRTCNEmLemgirqvsW63Q",
    "Now Spor|UCHowoDxzhyCPQBzhOpeP4-w",
    "Ekol Spor|UCjr2WQ5a20B5YyUY7qaa2sw",
    "Bein Spor Haber|UCPe9vNjHF1kEExT5kHwc7aw",
    "TJK TV|UC_8NgeVv0Ccl96U6C7E_fSg",
    
    # --- EKONOMİ & SİNEMA ---
    "CNBC-e|UCaO-M1dXacMwtyg0Pvovk4w",
    "Bloomberg HT|UCApLxl6oYQafxvykuoC2uxQ",
    "Kemal Sunal TV|UCHumSHRFQ8skiHTY75sxytQ",
    "Yesilcam TV|UCUALYmnkEmx8vlxIbpr2gmw",
    "Korku Filmleri TV|UCsbpTjR1Vh0L3gvBg9d0Dbg"
]

# IPTV Listesini oluşturmaya başlıyoruz
with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    for channel in channels:
        name, channel_id = channel.split("|")
        print(f"{name} için link alınıyor...")
        
        # YouTube canlı yayın adresini oluştur
        url = f"https://www.youtube.com/channel/{channel_id}/live"
        
        # Daha önce yaptığımız gibi yt-dlp ile ham linki çekiyoruz
        m3u8_url = os.popen(f"yt-dlp -g {url}").read().strip()
        
        if m3u8_url:
            # M3U formatına uygun şekilde yazıyoruz
            f.write(f"#EXTINF:-1,{name}\n{m3u8_url}\n")

print("İşlem tamam! Yeni listen hazır.")
