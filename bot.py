import re
from os import environ
from sys import argv
from telegram.ext import (
    Updater, 
    MessageHandler
)
from telegram import Bot


def valid_message(message: str) -> bool:
    forbidden_pattern = re.compile('[א-ת]')
    return re.search(forbidden_pattern, message) == None # Not found any character

def message_handler(update, context):
    """Send a message when the command /start is issued."""
    message_text = update.message.text
    user_name = update.message.from_user.first_name
    if not valid_message(message_text):
        print(update)

        update.message.reply_text('{}, Please write in english only dude!'.format(user_name))
        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)


if __name__ == '__main__':
    
    try:
        bot_token = environ['BOT_TOKEN']
    except KeyError:
            print('No env bot token have been provieded.')
            print('Usage: export BOT_TOKEN=<BOT_TOKEN>')
            print('python3 {}'.format(argv[0]))
            exit(1)
        

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)
    bot = Bot(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filters=None, callback=message_handler))


    # Start the Bot
    print('Bot running')
    updater.start_polling()
    updater.idle()


