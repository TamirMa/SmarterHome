import pytz
import datetime

from tools.logger import logger
import xml.etree.ElementTree as ET

from devices.generic import GenericDevice, DoorbellInterface
from tools.logger import logger


class NestDoorbellDevice(GenericDevice, DoorbellInterface):

    NEST_API_DOMAIN = "https://nest-camera-frontend.googleapis.com"

    EVENTS_URI = NEST_API_DOMAIN + "/dashmanifest/namespace/nest-phoenix-prod/device/{device_id}"
    DOWNLOAD_VIDEO_URI = NEST_API_DOMAIN + "/mp4clip/namespace/nest-phoenix-prod/device/{device_id}"

    
    def parse_events(self, events_xml):
        root = ET.fromstring(events_xml)
        periods = root.findall(".//{urn:mpeg:dash:schema:mpd:2011}Period")
        return [
            period.attrib for period in periods
        ]

    def get_events(self, start_time: datetime.datetime, end_time: datetime.datetime):
        params = {
            "start_time" : start_time.astimezone(pytz.timezone("UTC")).isoformat()[:-9]+"Z", # 2024-02-07T19:32:25.250Z
            "end_time" : end_time.astimezone(pytz.timezone("UTC")).isoformat()[:-9]+"Z", # 2024-02-08T19:32:25.250Z
            "types": 4, 
            "variant" : 2,
        }
        return self.parse_events(
            self._connection.make_get_request(NestDoorbellDevice.EVENTS_URI, params=params)
        )
        
    def download_specific_media(self, media_id, nc_media):
        # https://nest-camera-frontend.googleapis.com/download/med
        # ia/e5dbf51f-1717-43b5-9942-8f1fff394710/1/0.m4a?nc_media
        # =AVDml48BdFZz90QIk-5VUx3A3dvgwyfNiuguDbWopAvVE0RAerlgRux
        # E4t7FPDtpclgGNbyqGsWqSUJhYbKoMcVjU8IUmORRyaJuFjJEYL8o4V4
        # O_T0uSEOxXSUKvEnVPUsE9NkE2xF-5Ao7FiFdp8x1CidVS_BUKI0dOTZ
        # xMqjrhqI9YfkJ30aMXoh_rdz3grBmrlJ38IrEAbOe8o4vgAYO50WmVFX
        # qdQPENzzNR7MduyPG1dHT1pOk9TPnVvvz3Wryeeelx-EeYQEJn5vzQRO
        # cIGwDcaOnND_-akRStGtTYTLMwKpp-e1TQ0pQXOMTsttimrhC8U7hS8u
        # pv9W07hQwVXJiSehAINtPiTha0zO6iqWN_WWRfCOBfYad0FfTndRXkd5
        # KKo50IYj4XmJjMVHtgu8W_6ZSQhAn-oslWqIi5jUp3QNKlW0OYdDWsuA
        # XDjFE3EHt5lHi36StgnIe2_W9cFDS5-FSPRrXTtBHFDwHeEOBeE0DDVM
        # MK51ObA%3D%3D
        raise NotImplemented() 

    def download_video_by_times(self, start_time, end_time):
        params = {
            "start_time" : int(start_time.timestamp()*1000), # 1707368737876
            "end_time" : int(end_time.timestamp()*1000), # 1707368757371
        }
        return self._connection.make_get_request(NestDoorbellDevice.DOWNLOAD_VIDEO_URI, params=params)
