#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# this is the main class
# TODO move the telegram communication to a separate file
#
import logging
import sys

from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, Updater, CommandHandler

import lametric

import audio

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# handle all errors
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# handle all requests
def process_update(bot, update):
    logger.info(update)
    message = update.message.text
    if update.message.from_user.username in ['oleksm', 'TaisNik']:
        if message.startswith('youtube'):
            if message.split()[1] != 'stop':
                update.message.reply_text(text='starting playing youtube song soon')
                audio.download_and_play_youtube(message.split()[1])
            else:
                update.message.reply_text(text='silence')
                audio.stop_player()
        else:
            update.message.reply_text(text='sending a notification to lametric')
            lametric.send_notification_with_cat_sound(message)
    else:
        update.message.reply_text(text='you have nothing to do here ^_^')


# the starting point for the program
def main(token):
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # simple start function
    dp.add_handler(CommandHandler('start', process_update))
    dp.add_handler(MessageHandler(Filters.all, process_update))
    dp.add_handler(CallbackQueryHandler(process_update))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv):
        lametric.lametric_pass = sys.argv.pop()
        main(sys.argv.pop())
    else:
        print('Please specify token as the only argument to the application')
