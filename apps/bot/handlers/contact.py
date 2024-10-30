from django.utils import timezone
from django.utils.translation import activate, gettext as _
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message, CallbackQuery

from apps.bot.keyboard import get_main_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.support.models import Messages, DailyMessages, Answer, Group, BotUsers  # noqa
from apps.support.models import Messages, DailyMessages, Group


def handle_contact(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    logger.info(f"User {message.from_user.id} requested contact.")
    contact_button = types.InlineKeyboardButton(
        text=_("Contact"), callback_data="contact"
    )
    cancel_button = types.InlineKeyboardButton(text=_("Cancel"), callback_data="cancel")
    keyboard.add(contact_button, cancel_button)
    bot.send_message(message.chat.id, _("Contact us or cancel:"), reply_markup=keyboard)


def handle_delete_contact_callback(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.message.from_user.id))
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id, _("Has been canceled."), reply_markup=get_main_buttons()
    )


def handle_contact_callback_query(call: CallbackQuery, bot: TeleBot):
    activate(set_language_code(call.message.from_user.id))
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        _("Please send your message:"),
        reply_markup=types.ForceReply(selective=True),
    )
    bot.register_next_step_handler(call.message, save_user_message, bot)


def save_user_message(message: Message, bot: TeleBot):
    activate(set_language_code(message.from_user.id))
    user_message = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    user = BotUsers.objects.get(telegram_id=user_id)

    # Check the number of messages sent by the user today
    today = timezone.now().date()
    daily_message = DailyMessages.objects.filter(user=user, message_date=today).first()

    if daily_message:
        if daily_message.message_count >= 5:
            bot.send_message(
                message.chat.id,
                _("You have reached the daily message limit."),
                reply_markup=get_main_buttons(),
                reply_to_message_id=message_id,
            )
            return
    else:
        daily_message = DailyMessages(user=user, message_date=today, message_count=0)

    # Save the message to Messages model
    sending_message, created = Messages.objects.update_or_create(
        user=user,
        chat_id=chat_id,
        message_id=message_id,
        defaults={"text": user_message},
    )

    # Update or create the DailyMessages entry
    daily_message.message_count += 1
    daily_message.save()

    # Send the message to the group
    groups = Group.objects.filter(is_active=True)

    text = f"User: {user_id}\n\nMessage ID: {message_id}\n\nUsername: @{user.username}\n\nFull Name: {user.first_name} {user.last_name}\n\nMessage: {user_message}"

    inline_keyboard = InlineKeyboardMarkup()
    inline_button = InlineKeyboardButton(
        text="Reply", callback_data=f"answer_{sending_message.id}"
    )
    inline_keyboard.add(inline_button)

    for group in groups:
        try:
            bot.send_message(group.group_id, text=text, reply_markup=inline_keyboard)
        except Exception as e:
            logger.error(f"Error sending message to group {group.group_id}: {e}")

    bot.send_message(
        message.chat.id,
        _("Your message has been sent and saved."),
        reply_to_message_id=message_id,
        reply_markup=get_main_buttons(),
    )
