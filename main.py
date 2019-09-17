#!/usr/bin/python3
"""Starting of a telegram bot
Using Library of https://github.com/python-telegram-bot/python-telegram-bot
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot"""


import logging
import yaml
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

CONF = yaml.safe_load(open('token.yml'))

# From version 13 'use_context=True' will be the default.
UPDATER = Updater(token=CONF['telegram']['token'], use_context=True)
DISPATCHER = UPDATER.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    """Reaction to '/start' command messages"""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="I'm DK_Bot, please talk to me!")


START_HANDLER = CommandHandler('start', start)
DISPATCHER.add_handler(START_HANDLER)

UPDATER.start_polling()


def echo(update, context):
    """Echo all non-command messages it receives"""
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


ECHO_HANDLER = MessageHandler(Filters.text, echo)
DISPATCHER.add_handler(ECHO_HANDLER)


def inline_caps(update, context):
    """inline functionality, all text to UPPERCASE/CAPS - https://core.telegram.org/bots/inline"""
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


INLINE_CAPS_HANDLER = InlineQueryHandler(inline_caps)
DISPATCHER.add_handler(INLINE_CAPS_HANDLER)


def unknown(update, context):
    """a MessageHandler with a command filter to reply to all commands
    that were not recognized by the previous handler"""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand that command.")


UNKNOWN_HANDLER = MessageHandler(Filters.command, unknown)
DISPATCHER.add_handler(UNKNOWN_HANDLER)

#updater.stop()
