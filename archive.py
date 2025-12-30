import requests
import re

ARCHIVE_URL = "http://85.11.144.8/archive/"

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        links = re.findall(r'href="([^?].*?)"', response.text)
        return [l for l in links if l != '../']
    except:
        return []

with open("seyir_sandigi.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    channels = get_links(ARCHIVE_URL)
    for channel in channels:
        channel_name = channel.replace("/", "")
        channel_url = ARCHIVE_URL + channel
        files = get_links(channel_url)
        # Son 5 kaydı listeye ekler
        for video_file in files[-5:]:
            video_url = channel_url + video_file
            f.write(f"#EXTINF:-1,{channel_name} - {video_file}\n{video_url}\n")
