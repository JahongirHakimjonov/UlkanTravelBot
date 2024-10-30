from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot import types
from telebot.types import Message

from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.support.models import Info, InfoLinks


def handle_info(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    infos = Info.objects.filter(is_active=True)
    if not infos:
        bot.send_message(
            message.chat.id,
            _("There is no information available."),
            reply_to_message_id=message.message_id,
        )
    for info in infos:
        links = InfoLinks.objects.filter(is_active=True, info=info)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = []

        for link in links:
            button = types.InlineKeyboardButton(text=link.name, url=link.link)
            buttons.append(button)

        # Add buttons to the keyboard in pairs
        for i in range(0, len(buttons), 2):
            keyboard.add(*buttons[i: i + 2])

        caption = f"{info.full_name}\n\n{info.birth_date} - {info.age}\n\n{info.info}"
        bot.send_photo(
            message.chat.id,
            photo=info.photo,
            caption=caption,
            reply_markup=keyboard,
        )
    logger.info(f"User {message.from_user.id} requested info.")
