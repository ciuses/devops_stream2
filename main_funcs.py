import re
from telegram import Update
from telegram.ext import ConversationHandler
from db_model_data import Emails, Telephons, select_from_tables, add_telephons, add_emails


telephons_string = None
emails_string = None

def start(update: Update, _) -> None:
    user = update.effective_user
    update.message.reply_text(f'Приветствую {user.first_name}, aka {user.username}, USER ID: {user.id}')


def my_help(update: Update, _) -> None:
    help_str = ('/start - поприветствует\n'
                '/help - список доступных команд\n'
                '/exit - выход, если застрял\n'
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
                '/get_ss - порты\n'
                '/packages_services - установленные пакеты и службы ОС\n'
                '/get_repl_logs - логи реплики\n'
                '/get_emails - получить имейлы из базы\n'
                '/get_phone_numbers - получить номера')

    update.message.reply_text(help_str)


def echo(update: Update, _) -> None:
    update.message.reply_text(update.message.text)


def find_tel_numbers_command(update: Update, _) -> str:
    update.message.reply_text('Давай, где искать: ')
    return 'find_tel_numbers'


def find_tel_numbers(update: Update, _) -> int | str:
    user_input = update.message.text
    find_pat = re.compile(r'[\+7|8][\d(\s-]*[\d)\s]*')  # [\+7|8][\d(\s-]*[\d)\s]*
    find_result = find_pat.findall(user_input)

    if find_result:
        str_numbers = ''
        for my_index in range(len(find_result)):
            str_numbers += f'{my_index + 1}.\t{find_result[my_index]}\n'

        update.message.reply_text(f'<pre language="python">{str_numbers}</pre>', parse_mode='HTML')
        global telephons_string # запретная магия, за такое наказывают
        telephons_string = str_numbers
        update.message.reply_text('Хотелось бы Вам любезнейший, сохранить результаты в базку?')
        # return ConversationHandler.END  # <class 'int'> -1
        return 'telephone_step'

    else:
        update.message.reply_text('Нет номеров!')
        return ConversationHandler.END

def write_tel_numbers(update: Update, _) -> int:
    if telephons_string:
        list_of_tels = telephons_string.splitlines(keepends=True)

        for num in list_of_tels:
            _, tel = num.split('\t')
            clean_num = tel.replace('\n', '')

            try:
                add_telephons(my_num=clean_num)
            except Exception as exp:
                update.message.reply_text(exp)

        update.message.reply_text('Хорошо, сохраняю!')
        return ConversationHandler.END

    else:
        update.message.reply_text('Нет номеров!')
        return ConversationHandler.END



def get_from_the_database_telephons(update: Update, _) -> int:  # TODO добавить elif для строк более 4096
    query_tels = Telephons.id, Telephons.number
    telephons = select_from_tables(many_data=query_tels)

    if telephons:
        str_tels = ''
        for ind, tel in telephons:
            str_tels += f'{ind}. {tel}\n'
        update.message.reply_text(f'<pre language="python">{str_tels}</pre>', parse_mode='HTML')
        return ConversationHandler.END

    else:
        update.message.reply_text('В базе пусто!')
        return ConversationHandler.END


def find_emails_command(update: Update, _) -> str:
    update.message.reply_text('Ладно уж, по ищу ка я твои имэйлы: ')
    return 'find_emails'


def find_emails(update: Update, _) -> int | str:
    user_input = update.message.text
    find_pat = re.compile(r'[\w\.-]+@[\w-]+\.[a-zа-я]{2,9}')
    find_result = find_pat.findall(user_input)

    if find_result:
        str_numbers = ''
        for my_index, email in enumerate(find_result, start=1):
            str_numbers += f'{my_index}.\t{email}\n'

        update.message.reply_text(f'<pre language="python">{str_numbers}</pre>', parse_mode='HTML')
        global emails_string
        emails_string = str_numbers
        update.message.reply_text('Хотелось бы Вам любезнейший, сохранить результаты в базку?')
        return 'email_step'

    else:
        update.message.reply_text('Нет ни каких имэйлов!')
        return ConversationHandler.END


def write_emails(update: Update, _) -> int:
    if emails_string:
        list_of_emails = emails_string.splitlines(keepends=True)

        for ema in list_of_emails:
            _, email = ema.split('\t')
            clean_email = email.replace('\n', '')
            try:
                add_emails(my_ema=clean_email)
            except Exception as exp:
                update.message.reply_text(exp)

        update.message.reply_text('Хорошо, сохраняю!')
        return ConversationHandler.END

    else:
        update.message.reply_text('Нет имейлов!')
        return ConversationHandler.END


def get_from_the_database_emails(update: Update, _) -> int:  # TODO добавить elif для строк более 4096
    query_emails = Emails.id, Emails.email
    mails = select_from_tables(many_data=query_emails)

    if mails:
        str_emails = ''
        for ind, email in mails:
            str_emails += f'{ind}. {email}\n'
        update.message.reply_text(f'<pre language="python">{str_emails}</pre>', parse_mode='HTML')
        return ConversationHandler.END

    else:
        update.message.reply_text('В базе пусто!')
        return ConversationHandler.END


def check_pas_command(update: Update, _) -> str:
    update.message.reply_text('Мне нужен твой байк, простите, пароль: ')
    return 'check_pas'


def check_pas(update: Update, _) -> int:
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


def my_exit(update: Update, _) -> int:
    return ConversationHandler.END
