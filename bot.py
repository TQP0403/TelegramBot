import os
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, InlineQueryHandler

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot", reply_markup=reply_markup)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    print(query)
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def chat(update, context):
    context.bot.send_message()


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('chat', chat))
dispatcher.add_handler(InlineQueryHandler(inline_caps))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

print('start telegram bot started')
updater.start_polling()
updater.idle()
