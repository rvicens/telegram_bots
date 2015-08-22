#!/usr/bin/env python

import time
import logging
import telegram

class MessageProcessor():

	def __init__(self):
		self.msg = None

	def extractMessage(self,tlg_msg):
		self.msg = tlg_msg.message.text.encode('utf-8')

	def validateMessage(self):
		return True

	def process(self,tlg_msg):
		self.extractMessage(tlg_msg)
		if self.validateMessage():
			return self.msg
		return None

def processMessage(bot,last_update_id):
	
	for update in bot.getUpdates(offset=last_update_id):
		if last_update_id < update.update_id:

			# chat_id is required to reply any message
			chat_id = update.message.chat_id
			mp = MessageProcessor()
			message = mp.process(update) 
			
			if (message):
				# Reply the message
				bot.sendMessage(chat_id=chat_id, text=message)

				# Returns global offset to get the new updates
				return update.update_id
	return None

def main():

	LAST_UPDATE_ID = None

	# Telegram Bot Authorization Token
	bot = telegram.Bot('135410251:AAEd26Jua5Z_OpUOyMyzI7Hx_34_Q3q6_s0')

	# for updates. It starts with the latest update_id if available.
	try:
		LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
	except IndexError:
		LAST_UPDATE_ID = None

	while True:
		messageResult = processMessage(bot,LAST_UPDATE_ID)
		if messageResult:
			LAST_UPDATE_ID = messageResult
		time.sleep(3)


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	main()
