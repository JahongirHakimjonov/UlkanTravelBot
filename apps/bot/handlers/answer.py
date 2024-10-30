from django.utils.translation import activate, gettext as _
from telebot import TeleBot, types
from telebot.types import Message, CallbackQuery

from apps.bot.logger import logger
from apps.bot.utils.language import set_language_code
from apps.support.models import Messages, DailyMessages, Answer, Group, BotUsers  # noqa


def handle_answer_callback_query(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.message.from_user.id))
    message_id = call.data.split("_")[1]
    bot.send_message(
        call.message.chat.id,
        _("Please send your answer:"),
        reply_markup=types.ForceReply(selective=True),
    )
    bot.register_next_step_handler(call.message, save_answer, bot, message_id)


def save_answer(message: Message, bot: TeleBot, message_id: int):
    activate(set_language_code(message.from_user.id))
    answer_text = message.text

    try:
        message_obj = Messages.objects.get(id=message_id)
    except Messages.DoesNotExist:
        bot.send_message(
            message.chat.id, _("The message you are replying to does not exist.")
        )
        return

    Answer.objects.create(message=message_obj, text=answer_text)

    message_obj.is_answered = True
    message_obj.save()

    # Reply to the original message
    try:
        bot.send_message(
            message_obj.chat_id,
            _("You have received a reply:\n\n") + answer_text,
            reply_to_message_id=message_obj.message_id,
        )
    except Exception as e:
        logger.error(f"Error sending reply: {e}")

    bot.send_message(message.chat.id, _("Your answer has been saved."))
