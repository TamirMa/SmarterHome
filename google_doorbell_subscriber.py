from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os
import asyncio
import errno
import pytz
import pickle
import requests
from telegram import Bot, InputMediaVideo
from io import BytesIO

from tools.logger import logger

import asyncio
from aiohttp import ClientSession
from google.auth.transport.requests import Request
from aiohttp.client_exceptions import ClientError
from google_nest_sdm.auth import AbstractAuth
from google_nest_sdm.camera_traits import CameraLiveStreamTrait
from google_nest_sdm.exceptions import AuthException
from google_nest_sdm.device import Device
from google_nest_sdm.event import EventMessage
from google_nest_sdm.google_nest import Auth, DeviceWatcherCallback
from google_nest_sdm.google_nest_subscriber import (
    API_URL,
    GoogleNestSubscriber,
)

TOKEN_CACHE = ".google_nest.token"

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
assert CHANNEL_ID and TELEGRAM_BOT_TOKEN
# Replace with your actual channel ID

TELEGRAM_TIME_FORMAT = '%H:%M:%S %d/%m/%Y'

class TelegramWatcherCallback(DeviceWatcherCallback):
    def __init__(self, telegram_bot: Bot, telegram_channel: str, auth: Auth ,device: Device, output_type: str) -> None:
        super().__init__(device, output_type)

        self._telegram_bot = telegram_bot
        self._telegram_channel = telegram_channel
        self._auth = auth
        self._clip_sent = set()
        self._chime_sent = set()
        self._motion_sent = set()
        self._person_sent = set()

    async def download_clip(self, event_clip_url):
        logger.debug(f"Download a video clip: {event_clip_url}")
        try:
            creds = await self._auth.async_get_creds()
        except ClientError as err:
            raise AuthException(f"Access token failure: {err}") from err
        
        logger.debug("Successfully created an access token, about to download the clip")
        response = requests.get(
            event_clip_url,
            headers = {
                "Authorization": f"Bearer {creds.token}"
                }
        )
        assert response.status_code == 200, response.status_code
        return response.content

    async def send_doorbell_chime_telegram_notification(self, event_time, doorbell_chime_event) -> None:
        text_message = "Someone is ringing!"
        await self._telegram_bot.send_message(
            chat_id=self._telegram_channel, 
            text=text_message + f" [{event_time.strftime(TELEGRAM_TIME_FORMAT)}]"
        )

        logger.info("Telegram text message sent successfully!")

    async def send_person_detected_telegram_notification(self, event_time, motion_chime_event) -> None:
        zones = motion_chime_event["zones"]
        if 'Door' in zones:
            text_message = "Someone is at the door"
        else:
            text_message = "Person detected in the hallway"
        
        await self._telegram_bot.send_message(
            chat_id=self._telegram_channel, 
            text=text_message + f" [{event_time.strftime(TELEGRAM_TIME_FORMAT)}]",
            disable_notification='Door' not in zones
        )

        logger.info("Telegram text message sent successfully!")
    
    async def send_motion_detected_telegram_notification(self, event_time, motion_chime_event) -> None:
        zones = motion_chime_event["zones"]
        
        text_message = f"{'*' if 'Door' in zones else ''} Motion detected"
        await self._telegram_bot.send_message(
            chat_id=self._telegram_channel, 
            text=text_message + f" [{event_time.strftime(TELEGRAM_TIME_FORMAT)}]",
            disable_notification='Door' not in zones
        )

        logger.info("Telegram text message sent successfully!")

    async def send_clip_preview_telegram_notification(self, event_time, clip_preview_event) -> None:

        clip_preview_url = clip_preview_event["previewUrl"]

        # Send video data
        video_data = await self.download_clip(clip_preview_url)
        video_io = BytesIO(video_data)
        logger.debug("Downloaded the video-clip, about to send it")

        video_caption = f"Doorbell clip"
        video_media = InputMediaVideo(
            media=video_io, 
            caption=video_caption + f" [{event_time.strftime(TELEGRAM_TIME_FORMAT)}]"
        )
        
        await self._telegram_bot.send_media_group(
            chat_id=self._telegram_channel, 
            media=[video_media]
        )

        logger.info("Telegram video-clip message sent successfully!")

    async def async_handle_event(self, event_message: EventMessage) -> None:
        logger.info(f"event_id: {event_message.event_id}")
        try:
            logger.info(f"raw_data={event_message.raw_data}")

            event_json = event_message.raw_data
            if "resourceUpdate" not in event_json:
                return

            event_time = event_json["timestamp"].astimezone(pytz.timezone("Israel"))
            event_state = event_json["event_thread_state"]

            if "sdm.devices.events.DoorbellChime.Chime" in event_json["resourceUpdate"]["events"] and event_message.event_id not in self._chime_sent:
                doorbell_chime_event = event_json["resourceUpdate"]["events"]["sdm.devices.events.DoorbellChime.Chime"]
                await self.send_doorbell_chime_telegram_notification(event_time, doorbell_chime_event)
                self._chime_sent.add(event_message.event_id)

            if ("sdm.devices.events.DoorbellChime.Person" in event_json["resourceUpdate"]["events"]) and event_message.event_id not in self._person_sent:
                person_chime_event = event_json["resourceUpdate"]["events"]["sdm.devices.events.DoorbellChime.Person"]
                await self.send_person_detected_telegram_notification(event_time, person_chime_event)
                self._person_sent.add(event_message.event_id)
 
            if ("sdm.devices.events.DoorbellChime.Motion" in event_json["resourceUpdate"]["events"]) and event_message.event_id not in self._motion_sent:
                motion_chime_event = event_json["resourceUpdate"]["events"]["sdm.devices.events.DoorbellChime.Motion"]
                await self.send_motion_detected_telegram_notification(event_time, motion_chime_event)
                self._motion_sent.add(event_message.event_id)
 
            if "sdm.devices.events.CameraClipPreview.ClipPreview" in event_json["resourceUpdate"]["events"] and event_message.event_id not in self._clip_sent:
                clip_preview_event = event_json["resourceUpdate"]["events"]["sdm.devices.events.CameraClipPreview.ClipPreview"]
                await self.send_clip_preview_telegram_notification(event_time, clip_preview_event)
                self._clip_sent.add(event_message.event_id)

        except Exception as e:
            logger.info(f"Error sending Telegram message: {e}")

        logger.info("Done handling the event")

