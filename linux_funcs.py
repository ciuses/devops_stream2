import os
import subprocess
import time
import paramiko
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

load_dotenv()
ip = os.getenv('host')
log = os.getenv('user')
pa = os.getenv('pass')


def get_info_from_linux_single(my_comma='ls -la',
                               superuser=False,
                               host=ip,
                               login=log,
                               password=pa,
                               su_pass=pa) -> str:
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(hostname=host, username=login, password=password)

    if superuser:
        with cli.invoke_shell() as terminal:
            time.sleep(1)
            terminal.send(b'su --login\n')
            time.sleep(1)
            terminal.send(f'{su_pass}\n'.encode())
            time.sleep(2)
            terminal.send(f'{my_comma}\n'.encode())
            time.sleep(2)
            raw_data = terminal.recv(9999).decode()

        cli.close()
        return raw_data

    else:
        _, s_out, s_err = cli.exec_command(my_comma, timeout=None)
        raw_data = s_out.read() + s_err.read()
        norm_str = raw_data.decode()
        cli.close()

        return norm_str


def chank_it(my_input: str) -> list:
    '''
    Функция режет строку на строки и нарезает по 15 строк в список.
    :param my_input: Строка
    :return: Список строк по 15
    '''
    all_list = my_input.splitlines(keepends=True)
    list_of_ten = [''.join(all_list[group:group + 15]) for group in range(0, len(all_list), 15)]
    return list_of_ten


def linux_release(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='lsb_release -a')
    update.message.reply_text(my_release)


def linux_uname(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='uname -a')
    update.message.reply_text(my_release)


def linux_uptime(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='uptime')
    update.message.reply_text(my_release)


def linux_df(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='df -h')
    update.message.reply_text(my_release)


def linux_free(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='free -h')
    update.message.reply_text(my_release)


def linux_auths(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='last -n 10')
    update.message.reply_text(my_release)


def linux_w(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='w')
    update.message.reply_text(my_release)


def linux_mpstat(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='top', superuser=True)
    update.message.reply_text(my_release[461:])


def linux_critical(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='dmesg -H --level=err', superuser=True)  # crit
    update.message.reply_text(my_release[461:])


def linux_ps(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='ps')
    update.message.reply_text(my_release)


def linux_ss(update: Update, _) -> None:
    my_release = get_info_from_linux_single(my_comma='ss')
    if len(my_release) > 4096:
        my_chanks = chank_it(my_release)
        for one_chank in my_chanks:
            update.message.reply_text(one_chank)
    else:
        update.message.reply_text(my_release)


'''Другой концепт диалога где спрашиваешь уточнения.'''


# TODO выпилить этот блок, оно эксперементально
def linux_apt_list(update: Update, _) -> str:
    replay_keyboard = [['Один', 'Много']]
    markup_keys = ReplyKeyboardMarkup(replay_keyboard, one_time_keyboard=True)
    update.message.reply_text('Выбери режим, одного пакета или много?', reply_markup=markup_keys, )
    return 'linux_apt_list_one'


def linux_apt_list_one(update: Update, _) -> str:
    update.message.reply_text('Введи название пакета', reply_markup=ReplyKeyboardRemove(), )
    return 'linux_apt_list_one'


def linux_apt_list_one_get(update: Update, _) -> int:
    user_input = update.message.text
    my_release = get_info_from_linux_single(my_comma=f'apt list | grep {user_input}')
    update.message.reply_text(my_release)
    return ConversationHandler.END


def linux_apt_list_many(update: Update, _) -> int:  # выходит большой список
    my_release = get_info_from_linux_single(my_comma='apt list')
    update.message.reply_text(my_release)
    return ConversationHandler.END


'''Диалог через инлайн кнопки.'''


