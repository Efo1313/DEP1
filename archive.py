# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime

# AYARLAR
ARCHIVE_URL = "http://85.11.144.8/archive/"
LOGO_BASE = "https://www.seirsanduk.net/images/tvlogo/"

# TAM KANAL LİSTESİ (63 KANAL)
CHANNEL_DATA = {
    "2": {"name": "bTV", "logo": "btv.png"},
    "3": {"name": "Nova", "logo": "nova.png"},
    "4": {"name": "bTV Cinema", "logo": "btv-cinema.png"},
    "5": {"name": "Diema", "logo": "diema.png"},
    "6": {"name": "bTV Comedy", "logo": "btv-comedy.png"},
    "7": {"name": "HBO 3", "logo": "hbo-3.png"},
    "8": {"name": "AXN", "logo": "axn.png"},
    "9": {"name": "Kino Nova", "logo": "kino-nova.png"},
    "10": {"name": "Nova Sport", "logo": "nova-sport.png"},
    "11": {"name": "bTV Action", "logo": "btv-action.png"},
    "12": {"name": "Diema Family", "logo": "diema-family.png"},
    "13": {"name": "bTV Story", "logo": "btv-story.png"},
    "14": {"name": "AXN Black", "logo": "axn-black.png"},
    "15": {"name": "AXN White", "logo": "axn-white.png"},
    "16": {"name": "BNT 2", "logo": "bnt-2.png"},
    "17": {"name": "BNT 4", "logo": "bnt-4.png"},
    "18": {"name": "Bulgaria ON AIR", "logo": "bulgaria-on-air.png"},
    "20": {"name": "ALFA Ataka", "logo": "alfa.png"},
    "21": {"name": "Animal Planet", "logo": "animal-planet.png"},
    "28": {"name": "28 TV", "logo": ""},
    "29": {"name": "Cartoonito", "logo": "cartoonito.png"},
    "34": {"name": "Cartoon Network", "logo": "cartoon-network.png"},
    "38": {"name": "Discovery", "logo": "discovery.png"},
    "43": {"name": "Nova News", "logo": "nova-news.png"},
    "46": {"name": "EKids", "logo": "ekids.png"},
    "47": {"name": "Eurosport 1", "logo": "eurosport-1.png"},
    "48": {"name": "Eurosport 2", "logo": "eurosport-2.png"},
    "49": {"name": "Evrokom", "logo": "evrokom.png"},
    "54": {"name": "BNT 3", "logo": "bnt-3.png"},
    "56": {"name": "STAR Channel", "logo": "star-channel.png"},
    "57": {"name": "STAR Crime", "logo": "star-crime.png"},
    "58": {"name": "STAR Life", "logo": "star-life.png"},
    "59": {"name": "HBO", "logo": "hbo.png"},
    "65": {"name": "NatGeo Wild", "logo": "nat-geo-wild.png"},
    "66": {"name": "National Geographic", "logo": "nat-geo.png"},
    "76": {"name": "Ring", "logo": "ring.png"},
    "79": {"name": "PULS TV", "logo": ""},
    "80": {"name": "Skat TV", "logo": "skat.png"},
    "86": {"name": "TLC", "logo": "tlc.png"},
    "87": {"name": "Euronews", "logo": "euronews.png"},
    "89": {"name": "TV 1000", "logo": "tv-1000.png"},
    "92": {"name": "TVT", "logo": "tvt.png"},
    "94": {"name": "Viasat Explore", "logo": "viasat-explore.png"},
    "95": {"name": "Viasat History", "logo": "viasat-history.png"},
    "96": {"name": "Viasat Nature", "logo": "viasat-nature.png"},
    "108": {"name": "108 TV", "logo": ""},
    "114": {"name": "Agro TV", "logo": "agro-tv.png"},
    "137": {"name": "HBO 2", "logo": "hbo-2.png"},
    "182": {"name": "182 TV", "logo": ""},
    "192": {"name": "Nick Jr", "logo": "nick-jr.png"},
    "197": {"name": "7/8 TV", "logo": "7-8-tv.png"},
    "209": {"name": "Nickelodeon", "logo": "nickelodeon.png"},
    "485": {"name": "Di