def create_creds():

    token_cache = os.path.abspath(os.path.join(os.path.dirname(__file__), TOKEN_CACHE))
    logger.info(f"Reading token out of file: {token_cache}")
    with open(token_cache, "rb") as token:
        creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # Save the credentials for the next run
    if not os.path.exists(os.path.dirname(token_cache)):
        try:
            os.makedirs(os.path.dirname(token_cache))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(token_cache, "wb") as token:
        pickle.dump(creds, token)

    return creds


async def start_subscription_loop():

    user_creds = create_creds()
    
    logger.info("Loaded user credentials file")

    async with ClientSession() as client:
        auth = Auth(client, user_creds, API_URL)
    
        project_id = "32d0f7a4-62a1-4873-813f-9367169c9a72"
        subscription_id = "projects/doorbell-api-343817/subscriptions/doorbell_subscription"
        device_id = "enterprises/32d0f7a4-62a1-4873-813f-9367169c9a72/devices/AVPHwEtaettICkn7la9pLKhCGElLxBOTiaKB8FxGMA0en4G9lqkYGeQks1I4fD4cMFsmqSshLonProTvTS9UCcPVsFcblg"

        logger.info(f"Subscription: {subscription_id}")
        logger.info(f"Nest Project ID: {project_id}")

        subscriber = GoogleNestSubscriber(
            auth, project_id, subscription_id
        )

        device_manager = await subscriber.async_get_device_manager()
        dev = device_manager.devices[device_id]

        # Initialize the bot
        telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)
        logger.info("Initialized a Telegram Bot")

        dev_callback = TelegramWatcherCallback(
            telegram_bot=telegram_bot, 
            telegram_channel= CHANNEL_ID, 
            auth=auth, 
            device=dev, 
            output_type="json"
        )

        dev.add_event_callback(dev_callback.async_handle_event)
        logger.info("Added an event callback to the subscribtion watcher")
        
        await subscriber.start_async()
        try:
            while True:
                await asyncio.sleep(10)
        except KeyboardInterrupt:
            subscriber.stop_async()

if __name__ == "__main__":
    asyncio.run(start_subscription_loop())
