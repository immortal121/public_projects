#               Telegram bot
# -----------------------------------------------------------------------------
# requirement
#
#
# 5977691196:AAFu29cO9TIHPnqlD_Up7BWeupGH0z1f40g#
import telegram.ext
Token = "5977691196:AAFu29cO9TIHPnqlD_Up7BWeupGH0z1f40g"

updater = telegram.ext.Updater("5977691196:AAFu29cO9TIHPnqlD_Up7BWeupGH0z1f40g", use_context=True)
dispatcher = updater.dispatcher

def start(update,context):
    update.message.reply_text("Hello !My Name is Tinku bot")

def help(update,context):
    update.message.reply_text(
        """
        =>/Show to see message
        =>/Add two no on chat
        =>/profile Show Profile
        """
    )

def show(update,context):
    print(context)
    update.message.reply_text(
        """
        This is Demo of Telegram Bot 
        """
    )
def profile(update,context):
    update.message.reply_text(
        """
        My message
        """
    )
def add(update,context):
    print(context)
    update.message.reply_text(
        """
        This is Demo of Telegram Bot 
        """
    )

dispatcher.add_handler(telegram.ext.CommandHandler('start',start))
dispatcher.add_handler(telegram.ext.CommandHandler('help',help))
dispatcher.add_handler(telegram.ext.CommandHandler('add',show))
dispatcher.add_handler(telegram.ext.CommandHandler('profile',show))

updater.start_polling()
updater.idle()