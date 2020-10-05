from os import environ
from sys import argv
from telegram.ext import (
    Updater, 
    MessageHandler,
    CommandHandler,
    Filters
)
from telegram import Bot
from threading import Timer

RANGES = range(97, 123), range(65, 91)

def valid_message(message: str) -> bool:
    for character in message:
        if character.isalpha():
            character_code = ord(character)
            if all(character_code not in x for x in RANGES):
                print(f'invalid character {character}')
                return False
    return True
        
def message_handler(update, _):
    """Send a message when the command /start is issued."""
    message_text = update.message.text
    user_name = update.message.from_user.first_name
    if not valid_message(message_text) and not TEMPORARILY_ALLOWED:
        my_message = update.message.reply_text('{}, Please write in english only dude!'.format(user_name))
        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        timer = Timer(3, bot.delete_message, kwargs={"chat_id": my_message.chat.id, "message_id": my_message.message_id})
        timer.start()


def temporarily_allow_handler(update, _):
    """ Temporarily allow to send messages """
    global TEMPORARILY_ALLOWED
    user_id = update.message.chat.id
    if user_id == ADMIN_ID:
        TEMPORARILY_ALLOWED = True
        update.message.reply_text("Temprarily allowed!")


def disallow_handler(update, _):
    """ Temporarily allow to send messages """
    global TEMPORARILY_ALLOWED
    user_id = update.message.chat.id
    if user_id == ADMIN_ID:
        TEMPORARILY_ALLOWED = False
        update.message.reply_text("Temprarily allowed disabled!")


if __name__ == '__main__':


    TEMPORARILY_ALLOWED = False
    
    try:
        BOT_TOKEN = environ['BOT_TOKEN']
        ADMIN_ID = int(environ['ADMIN_ID'])
    except KeyError:
            print('No env bot token have been provieded.')
            print('Usage: export BOT_TOKEN=<BOT_TOKEN> ADMIN_ID=<ADMIN USER ID>')
            print('python3 {}'.format(argv[0]))
            exit(1)
        

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)
    bot = Bot(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filters=~Filters.command, callback=message_handler))
    dp.add_handler(CommandHandler("allow", callback=temporarily_allow_handler))
    dp.add_handler(CommandHandler("disallow", callback=disallow_handler))

    # Start the Bot
    print('Bot running')
    updater.start_polling()
    updater.idle()
