from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import (
    Message,
)

from apps.bot.keyboard import get_main_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code


def any_user(message: Message, bot: TeleBot):
    try:
        activate(set_language_code(message.from_user.id))
        update_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_active=True,
        )
        logger.info(f"User {message.from_user.id} started the bot.")
        bot.send_message(
            message.chat.id,
            _(
                "Welcome to the bot! You can use the main menu to navigate the bot. "
                "If you have any questions, please contact the support team."
            ),
            reply_markup=get_main_buttons(),
        )
    except Exception as e:
        bot.send_message(message.chat.id, _("An error occurred."))
        logger.error(f"Error in any_user: {e}")
