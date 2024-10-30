import os

from django.utils.translation import activate, gettext as _
from telebot import TeleBot

from apps.bot.logger.logging import logger
from apps.bot.utils.language import set_language_code
from apps.support.models import BotUsers, News

bot = TeleBot(os.getenv("BOT_TOKEN"))


def send_news(user_id, title, content, image, news_id):
    try:
        user = BotUsers.objects.get(id=user_id)
        news = News.objects.get(id=news_id)
        activate(set_language_code(user.telegram_id))
        logger.info(f"Sending message to {user.telegram_id}")
        if not isinstance(user.telegram_id, int):
            raise ValueError("Invalid telegram_id: must be an integer")
        if not image:
            raise ValueError("Image must be non-empty")
        if (
            image.size > 5 * 1024 * 1024
        ):  # Check if the image size is greater than 10 MB
            raise ValueError("Image size exceeds the 10 MB limit")
        message = _(f"{news.title}\n\n{news.content}")
        bot.send_photo(
            user.telegram_id, news.image, caption=message, parse_mode="Markdown"
        )
    except BotUsers.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except ValueError as e:
        logger.error(e)
