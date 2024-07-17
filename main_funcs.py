import re
from telegram import Update
from telegram.ext import ConversationHandler


def start(update: Update, context) -> None:
    user = update.effective_user
    update.message.reply_text(f'Привествую {user.first_name}, aka {user.username}, USER ID: {user.id}')

def my_help(update: Update, context) -> None:
    help_str = ('/start - поприветствует\n'
                '/help - список доступных команд\n'
                '/find_tel_numbers - поиск телефона в тексте\n'
                '/find_emails - поиск электронного адреса в тексте\n'
                '/verify_password - валидация пароля\n'
                '/get_release - посмотреть релиз\n'
                '/get_uname - архитектуру\n'
                '/get_uptime - время работы\n'
                '/get_df - место\n'
                '/get_free - утилизация оперативки\n'
                '/get_mpstat - производительность\n'
                '/get_w - пользователи в системе\n'
                '/get_auths - последние 10 юзеров\n'
                '/get_critical - ошибки ядра\n'
                '/get_ps - процессы\n'
                '/get_ss - порты')

    update.message.reply_text(help_str)

def echo(update: Update, context) -> None:
    update.message.reply_text(update.message.text)

def find_tel_numbers_command(update: Update, context) -> str:
    update.message.reply_text('Давай, где искать: ')
    return 'find_tel_numbers'

def find_tel_numbers(update: Update, context) -> int:
    user_input = update.message.text
    find_pat = re.compile(r'[\+7|8][\d(\s-]*[\d)\s]*')  # [\+7|8][\d(\s-]*[\d)\s]*
    find_result = find_pat.findall(user_input)

    if find_result:
        str_numbers = ''
        for my_index in range(len(find_result)):
            str_numbers += f'{my_index + 1}.\t{find_result[my_index]}\n'

        update.message.reply_text(str_numbers)
        return ConversationHandler.END # <class 'int'> -1

    else:
        update.message.reply_text('Нет номеров!')
        return ConversationHandler.END

def find_emails_command(update: Update, context) -> str:
    update.message.reply_text('Ладно уж, по ищу ка я твои имэйлы: ')
    return 'find_emails'

def find_emails(update: Update, context) -> int:
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
        update.message.reply_text('Нет ни каких имэйлов!')
        return ConversationHandler.END

def check_pas_command(update: Update, context) -> str:
    update.message.reply_text('Мне нужен твой байк, простите, пароль: ')
    return 'check_pas'

def check_pas(update: Update, context) -> int:

    user_input = update.message.text

    if not re.search(r'^.{8,}$', user_input):
        update.message.reply_text('Ваш пароль мог быть и подлиннее, обидно как то даже.')
        return ConversationHandler.END

    elif not re.search(r'(?=.*[A-Z])', user_input):
        update.message.reply_text('Не нашёл букв по крупнее, мелочь одна.')
        return ConversationHandler.END

    elif not re.search(r'(?=.*[a-z])', user_input):
        update.message.reply_text('Не капси, добавь пару мелких букв.')
        return ConversationHandler.END

    elif not re.search(r'(?=.*[0-9])', user_input):
        update.message.reply_text('А где же числа?')
        return ConversationHandler.END

    elif not re.search(r'(?=.*[!@#$%^&*()])', user_input):
        update.message.reply_text('Отсыпь спецсимволов не жадничай.')
        return ConversationHandler.END

    else:
        update.message.reply_text('Впечатляет, всё как надо, обнимаю твои мысли, всё на созвоне.')
        return ConversationHandler.END


def my_exit(update: Update, context) -> int:
    return ConversationHandler.END