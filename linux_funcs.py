import os
import time
import paramiko
from dotenv import load_dotenv
from telegram import Update

load_dotenv()
ip = os.getenv('host')
log = os.getenv('user')
pa = os.getenv('pass')


def get_info_from_linux_many(my_comma = 'ls -la'):

    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(hostname=ip, username=log, password=pa)

    raw_data = None

    with cli.invoke_shell() as terminal:
        time.sleep(1)
        terminal.send('su -l\n')
        time.sleep(1)
        terminal.send(f'{pa}\n')
        time.sleep(2)
        terminal.send(f'{my_comma}\n')
        time.sleep(2)
        raw_data = terminal.recv(9999).decode()

    cli.close()
    return raw_data


def get_info_from_linux_single(my_comma = 'ls -la') -> str:

    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(hostname=ip, username=log, password=pa)
    _, s_out, s_err = cli.exec_command(my_comma, timeout=None)
    raw_data = s_out.read() + s_err.read()
    norm_str = raw_data.decode()
    cli.close()

    return norm_str

def linux_release(update: Update, context) -> None:
    my_release = get_info_from_linux_single(my_comma='lsb_release -a')
    update.message.reply_text(my_release)

def linux_uname(update: Update, context) -> None:
    my_release = get_info_from_linux_single(my_comma='uname -a')
    update.message.reply_text(my_release)

def linux_uptime(update: Update, context) -> None:
    my_release = get_info_from_linux_single(my_comma='uptime')
    update.message.reply_text(my_release)

def linux_df(update: Update, context) -> None:
    my_release = get_info_from_linux_single(my_comma='df -h')
    update.message.reply_text(my_release)

def linux_free(update: Update, context) -> None:
    my_release = get_info_from_linux_single(my_comma='free -h')
    update.message.reply_text(my_release)


if __name__ == '__main__':
    print(get_info_from_linux_single(my_comma='uname -a'))
    # print(get_info_from_linux_many())