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

from linux_funcs import (linux_release,
                         linux_df,
                         linux_free,
                         linux_uptime,
                         linux_uname,
                         linux_auths)

from main_funcs import (echo,
                        start,
                        my_help,
                        find_tel_numbers,
                        find_tel_numbers_command,
                        find_emails,
                        find_emails_command,
                        check_pas,
                        check_pas_command)


load_dotenv()
TG_TOKEN = os.getenv('ciuse_bot')
logging.basicConfig(filename='my_log.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




def run():
    updater = Updater(TG_TOKEN, use_context=True)
    my_disp = updater.dispatcher

    '''Перехват сообщений'''
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    '''Перехват команд'''
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', my_help)
    linux_release_handler = CommandHandler('get_release', linux_release)
    linux_uname_handler = CommandHandler('get_uname', linux_uname)
    linux_uptime_handler = CommandHandler('get_uptime', linux_uptime)
    linux_df_handler = CommandHandler('get_df', linux_df)
    linux_free_handler = CommandHandler('get_free', linux_free)
    linux_auths_handler = CommandHandler('get_auths', linux_auths)

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

    '''Перехват диалога пароля'''
    check_pas_handler = ConversationHandler(
        entry_points=[CommandHandler('verify_password', check_pas_command)],
        states={'check_pas': [MessageHandler(Filters.text & ~Filters.command, check_pas)], },
        fallbacks=[])


    '''Диспетчеры'''
    my_disp.add_handler(find_tel_numbers_handler)
    my_disp.add_handler(find_emails_handler)
    my_disp.add_handler(check_pas_handler)

    my_disp.add_handler(start_handler)
    my_disp.add_handler(help_handler)

    '''Linux'''
    my_disp.add_handler(linux_release_handler)
    my_disp.add_handler(linux_uname_handler)
    my_disp.add_handler(linux_uptime_handler)
    my_disp.add_handler(linux_df_handler)
    my_disp.add_handler(linux_free_handler)
    my_disp.add_handler(linux_auths_handler)

    my_disp.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    run()

