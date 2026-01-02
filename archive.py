                for video_file in video_files:
                    video_url = channel_url + video_file
                    
                    # Dosya adından tarih ve saati ayıklayan sihirli satırlar:
                    # Örnek dosya: ch-2-20260101-14.mpg
                    match = re.search(r'(\d{4})(\d{2})(\d{2})-(\d{2})', video_file)
                    
                    if match:
                        yil, ay, gun, saat = match.groups()
                        video_tarihi = f"{gun}.{ay}" # Artık bu her dosya için özel (01.01, 02.01 vb.)
                        time_label = saat
                    else:
                        # Eğer format uymazsa eski yöntemi kullan
                        raw_time = video_file.split('-')[-1].replace('.mpg', '')
                        time_label = "".join(filter(str.isdigit, raw_time))
                        video_tarihi = datetime.now().strftime("%d.%m") # Mecbur kalınca bugünü yaz
                    
                    if not time_label: continue
                    
                    logo_url = LOGO_BASE + data["logo"] if data["logo"] else ""
                    
                    # BURASI ÖNEMLİ: video_tarihi artık her satırda değişecek
                    display_name = f"{data['name']} ({time_label}:00 - {video_tarihi})"
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{data["name"]}",{display_name}\n')
                    f.write(f"{video_url}\n")
