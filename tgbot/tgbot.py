import json
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater


updater = None
dispatcher = None
classifyGame = None
detect_checkers = None


def send_message(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def start(update: Update, context: CallbackContext):
    send_message(context.bot, update.effective_chat.id, 'Hello!\nSend me a picture of a board game and i will try to classify it!')


def image_handler(update: Update, context: CallbackContext):
    image_id = None
    if update.message.document is not None:
        image_id = update.message.document.file_id
    elif update.message.photo != []:
        image_id = update.message.photo[len(update.message.photo) - 1].file_id

    if image_id is not None:
        obj = context.bot.get_file(image_id)
        obj.download('image.png')

        game_type = classifyGame('image.png')
        send_message(context.bot, update.effective_chat.id, 'This is a "' + game_type + '" game!')
        if game_type == 'checkers':
            try:
                send_message(context.bot, update.effective_chat.id, 'Analyzing checkers game field...')
                detect_checkers('image.png', update.effective_chat.id)
            except:
                send_message(context.bot, update.effective_chat.id, 'Analyzing failed!')
    else:
        send_message(context.bot, update.effective_chat.id, 'The error has occured')


def initBot(token=None, classifyGameFunction=None, detect_checkersFunction=None):
    global updater
    global dispatcher
    global classifyGame
    global detect_checkers

    if token is None:
        print('Please specify telegram bot token')
        return

    classifyGame = classifyGameFunction
    detect_checkers = detect_checkersFunction

    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler((Filters.document.image | Filters.photo) & (~Filters.command), image_handler))

    updater.start_polling()
    return updater.bot


def stopBot():
    if updater is not None:
        updater.stop_polling()
        print('Bot has stopped')
    else:
        print('Bot was already stopped')
