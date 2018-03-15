#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# this is the main class
# TODO move the telegram communication to a separate file
#
import logging
import argparse
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler
from wit import Wit
from handler import handle
from settings import telegram_token, wit_token, lametric_pass

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# handle all errors
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# wit.ai client
client = Wit(wit_token)


# call wit.ai to
def process_nlp(text):
    response = client.message(text)
    intents = response.get('entities').get('intent')
    intent = intents[0].get('value') if intents else None
    messages = response.get('entities').get('message_body')
    message = None
    if messages:
        message = messages[0].get('value')
    else:
        if response.get('entities').get('duration'):
            message = response.get('entities').get('duration')[0].get('value')
    return {'intent': intent, 'value': message}


# handle all requests
def process_update(bot, update):
    logger.info(update)
    message = update.message.text
    if update.message.from_user.username in ['oleksm', 'TaisNik']:
        # now process the message with wit
        what_to_do = process_nlp(message)
        if what_to_do.get('intent'):
            reply_text = handle(what_to_do.get('intent'), what_to_do.get('value'))
            update.message.reply_text(text=reply_text)
        else:
            update.message.reply_text(text='what is your intent?')
    else:
        update.message.reply_text(text='you have nothing to do here ^_^')


# the starting point for the program
def start_telegram_bot():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=telegram_token)
    dp = updater.dispatcher

    # simple start function
    dp.add_handler(CommandHandler('start', process_update))
    dp.add_handler(MessageHandler(Filters.all, process_update))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot
    updater.idle()


if __name__ == '__main__':
    # initiate the parser
    parser = argparse.ArgumentParser()
    # add all the arguments we want to receive
    parser.add_argument('--telegram', '-tg')
    parser.add_argument('--lametric', '-lm')
    parser.add_argument('--wit', '-wt')
    # parse arguments
    args = parser.parse_args()
    # check all arguments are provided
    if args.telegram and args.lametric and args.wit:
        lametric_pass = args.lametric
        telegram_token = args.telegram
        wit_token = args.wit
        start_telegram_bot()
    else:
        print('Please specify tokens as arguments to the application')
