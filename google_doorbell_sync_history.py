from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from server.camera_router import CameraEvent
from tools import actions
from tools.logger import logger

from io import BytesIO
import asyncio
import os
import pytz
import datetime

from telegram import Bot, InputMediaVideo


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
assert CHANNEL_ID and TELEGRAM_BOT_TOKEN

REFRESH_EVERY_X_MINUTES=60

class TelegramEventsSync(object):
    
    TELEGRAM_TIME_FORMAT = '%H:%M:%S %d/%m/%Y'
    
    def __init__(self, telegram_bot_token, refresh_every_x_minutes) -> None:
        self._telegram_bot = Bot(token=telegram_bot_token)
        self._refresh_every_x_minutes = refresh_every_x_minutes
        logger.info("Initialized a Telegram Bot")

    async def sync(self):
        # Initialize the bot
    
        all_recent_camera_events = actions.get_all_camera_events(
            end_time = pytz.timezone("Israel").localize(datetime.datetime.now()),
            duration_minutes=self._refresh_every_x_minutes + 10 # The extra 10 minutes are used for not missing an overlapping event
        )

        logger.info(f"Received {len(all_recent_camera_events)} camera events")

        for camera_event in all_recent_camera_events[::-1]:
            camera_event_obj = CameraEvent(**camera_event)
            logger.info(f"Downloading camera event: {camera_event}")
            video_data = actions.download_camera_event(camera_event)
            video_io = BytesIO(video_data)

            video_caption = f"{camera_event_obj.device_id} clip"
            event_local_time = camera_event_obj.start_time.astimezone(pytz.timezone('Israel'))
            video_media = InputMediaVideo(
                media=video_io, 
                caption=video_caption + f" [{event_local_time.strftime(self.TELEGRAM_TIME_FORMAT)}]"
            )
            
            await self._telegram_bot.send_media_group(
                chat_id=CHANNEL_ID, 
                media=[video_media],
                disable_notification=True,
            )
            logger.debug("Sent clip successfully")
        
async def main():

    tes = TelegramEventsSync(TELEGRAM_BOT_TOKEN, REFRESH_EVERY_X_MINUTES)
    await tes.sync()
    # Schedule the job to run every 5 minutes
    # scheduler.add_job(tes.sync, 'interval', minutes=REFRESH_EVERY_X_MINUTES, next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10))
    
if __name__ == "__main__":
    asyncio.run(main())