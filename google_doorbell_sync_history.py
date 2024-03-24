from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from server.camera_router import CameraEvent
from tools import actions
from tools.logger import logger

from io import BytesIO
import time
import asyncio
import os
import pytz
import datetime

from telegram import Bot, InputMediaVideo
from apscheduler.schedulers.asyncio import AsyncIOScheduler


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
assert CHANNEL_ID and TELEGRAM_BOT_TOKEN

REFRESH_EVERY_X_MINUTES=30


class TelegramEventsSync(object):
    
    TELEGRAM_TIME_FORMAT = '%H:%M:%S %d/%m/%Y'
    
    def __init__(self, telegram_bot_token, refresh_every_x_minutes) -> None:
        self._telegram_bot = Bot(token=telegram_bot_token)
        self._refresh_every_x_minutes = refresh_every_x_minutes
 
        self._recent_events = set()
        logger.info("Initialized a Telegram Bot")

    async def sync(self):
        # Initialize the bot
    
        all_recent_camera_events = actions.get_all_camera_events(
            end_time = pytz.timezone("Israel").localize(datetime.datetime.now()),
            # 2.5 hours, a bit less than the maxmimum time of what Google 
            # is saving the videos (3 hours is risky because they can cut 
            # your videos and change the start time == event_id)
            duration_minutes=150 
        )

        logger.info(f"Received {len(all_recent_camera_events)} camera events")

        for camera_event in all_recent_camera_events:
            camera_event_obj = CameraEvent(**camera_event)

            if camera_event_obj.event_id in self._recent_events:
                logger.info(f"CameraEvent ({camera_event}) already sent, skipping..")
                continue

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

            self._recent_events.add(camera_event_obj.event_id)
        
def main():

    tes = TelegramEventsSync(TELEGRAM_BOT_TOKEN, REFRESH_EVERY_X_MINUTES)

    # Schedule the job to run every x minutes
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        tes.sync, 
        'interval', 
        minutes=REFRESH_EVERY_X_MINUTES, 
        next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=2)
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

    
if __name__ == "__main__":
    main()