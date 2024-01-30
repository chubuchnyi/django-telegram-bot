from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON, ADD_TOPIC_BUTTON
from tgbot.handlers.onboarding.static_text import company_name, secret_level_button_text, add_topic


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(company_name, url="http://jet-itech.com"),
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}'),
        InlineKeyboardButton(add_topic, callback_data=f'{ADD_TOPIC_BUTTON}')

    ]]

    return InlineKeyboardMarkup(buttons)
