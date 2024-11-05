import datetime
import requests

# Locations: https://raw.githubusercontent.com/hebcal/dotcom/v1.1/hebcal.com/dist/cities2.txt
LOCATION = 293397


def get_shabat_times_online(location):
    # res = requests.get(f"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy=2023&gm=5&gd=21") # Example for 2 shabat-s in a row
    res = requests.get(f"https://www.hebcal.com/shabbat?cfg=json&geonameid={location}&M=on")
    return res.json()
    '''
    {
        "title": "Hebcal Tel Aviv June 2023",
        "date": "2023-06-05T13:30:26.544Z",
        "location":
        {
            "title": "Tel Aviv, Israel",
            "city": "Tel Aviv",
            "tzid": "Asia/Jerusalem",
            "latitude": 32.08088,
            "longitude": 34.78057,
            "cc": "IL",
            "country": "Israel",
            "admin1": "Tel Aviv",
            "asciiname": "Tel Aviv",
            "geo": "geoname",
            "geonameid": 293397
        },
        "range":
        {
            "start": "2023-06-09",
            "end": "2023-06-10"
        },
        "items":
        [
            {
                "title": "Candle lighting: 19:28",
                "date": "2023-06-09T19:28:00+03:00",
                "category": "candles",
                "title_orig": "Candle lighting",
                "hebrew": "הדלקת נרות",
                "memo": "Parashat Sh'lach"
            },
            {
                "title": "Parashat Sh'lach",
                "date": "2023-06-10",
                "hdate": "21 Sivan 5783",
                "category": "parashat",
                "hebrew": "פרשת שלח־לך",
                "leyning":
                {
                    "1": "Numbers 13:1-13:20",
                    "2": "Numbers 13:21-14:7",
                    "3": "Numbers 14:8-14:25",
                    "4": "Numbers 14:26-15:7",
                    "5": "Numbers 15:8-15:16",
                    "6": "Numbers 15:17-15:26",
                    "7": "Numbers 15:27-15:41",
                    "torah": "Numbers 13:1-15:41",
                    "haftarah": "Joshua 2:1-24",
                    "maftir": "Numbers 15:37-15:41"
                },
                "link": "https://hebcal.com/s/shlach-20230610?i=on&us=js&um=api"
            },
            {
                "title": "Havdalah: 20:29",
                "date": "2023-06-10T20:29:00+03:00",
                "category": "havdalah",
                "title_orig": "Havdalah",
                "hebrew": "הבדלה"
            }
        ]
    }
    '''

def get_shabat_times():
    def parse_date(date_str):
        return datetime.datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
    
    res = get_shabat_times_online(location=LOCATION)
    
    times = []
    for item in res["items"]:
        if item["category"] == "candles":
            datetime_obj = parse_date(item["date"])
            if len(times) > 0 and times[-1]["end"] is None:
                if datetime_obj < datetime.datetime.now():
                    del times[-1]
                else:
                    times[-1]["end"] = datetime_obj
            elif len(times) > 0:
                break
            times.append({
                "start": datetime_obj,
                "end": None,
            })
        if item["category"] == "havdalah":
            datetime_obj = parse_date(item["date"])
            if datetime_obj < datetime.datetime.now():
                del times[-1]
            else:
                times[-1]["end"] = datetime_obj
    # Filter the time-sections that are in the past
    return times



if __name__ == "__main__":
    print (get_shabat_times())