def linux_packages_services(update, _) -> str:
    k_board = [
        [InlineKeyboardButton('Получить список всех установленных пакетов', callback_data='all_packages')],
        [InlineKeyboardButton('Получить список всех запущенных служб', callback_data='all_services'), ],
        [InlineKeyboardButton('Получить информацию о конкретном пакете', callback_data='single_package'), ],
        [InlineKeyboardButton('Получить информацию о конкретной службе', callback_data='single_service'), ],
    ]

    mrk = InlineKeyboardMarkup(k_board)
    update.message.reply_text(text='Выберете один из вариантов получения информации о пакетах или службах:',
                              reply_markup=mrk)
    return 'first_level'


def all_install_packages(update, _) -> str:
    quiry = update.callback_query
    quiry.answer()
    my_all_packages = get_info_from_linux_single(my_comma='apt list --installed')

    if len(my_all_packages) > 4096:
        my_chanks = chank_it(my_all_packages)
        for one_chank in my_chanks:
            quiry.message.reply_text(one_chank)
    else:
        quiry.message.reply_text(my_all_packages)

    return 'first_level'


def all_up_services(update, _) -> str:
    quiry = update.callback_query
    quiry.answer()
    my_all_services = get_info_from_linux_single(my_comma='systemctl list-units --type service --state running')

    if len(my_all_services) > 4096:
        my_chanks = chank_it(my_all_services)
        for one_chank in my_chanks:
            quiry.message.reply_text(one_chank)
    else:
        quiry.message.reply_text(my_all_services)

    return 'first_level'


def single_package_get(update, _) -> str:
    quiry = update.callback_query
    quiry.answer()
    k_board = [[InlineKeyboardButton("...", callback_data='_'), ]]
    rmk = InlineKeyboardMarkup(k_board)
    quiry.edit_message_text(text='Напиши название пакета: ', reply_markup=rmk)

    return 'second_level'


def single_package_post(update, _) -> str:
    user_input = update.message.text
    my_single_package = get_info_from_linux_single(my_comma=f'apt list --installed | grep {user_input}')

    if len(my_single_package) > 4096:
        my_chanks = chank_it(my_single_package)
        for one_chank in my_chanks:
            update.message.reply_text(one_chank)
    else:
        update.message.reply_text(my_single_package)

    # update.message.reply_text(my_single_package)
    return 'second_level'


def single_service_get(update, _) -> str:
    quiry = update.callback_query
    quiry.answer()
    k_board = [[InlineKeyboardButton("...", callback_data='_'), ]]
    rmk = InlineKeyboardMarkup(k_board)
    quiry.edit_message_text(text='Напиши название службы: ', reply_markup=rmk)

    return 'third_level'


def single_service_post(update, _) -> str:
    user_input = update.message.text
    my_single_service = get_info_from_linux_single(my_comma=f'systemctl list-units --type service | grep {user_input}',
                                                   superuser=True)
    update.message.reply_text(my_single_service[461:])
    return 'third_level'


def linux_replica_log(update: Update, _) -> None:
    my_com = 'tail -n 15 /var/log/postgresql/postgresql-15-main.log'
    log_15_str = get_info_from_linux_single(my_comma=my_com,
                                            superuser=True,
                                            host=os.getenv('v_host'),
                                            login=os.getenv('v_user'),
                                            password=os.getenv('v_pass'),
                                            su_pass=os.getenv('v_su_pass'))

    update.message.reply_text(f'<pre language="python">{log_15_str[495:]}</pre>', parse_mode='HTML')

def linux_replica_log2(update: Update, _) -> None:
    my_data = subprocess.run(["tail", "/tmp/postgresql-my.log"], capture_output=True)
    update.message.reply_text(f'<pre language="python">{my_data.stdout.decode()}</pre>', parse_mode='HTML')


if __name__ == '__main__':
    pass
    # print(get_info_from_linux_single(my_comma='ss'))
    # h = os.getenv('v_host')
    # u = os.getenv('v_user')
    # p = os.getenv('v_pass')
    # sp = os.getenv('v_su_pass')
    #
    # print(get_info_from_linux_single(host=h, login=u, password=p, su_pass=sp))

    # linux_replica_log()
