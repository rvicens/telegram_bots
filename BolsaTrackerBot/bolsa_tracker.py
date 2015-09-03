#!/usr/bin/env python

import time
import logging
import telegram

from config import *
from lib.TelegramMessageProcessor.TelegramMessageProcessor import *

def processMessage(bot, last_update_id,logger):
    for update in bot.getUpdates(offset=last_update_id):
        if last_update_id < update.update_id:
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            logger.debug("Found new message with ID:{0} and Chat ID:{1}".format(update.update_id,chat_id))
            mp = TelegramMessageProcessor()
            message = mp.process(update)

            if (message):
                # Reply the message
                bot.sendMessage(chat_id=chat_id, text=message)
                # Returns global offset to get the new updates
                logger.debug("Finished processing message with ID:{0} and Chat ID:{1}".format(update.update_id,chat_id))
                return update.update_id
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
    except IndexError:
        LAST_UPDATE_ID = None
        logger.exception("ERROR retrieving update id")

    while True:
        messageResult = processMessage(bot, LAST_UPDATE_ID,logger)
        if messageResult:
            LAST_UPDATE_ID = messageResult
        time.sleep(3)


if __name__ == '__main__':

    log_level = logging.DEBUG
    #logger = logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    hdlr = logging.FileHandler('logs/bolsatracker.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(log_level)

    main(logger)
