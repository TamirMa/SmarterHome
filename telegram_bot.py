from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import re
import os
import datetime
from server.control_router import DeviceType, LightState
from scheduler import tools
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters, CallbackContext, Application


TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_USER_IDs = [
    int(allowed_user_id) 
    for allowed_user_id in os.environ["TELEGRAM_ALLOWED_LIST"].split(",")
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def go_away(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ALLOWED_USER_IDs:
        await update.message.reply_text("Go Away")
        raise Exception(f"Stranger. Stop. {update.message.from_user.id}")

async def hello(update: Update, context: CallbackContext):
    await go_away(update, context)
    
    await update.message.reply_text(f'Hello, {update.message.from_user.first_name}!')

async def handle_device_init(update: Update, context: CallbackContext):
    await go_away(update, context)

    device_type = update.message.text[1:]
    logger.info(f'{device_type} command received')

    # Create buttons to slect language:
    devices = tools.get_all_devices(device_type)

    # Create initial message:
    message = "Please choose a light from the list:"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(" ".join(re.findall(r'[A-Z][a-z]*', device)), callback_data=device)
            ]
            for device in devices
        ]
    )

    context.user_data['waiting_for_device'] = device_type
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def handle_device_command(update: Update, context: CallbackContext):
    
    query = update.callback_query
    option = query.data

    await query.message.edit_reply_markup(reply_markup=None)  # Remove the inline keyboard

    if context.user_data.get('waiting_for_command'):
        device_type = context.user_data.get('waiting_for_command')
        device = context.user_data['device_in_context']
        if device_type == DeviceType.Lights:
            tools.change_light_state(device, option)
            await query.edit_message_text(text=f'Turned light {device} {option}')
            
        elif device_type == DeviceType.Sockets:
            tools.change_socket_state(device, option)
            await query.edit_message_text(text=f'Turned socket {device} {option}')
            
        del context.user_data['device_in_context']
        del context.user_data['waiting_for_command']

    elif context.user_data.get('waiting_for_device'):
        device_type = context.user_data.get('waiting_for_device')
        devices = tools.get_all_devices(device_type)
        if option in devices:
            keyboard = [
                [
                    InlineKeyboardButton("On", callback_data="on"),
                    InlineKeyboardButton("Off", callback_data="off")
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.user_data['device_in_context'] = option
            context.user_data['waiting_for_command'] = device_type
            del context.user_data['waiting_for_device']
            await query.edit_message_text(text="What would like to to do?", reply_markup=reply_markup)
        else:
            del context.user_data['waiting_for_device']
            await query.edit_message_text(f'Cannot find device')

async def process_message(update: Update, context: CallbackContext):
    await go_away(update, context)

    if context.user_data.get('device_in_context'):
        del context.user_data['device_in_context']
    if context.user_data.get('waiting_for_command'):
        del context.user_data['waiting_for_command']
    if context.user_data.get('waiting_for_device'):
        del context.user_data['waiting_for_device']
    await update.message.reply_text(f'what?')

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('hello', hello))
    application.add_handler(CommandHandler(DeviceType.Lights, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Sockets, handle_device_init))
    application.add_handler(CallbackQueryHandler(handle_device_command))
    application.add_handler(MessageHandler(filters.TEXT, process_message))

    application.run_polling()

if __name__ == '__main__':
    main()