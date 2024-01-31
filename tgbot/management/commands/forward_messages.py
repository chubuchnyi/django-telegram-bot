#the feature for a Telegram bot created using the django-telegram-bot library to redirect messages from a group topic to a user and from a user to the group topic, you'll need to modify the existing Django project and create custom handlers.

# forward_messages.py

from django.core.management.base import BaseCommand
from telegram.ext import Updater, MessageHandler, Filters
from dtb.settings import TELEGRAM_TOKEN, CRM_CHAT_ID
from users.models import User
class Command(BaseCommand):
    help = 'Run the Telegram bot and forward messages'

    def handle(self, *args, **options):
        # Initialize the bot updater and dispatcher
        updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        def forward_message_to_user(user_id, message):
            # Use the bot token to send a message to the user
            updater.bot.send_message(chat_id=user_id, text=message)

        def forward_message_to_group(group_chat_id, message):
            # Use the bot token to send a message to the group chat
            updater.bot.send_message(chat_id=group_chat_id, text=message)

        def forward_group_message(update, context):
            # Extract message content and sender informatio
            message = update.message.text            
            user_chat_id = CRM_CHAT_ID + "_" + str(update.message.message_thread_id)
            user_id = User.get_topic_user_id(user_chat_id)
            forward_message_to_user(user_id, message)

        group_message_handler = MessageHandler(Filters.group, forward_group_message)
        dispatcher.add_handler(group_message_handler)

        def forward_user_message(update, context):
            # Extract message content and chat (group) information
            message = update.message.text
            user_id=update.message.from_user.id
            print("forward_user_message", user_id, message)
            group_chat_id=User.get_user_topic_id(user_id=user_id)
            updater.bot.forwardMessage(chat_id=group_chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            #update.message.chat_id
            if update.message.is_topic_message == True:
                group_chat_id=update.message.message_thread_id
            user_name= update.message.from_user.username
            print("user_name",user_name, group_chat_id, message)
            # Forward the message to the group chat
            forward_message_to_group(group_chat_id, message)
            # forward the message to the topic of groupe
             

        user_message_handler = MessageHandler(Filters.private, forward_user_message)
        dispatcher.add_handler(user_message_handler)

        # Start the bot
        updater.start_polling()
        updater.idle()




        