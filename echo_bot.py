import os
import logging
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()
TG_TOKEN = os.getenv('ciuse_bot')

logging.basicConfig(filename='my_log.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context) -> None:
    user = update.effective_user
    update.message.reply_text(f'Дороу {user.first_name}')


def echo(update: Update, context) -> None:
    update.message.reply_text(update.message.text)


def run():
    updater = Updater(TG_TOKEN, use_context=True)
    my_disp = updater.dispatcher
    my_disp.add_handler(CommandHandler('start', start))
    my_disp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
