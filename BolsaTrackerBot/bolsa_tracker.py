#!/usr/bin/env python

import time
import os
import telegram
import logging.handlers

from config import *
from lib.TelegramMessageProcessor.TelegramMessageProcessor import *

def processMessage(bot, last_update_id,logger):

    if not last_update_id:
        return None

    try:
        bot_updates = bot.getUpdates(offset=last_update_id)
    except:
        logger.exception("Raised Exception retrieving bot Updates at 'processMessage'")
        return None

    for update in bot_updates:
        if last_update_id < update.update_id:
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            logger.debug("Found new message with ID:{0} and Chat ID:{1}".format(update.update_id,chat_id))
            mp = TelegramMessageProcessor()
            message = mp.process(update)

            if not message:
                continue

            if message["text"] or message["replay_markup"]:

                # Reply the message
                bot.sendMessage(chat_id=chat_id, text=message["text"], reply_markup=message["replay_markup"])

                if message.has_key("photo"):
                    if message["photo"]:
                         bot.sendPhoto(chat_id=chat_id, photo=message["photo"])

                # Returns global offset to get the new updates
                logger.debug("Finished processing message with ID:{0} and Chat ID:{1}".format(update.update_id,chat_id))
                return update.update_id
            else:
                logger.debug("Message Seems to be None")

    return None


def main(logger):
    LAST_UPDATE_ID = None

    # Telegram Bot Authorization Token
    bot = telegram.Bot(API_KEY)

    # for updates. It starts with the latest update_id if available.
    try:
        logger.debug("Getting Telegram updates")
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
        logger.debug("Last Update ID:{0}".format(str(LAST_UPDATE_ID)))
    except:
        LAST_UPDATE_ID = None
        logger.exception("ERROR retrieving update id")

    while True:
        messageResult = processMessage(bot, LAST_UPDATE_ID,logger)

        if messageResult:
            LAST_UPDATE_ID = messageResult
        time.sleep(3)


if __name__ == '__main__':

    logger = logging.getLogger("Main")

    # change to debug level if desired
    # logging.DEBUG

    logger.setLevel(logging.DEBUG)

    main_dir = os.getcwd()
    logs_dir = main_dir + "/logs"

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create the logging file handler
    logfile = logs_dir + "/bolsatracker.log"

    fh = logging.handlers.TimedRotatingFileHandler(logfile, when='H', interval=4, backupCount=24)
    #fh = logging.FileHandler(logfile)

    formatter = logging.Formatter('%(threadName)s - %(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add handler to logger object
    logger.addHandler(fh)
    logger.info("Bot Started")

    main(logger)
