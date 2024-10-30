import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from telebot import TeleBot

from apps.order.models import Order, Group

bot = TeleBot(os.getenv("BOT_TOKEN"))


@receiver(post_save, sender=Order)
def post_save_answer(sender, instance, created, **kwargs):
    if created:
        try:
            groups = Group.objects.all()
            for group in groups:
                text = f"Ism Familiya:\t\t{instance.name}\n\nTelefon raqam:\t\t{instance.phone}\n\nEmail:\t\t{instance.email}\n\nXabar:\t\t{instance.message}"
                bot.send_message(
                    group.group_id,
                    text=text,
                )
        except Exception as e:
            print(f"Error sending message: {e}")
        print(f"New answer created: {instance.name}")
