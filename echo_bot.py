import os
import logging
import re
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler)

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


def my_help(update: Update, context) -> None:
    update.message.reply_text('No help!')


def find_tel_numbers_command(update: Update, context) -> None:
    update.message.reply_text('Давай, где искать: ')
    return 'find_tel_numbers'


def find_tel_numbers(update: Update, context):
    user_input = update.message.text
    find_pat = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}')  # [\+7|8][\d(\s-]*[\d)\s]*
    find_result = find_pat.findall(user_input)

    if find_result:
        str_numbers = ''
        for my_index in range(len(find_result)):
            str_numbers += f'{my_index + 1}.\t{find_result[my_index]}\n'

        update.message.reply_text(str_numbers)
        return ConversationHandler.END

    else:
        update.message.reply_text('Нет номеров!')
        return ConversationHandler.END

def find_emails_command(update: Update, context) -> None:
    update.message.reply_text('Ладно уж, по ищу ка я твои имэйлы: ')
    return 'find_emails'


def find_emails(update: Update, context):
    user_input = update.message.text
    find_pat = re.compile(r'[\w\.-]+@[\w-]+\.[a-zа-я]{2,9}')
    find_result = find_pat.findall(user_input)

    if find_result:
        str_numbers = ''
        for my_index, email in enumerate(find_result, start=1):
            str_numbers += f'{my_index}.\t{email}\n'

        update.message.reply_text(str_numbers)
        return ConversationHandler.END

    else:
        update.message.reply_text('Нет номеров!')
        return ConversationHandler.END


def run():
    updater = Updater(TG_TOKEN, use_context=True)
    my_disp = updater.dispatcher

    '''Перехват сообщений'''
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)

    '''Перехват команд'''
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', my_help)

    '''Перехват диалога тела'''
    find_tel_numbers_handler = ConversationHandler(
        entry_points=[CommandHandler('find_tel_numbers', find_tel_numbers_command)],
        states={'find_tel_numbers': [MessageHandler(Filters.text & ~Filters.command, find_tel_numbers)], },
        fallbacks=[])

    '''Перехват диалога мыла'''
    find_emails_handler = ConversationHandler(
        entry_points=[CommandHandler('find_emails', find_emails_command)],
        states={'find_emails': [MessageHandler(Filters.text & ~Filters.command, find_emails)], },
        fallbacks=[])


    '''Диспетчеры'''
    my_disp.add_handler(find_tel_numbers_handler)
    my_disp.add_handler(find_emails_handler)
    my_disp.add_handler(start_handler)
    my_disp.add_handler(help_handler)
    my_disp.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    run()
