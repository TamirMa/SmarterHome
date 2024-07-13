from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import re
import os
from server.control_router import CurtainState, FanState, LightState, SocketState, TVCommands
from devices.manager import DeviceType
from tools import actions
from tools.logger import logger
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters, CallbackContext, Application


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDs = [
    int(allowed_user_id) 
    for allowed_user_id in os.getenv("TELEGRAM_ALLOWED_LIST", "0").split(",")
]

async def go_away(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ALLOWED_USER_IDs:
        await update.message.reply_text("Go Away")
        raise Exception(f"Stranger. Stop. {update.message.from_user.id}")

async def hello(update: Update, context: CallbackContext):
    await go_away(update, context)
    
    await update.message.reply_text(f'Hello, {update.message.from_user.first_name}!')


async def handle_device_tags_init(update: Update, context: CallbackContext):
    await go_away(update, context)

    device_type = update.message.text[1:]
    logger.info(f'{device_type} command received')

    # Create buttons to slect language:
    tags = actions.get_all_tags()
    
    # Create initial message:
    message = f"Please choose a {device_type} from the list:"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(tag, callback_data=tag)
            ]
            for tag in sorted(tags)
        ] + 
        [
            [
                InlineKeyboardButton("Ignore", callback_data="ignore")
            ]
        ]
    )

    context.user_data['waiting_for_device'] = "tags"
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def handle_device_init(update: Update, context: CallbackContext):
    await go_away(update, context)

    device_type = update.message.text[1:]
    logger.info(f'{device_type} command received')

    # Create buttons to slect language:
    devices = actions.get_all_devices(device_type)

    # Create initial message:
    message = f"Please choose a {device_type} from the list:"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(" ".join(re.findall(r'[A-Z]+[a-z]*', device)), callback_data=device)
            ]
            for device in sorted(devices)
        ] + 
        [
            [
                InlineKeyboardButton("Ignore", callback_data="ignore")
            ]
        ]
    )

    context.user_data['waiting_for_device'] = device_type
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def handle_device_command(update: Update, context: CallbackContext):
    
    query = update.callback_query
    option = query.data

    await query.message.edit_reply_markup(reply_markup=None)  # Remove the inline keyboard

    if option == "ignore":
        await query.edit_message_text(text=f'Ignored')
    elif context.user_data.get('waiting_for_device') == 'tags':
        tags = actions.get_all_tags()
        tag = option

        if tag not in tags:
            await query.edit_message_text(text=f'Couldn\'t find tag')
        else:
            actions.apply_tag_state(tag)
            await query.edit_message_text(text=f'Turned "{tag}" devices off')

    elif context.user_data.get('waiting_for_device') == 'shabat':
        del context.user_data['waiting_for_device']
        
        tasks = context.user_data['shabat']
        del context.user_data['shabat']
        
        if option == "ok":
            actions.set_tasks(tasks)

            acked_tasks = actions.get_tasks()
            message = "Done. This is the list of tasks for shabat:\n"
            message += '\n'.join([task["description"] for task in acked_tasks])

            await query.edit_message_text(text=message)
        else:
            await query.edit_message_text(text=f'Cancelled')
    
    elif context.user_data.get('waiting_for_device') == 'tasks':
        del context.user_data['waiting_for_device']
        
        if option == "clear":
            actions.clear_tasks()
            message = "Done."
            await query.edit_message_text(text=message)
        else:
            await query.edit_message_text(text=f'Bye')

    elif context.user_data.get('waiting_for_device'):
        device_type = context.user_data.get('waiting_for_device')
        del context.user_data['waiting_for_device']
        devices = actions.get_all_devices(device_type)
        if option in devices:
            if device_type == DeviceType.Lights:
                keyboard = [
                    [
                        InlineKeyboardButton("On", callback_data=LightState.ON),
                        InlineKeyboardButton("Off", callback_data=LightState.OFF),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Sockets:
                keyboard = [
                    [
                        InlineKeyboardButton("On", callback_data=SocketState.ON),
                        InlineKeyboardButton("Off", callback_data=SocketState.OFF),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Ovens:
                keyboard = [
                    [
                        InlineKeyboardButton("Start (Turbo 180°)", callback_data="start_1"),
                        InlineKeyboardButton("Stop", callback_data="stop"),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Heaters:
                keyboard = [
                    [
                        InlineKeyboardButton("On[120])", callback_data="on_120"),
                        InlineKeyboardButton("On[30]", callback_data="on_30"),
                        InlineKeyboardButton("Off", callback_data="off"),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.ACs:
                keyboard = [
                    [
                        InlineKeyboardButton("Turn On", callback_data="on"),
                        InlineKeyboardButton("Stop", callback_data="stop"),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Dishwashers:
                keyboard = [
                    [
                        InlineKeyboardButton("Start", callback_data="start"),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Fans:
                keyboard = [
                    [
                        InlineKeyboardButton("Fan3", callback_data=FanState.FAN3),
                        InlineKeyboardButton("Fan2", callback_data=FanState.FAN2),
                        InlineKeyboardButton("Stop", callback_data=FanState.STOP),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            elif device_type == DeviceType.Curtains:
                keyboard = [
                    [
                        InlineKeyboardButton("Open", callback_data=CurtainState.OPEN),
                        InlineKeyboardButton("Stop", callback_data=CurtainState.STOP),
                        InlineKeyboardButton("Close", callback_data=CurtainState.CLOSE),
                        InlineKeyboardButton("Cancel", callback_data="cancel")
                    ],
                ]
            else:
                raise Exception(f"Unsupported device type {device_type}")
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.user_data['device_in_context'] = option
            context.user_data['waiting_for_command'] = device_type
            await query.edit_message_text(text="What would like to to do?", reply_markup=reply_markup)
        else:
            await query.edit_message_text(f'Cannot find device')
    elif context.user_data.get('waiting_for_command'):
        device_type = context.user_data.get('waiting_for_command')
        device = context.user_data['device_in_context']
        
        del context.user_data['device_in_context']
        del context.user_data['waiting_for_command']
        
        if option == "cancel":
            await query.edit_message_text(text=f'Cancelled')

        elif device_type == DeviceType.Lights:
            actions.change_light_state(device, option)
            await query.edit_message_text(text=f'Turned light {device} {option}')
            
        elif device_type == DeviceType.Sockets:
            actions.change_socket_state(device, option)
            await query.edit_message_text(text=f'Turned socket {device} {option}')

        elif device_type == DeviceType.Curtains:
            actions.change_curtain_state(device, option)
            await query.edit_message_text(text=f'Curtain {device} - {option}')
        
        elif device_type == DeviceType.Fans:
            actions.change_fan_state(device, option)
            await query.edit_message_text(text=f'Fan {device} - {option}')

        elif device_type == DeviceType.Ovens:
            if option == "start_1":
                actions.turn_on_oven(device_id=device)
            elif option == "stop":
                actions.turn_off_oven(device_id=device)
            else:
                raise Exception(f"Unknown command for oven - {option}")
            await query.edit_message_text(text=f'Turned oven {device} {option}')
        
        elif device_type == DeviceType.Heaters:
            if option == "on_120":
                actions.turn_on_heater(device_id=device, timer=120)
            elif option == "on_30":
                actions.turn_on_heater(device_id=device, timer=30)
            elif option == "off":
                actions.turn_off_heater(device_id=device)
            else:
                raise Exception(f"Unknown command for heater - {option}")
            await query.edit_message_text(text=f'Turned heater {device} {option}')
        
        elif device_type == DeviceType.ACs:
            if option == "on":
                actions.turn_on_ac(device_id=device)
            elif option == "stop":
                actions.turn_off_ac(device_id=device)
            else:
                raise Exception(f"Unknown command for AC - {option}")
            await query.edit_message_text(text=f'AC {device}: {option}')

        elif device_type == DeviceType.Dishwashers:
            if option == "start":
                actions.start_dishwasher(device)
                await query.edit_message_text(text=f'Starting dishwasher {device}')

        else:
            await query.edit_message_text(text=f'Error')
                

async def handle_shabat_command(update: Update, context: CallbackContext):
    await go_away(update, context)

    logger.info(f'all command received')

    # Create initial message:

    tasks = actions.generate_shabat_tasks()
    message = "This is the list of tasks for shabat:\n"
    message += '\n'.join([task["description"] for task in tasks])

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("OK", callback_data="ok"),
                InlineKeyboardButton("Cancel", callback_data="cancel")
            ],
        ]
    )

    context.user_data['waiting_for_device'] = 'shabat'
    context.user_data['shabat'] = tasks
    
    await update.message.reply_text(message, reply_markup=reply_markup)

async def handle_tasks_command(update: Update, context: CallbackContext):
    await go_away(update, context)

    logger.info(f'all command received')

    # Create initial message:

    tasks = actions.get_tasks()
    message = "This is the list of tasks:\n"
    message += '\n'.join([task["description"] for task in tasks])

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Clear All", callback_data="clear"),
                InlineKeyboardButton("Cancel", callback_data="cancel")
            ],
        ]
    )

    context.user_data['waiting_for_device'] = 'tasks'
    
    await update.message.reply_text(message, reply_markup=reply_markup)
        
async def handle_test_shabat_command(update: Update, context: CallbackContext):
    await go_away(update, context)

    logger.info(f'test shabat command received')

    # Create initial message:

    if actions.test_shabat_scheduler():
        message = "Tested shabat tasks"
    else:
        message = "Exception when testing shabat tasks, please check logs"
    
    await update.message.reply_text(message)
        

async def process_message(update: Update, context: CallbackContext):
    await go_away(update, context)

    if context.user_data.get('device_in_context'):
        del context.user_data['device_in_context']
    if context.user_data.get('waiting_for_command'):
        del context.user_data['waiting_for_command']
    if context.user_data.get('waiting_for_device'):
        del context.user_data['waiting_for_device']
    if context.user_data.get('shabat'):
        del context.user_data['shabat']
    await update.message.reply_text(f'what?')

def main():

    if not TOKEN:
        logger.error("Telegram TOKEN is empty, cannot start the bot")
        return
        
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('hello', hello))
    application.add_handler(CommandHandler(DeviceType.Lights, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Sockets, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Ovens, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Curtains, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Dishwashers, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Fans, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.Heaters, handle_device_init))
    application.add_handler(CommandHandler(DeviceType.ACs, handle_device_init))
    application.add_handler(CommandHandler("tags", handle_device_tags_init))
    application.add_handler(CommandHandler("shabat", handle_shabat_command))
    application.add_handler(CommandHandler("tasks", handle_tasks_command))
    application.add_handler(CommandHandler("test", handle_test_shabat_command))
    application.add_handler(CallbackQueryHandler(handle_device_command))
    application.add_handler(MessageHandler(filters.TEXT, process_message))

    application.run_polling()

if __name__ == '__main__':
    main()
