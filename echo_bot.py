import os
import logging
from dotenv import load_dotenv
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler,
                          CallbackQueryHandler)

from linux_funcs import (linux_release,
                         linux_df,
                         linux_free,
                         linux_uptime,
                         linux_uname,
                         linux_auths,
                         linux_w,
                         linux_mpstat,
                         linux_apt_list,
                         linux_apt_list_one,
                         linux_apt_list_many,
                         linux_apt_list_one_get,
                         linux_packages_services,
                         all_install_packages,
                         all_up_services,
                         single_package_get,
                         single_service_get,
                         single_package_post,
                         single_service_post)

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
    linux_w_handler = CommandHandler('get_w', linux_w)
    linux_mpstat_handler = CommandHandler('get_mpstat', linux_mpstat)

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

    '''Перехват диалога apt list'''
    apt_list_handler = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', linux_apt_list)],
        states={'linux_apt_list_one': [MessageHandler(Filters.regex('^(Один)$'), linux_apt_list_one),
                                       MessageHandler(Filters.regex('^(Много)$'), linux_apt_list_many),
                                       MessageHandler(Filters.text, linux_apt_list_one_get)], },
        fallbacks=[])

    '''Перехват деалога запроса пакетов и сервисов'''
    decision_tree = ConversationHandler(
        entry_points=[CommandHandler('packages_services', linux_packages_services)],
        states={'first_level': [CallbackQueryHandler(all_install_packages, pattern='^all_packages$'),
                                CallbackQueryHandler(all_up_services, pattern='^all_services$'),
                                CallbackQueryHandler(single_package_get, pattern='^single_package$'),
                                CallbackQueryHandler(single_service_get, pattern='^single_service$'),],

                'second_level': [MessageHandler(Filters.text & ~Filters.command, single_package_post),],
                'third_level': [MessageHandler(Filters.text & ~Filters.command, single_service_post),]
                },
        fallbacks=[CommandHandler('packages_services', linux_packages_services)])

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
    my_disp.add_handler(linux_w_handler)
    my_disp.add_handler(linux_mpstat_handler)
    my_disp.add_handler(apt_list_handler)
    my_disp.add_handler(decision_tree)

    my_disp.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    run()
    #TODO дописать отправку из файла
