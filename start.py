from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os
from tools.logger import logger
import threading
import subprocess

SERVER_PORT = os.getenv("SERVER_PORT")

def start_google_doorbell_subscriber():
    logger.info(f'Starting Google Doorbell listener')
    google_doorbell_subscriber_command = [
        'python3',
        'google_doorbell_subscriber.py',
    ]
    subprocess.run(google_doorbell_subscriber_command, check=True)

def start_telegram_bot():
    logger.info(f'Starting telegram bot')
    telegram_command = [
        'python3',
        'telegram_bot.py',
    ]
    subprocess.run(telegram_command, check=True)

def start_fast_api():
    logger.info(f'Starting fastapi server')
    uvicorn_command = [
        'uvicorn',
        'api_server:app',
        '--port',
        SERVER_PORT,
        '--host',
        '0.0.0.0',
    ]
    subprocess.run(uvicorn_command, check=True)

google_nest_thread = threading.Thread(target=start_google_doorbell_subscriber)
telegram_bot_thread = threading.Thread(target=start_telegram_bot)
fast_api_thread = threading.Thread(target=start_fast_api)

google_nest_thread.start()
telegram_bot_thread.start()
fast_api_thread.start()

google_nest_thread.join()
telegram_bot_thread.join()
fast_api_thread.join()