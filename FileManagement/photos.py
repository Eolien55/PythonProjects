import shutil
import os
import sys
import time
import PIL.Image
import PIL.ExifTags
import requests
import json
import re


def get_exif(filename):
    img = PIL.Image.open(filename)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    return exif


def lonlat(gps):
    results = []
    for i in ["GPSLongitude", "GPSLatitude"]:
        ref = gps[i+"Ref"]
        val = gps[i]
        val = (val[0]+(val[1]/60)+(val[2]/3600)) * \
            [-1, 1][int(ref in ["N", "E"])]
        val = eval(str(val))
        results.append(val)
    return results


months = {
    "01": "Janvier",
    "02": "F\u00e9vrier",
    "03": "Mars",
    "04": "Avril",
    "05": "Mai",
    "06": "Juin",
    "07": "Juillet",
    "08": "Ao\u00fbt",
    "09": "Septembre",
    "10": "Octobre",
    "11": "Novembre",
    "12": "D\u00e9cembre"
}

url = "https://maps.googleapis.com/maps/api/geocode/json"

for folder, _, files in os.walk("."):
    folder = os.path.abspath(folder)
    for file in files:
        format = re.findall(r"\.[A-Za-z0-9_]+$", file)[0]
        file = folder+"/"+file
        exif = get_exif(file)
        DateTime = exif["DateTime"]
        year = DateTime[:4]
        month = months[DateTime[5:7]]
        if "GPSInfo" in exif:
            gps = {PIL.ExifTags.GPSTAGS.get(
                i): exif['GPSInfo'][i] for i in exif['GPSInfo']}
            lon, lat = lonlat(gps)
            params = {"lon": str(lon), "lat": str(
                lat), "zoom": 10, "format": "json", "accept-language": "fr"}
            adress = requests.get(
                "https://nominatim.openstreetmap.org/reverse", params=params).text
            adress = json.loads(adress).get("display_name")
            if adress:
                adress = adress.split(", ")
                city = adress[0]
                country = adress[-1]
            else:
                city = None
                country = None
        else:
            city = None
            country = None
        if city and country:
            if not os.path.exists(os.path.abspath(".") +
                                  f"/{country}/{city}/{year}/{month}"):
                os.makedirs(os.path.abspath(".") +
                            f"/{country}/{city}/{year}/{month}")
            name = str(len(os.listdir(os.path.abspath(".") +
                                      f"/{country}/{city}/{year}/{month}"))+1)+format
            newfile = os.path.abspath(
                ".")+f"/{country}/{city}/{year}/{month}/{name}"
        else:
            if not os.path.exists(os.path.abspath(".") +
                                  f"/{year}/{month}"):
                os.makedirs(os.path.abspath(".") +
                            f"/{year}/{month}")
            name = str(len(os.listdir(os.path.abspath(".") +
                                      f"/{year}/{month}"))+1)+format
            newfile = os.path.abspath(".")+f"/{year}/{month}/{name}"
        shutil.move(file, newfile)
"""{'GPSLatitudeRef': 'N',
 'GPSLatitude': (48.0, 53.0, 26.91),
 'GPSLongitudeRef': 'E',
 'GPSLongitude': (2.0, 8.0, 20.77),
 'GPSAltitudeRef': b'\x00',
 'GPSAltitude': 31.340000152617,
 'GPSTimeStamp': (18.0, 2.0, 53.42),
 'GPSSpeedRef': 'K',
 'GPSSpeed': 0.0,
 'GPSImgDirectionRef': 'T',
 'GPSImgDirection': 83.45333869670152,
 'GPSDestBearingRef': 'T',
 'GPSDestBearing': 83.45333869670152,
 'GPSDateStamp': '2021:04:09',
 'GPSHPositioningError': 65.0}"""
