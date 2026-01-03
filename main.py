# -*- coding: utf-8 -*-
import os
import datetime

# Kanal listesi
channels = [
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
    "A Spor|UCJElRTCNEmLemgirqvsW63Q",
    "Now Spor|UCHowoDxzhyCPQBzhOpeP4-w",
    "Ekol Spor|UCjr2WQ5a20B5YyUY7qaa2sw",
    "Bein Spor Haber|UCPe9vNjHF1kEExT5kHwc7aw",
    "TJK TV|UC_8NgeVv0Ccl96U6C7E_fSg",
    "CNBC-e|UCaO-M1dXacMwtyg0Pvovk4w",
    "Bloomberg HT|UCApLxl6oYQafxvykuoC2uxQ",
    "Kemal Sunal TV|UCHumSHRFQ8skiHTY75sxytQ",
    "Yesilcam TV|UCUALYmnkEmx8vlxIbpr2gmw",
    "Korku Filmleri TV|UCsbpTjR1Vh0L3gvBg9d0Dbg"
]

print(f"Guncelleme Saati: {datetime.datetime.now()}")

# Gercekci bir User-Agent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    
    for channel in channels:
        name, channel_id = channel.split("|")
        live_url = f"https://www.youtube.com/channel/{channel_id}/live"
        
        # yt-dlp komutunu daha agresif ve net hale getirdik
        # -f 95/94/best: Belirli kalite formatlarini zorlar
        cmd = f"yt-dlp --geo-bypass --user-agent '{UA}' -f 95/94/best -g {live_url}"
        m3u8_link = os.popen(cmd).read().strip()
        
        if m3u8_link and "m3u8" in m3u8_link:
            f.write(f"#EXTINF:-1,{name}\n{m3u8_link}\n")
            print(f"OK: {name}")
        else:
            # Yedek link
            f.write(f"#EXTINF:-1,{name} (Direkt Link)\n{live_url}\n")
            print(f"FAILED: {name} (Yedek link eklendi)")

print("Yayinlarim.m3u listesi tamamlandi.")
