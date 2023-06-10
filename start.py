from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os
from tools.logger import logger
import threading
import subprocess

SERVER_PORT = os.getenv("SERVER_PORT")

def start_telegram_bot():
    logger.info(f'Starting telegram bot')
    telegram_command = [
        'python3',
        'telegram_bot.py',
    ]
    subprocess.run(telegram_command, check=True)

def start_python_scheduler():
    logger.info(f'Starting scheduler')
    scheduler_command = [
        'python3',
        'scheduler.py',
    ]
    subprocess.run(scheduler_command, check=True)

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

telegram_bot_thread = threading.Thread(target=start_telegram_bot)
python_scheduler_thread = threading.Thread(target=start_python_scheduler)
fast_api_thread = threading.Thread(target=start_fast_api)

telegram_bot_thread.start()
python_scheduler_thread.start()
fast_api_thread.start()

telegram_bot_thread.join()
python_scheduler_thread.join()
fast_api_thread.join()