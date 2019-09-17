#!/usr/bin/python3
# Starting of a telegram bot
# Using Library of https://github.com/python-telegram-bot/python-telegram-bot
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

import logging
import yaml
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

conf = yaml.safe_load(open('token.yml'))

updater = Updater(token=conf['telegram']['token'],use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm DK_Bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#updater.stop()
