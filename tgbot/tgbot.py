import json
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater


updater = None
dispatcher = None
classifyGame = None


def send_message(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def start(update: Update, context: CallbackContext):
    send_message(context.bot, update.effective_chat.id, 'Hello!\nSend me a picture of a board game and i will try to classify it!')


def image_handler(update: Update, context: CallbackContext):
    image_id = None
    if update.message.document is not None:
        image_id = update.message.document.file_id
    elif update.message.photo != []:
        image_id = update.message.photo[0].file_id

    if image_id is not None:
        obj = context.bot.get_file(image_id)
        obj.download('image.png')
        if classifyGame is not None:
            send_message(context.bot, update.effective_chat.id, 'This is a "' + classifyGame('image.png') + '" game!')
        else:
            send_message(context.bot, update.effective_chat.id, 'Game classifier function is not specified')
    else:
        send_message(context.bot, update.effective_chat.id, 'The error has occured')


def initBot(token=None, classifyGameFunction=None):
    global updater
    global dispatcher
    global classifyGame
    if token is None:
        print('Please specify telegram bot token')
        return

    classifyGame = classifyGameFunction

    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler((Filters.document.image | Filters.photo) & (~Filters.command), image_handler))

    updater.start_polling()


def stopBot():
    if updater is not None:
        updater.stop_polling()
        print('Bot has stopped')
    else:
        print('Bot was already stopped')


if __name__ == '__main__':
    CONFIG_PATH = "config.json"
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    BOT_TOKEN = config['TG_BOT_KEY']
    initBot(token=BOT_TOKEN)
