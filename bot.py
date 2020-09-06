import re
from os import environ
from telegram.ext import (
    Updater, 
    MessageHandler
)


def valid_message(message: str) -> bool:
    forbidden_pattern = re.compile('[א-ת]')
    return re.search(forbidden_pattern, message) == None # Not found any character

def message_handler(update, context):
    """Send a message when the command /start is issued."""
    message_text = update.message.text
    user_name = update.message.from_user.first_name
    if not valid_message(message_text):
        update.message.reply_text('{}, Please write in english only dude!'.format(user_name))


if __name__ == '__main__':

    try:
        bot_token = environ['BOT_TOKEN']
    except KeyError:
            print('No env bot token have been provieded.')
            exit(1)
        

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filters=None, callback=message_handler))


    # Start the Bot
    updater.start_polling()
    updater.idle()


