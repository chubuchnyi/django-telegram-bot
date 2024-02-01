import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from telegram import Bot



from tgbot.dispatcher import setup_dispatcher


from telegram.ext import Updater, MessageHandler, Filters
from dtb.settings import TELEGRAM_TOKEN, CRM_CHAT_ID
from users.models import User

def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    updater = Updater(tg_token, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)


    def forward_message_to_user(user_id, message):
            # Use the bot token to send a message to the user
            print(updater.bot.send_message(chat_id=user_id, text=message))

    def forward_message_to_group(chat_id, message):
        # Use the bot token to send a message to the group chat
        #id is the substring of the chat_id = CRM_CHAT_ID + "_" + str(message_thread_id)
        message_thread_id = chat_id.split("_")[1]

        print(updater.bot.sendMessage(chat_id=CRM_CHAT_ID, text=message,message_thread_id = message_thread_id))

        #send message to the thread of the chat
        #updater.bot.sendMessage(chat_id=group_chat_id, text=message, reply_to_message_id=update.message.message_id, message_thread_id=update.message.message_thread_id)

    def forward_group_message(update, context):
        # Extract message content and sender informatio
        message = update.message.text            
        user_chat_id = CRM_CHAT_ID + "_" + str(update.message.message_thread_id)
        user_id = User.get_topic_user_id(user_chat_id)
        print("forward_group_message", user_id, message, user_chat_id)
        if user_id is None:
            print("user_id is None")
            return
        try:
            forward_message_to_user(user_id, message)
        except:
            print("user_id", str(user_id), "is not valid")
            return
        

    group_message_handler = MessageHandler(Filters.chat_type.groups, forward_group_message)
    dp.add_handler(group_message_handler)

    def forward_user_message(update, context):
        # Extract message content and chat (group) information
        message = update.message.text
        user_id=update.message.from_user.id
        
        group_chat_id=User.get_user_topic_id(user_id=user_id)
        #updater.bot.forwardMessage(chat_id=group_chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        print("forward_user_message", user_id, message, group_chat_id)
        if group_chat_id is None:
            print("group_chat_id is None")
            return
        
        try:
            forward_message_to_group(group_chat_id, message)
        except:
            print("user_id", str(user_id), "is not valid")

        # if update.message.is_topic_message == True:
        #     group_chat_id=update.message.message_thread_id
        # user_name= update.message.from_user.username
        # print("user_name",user_name, group_chat_id, message)
        # # Forward the message to the group chat
        # forward_message_to_group(group_chat_id, message)

            

    user_message_handler = MessageHandler(Filters.chat_type.private, forward_user_message)
    dp.add_handler(user_message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
