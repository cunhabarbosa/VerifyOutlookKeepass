"""
Check if all my email accounts in the Keepass file are configured in Microsoft Outlook and send the result via Telegram

Author: Antonio Barbosa
E-mail: cunha.barbosa@gmail.com
Version: [1.0.0] - 2022-01-25
"""

import os
import sys
from pykeepass import PyKeePass
import win32com.client
from configparser import ConfigParser

# Tony Library
from library import benchmark
from library import telegram

# Read config.ini file
# https://tutswiki.com/read-write-config-files-in-python/
config_object = ConfigParser()
config_object.read('settings.ini')

#Keepass config
keepass_directory = config_object['KEEPASS_FILE']['KEEPASS_DIRECTORY']
keepass_filename = config_object['KEEPASS_FILE']['KEEPASS_FILENAME']
keepass_password = config_object['KEEPASS_FILE']['KEEPASS_PASSWORD']
keepass_group = config_object['KEEPASS_FILE']['KEEPASS_DB_GROUP']

# Telegram info
telegram_token = config_object['TELEGRAM_INFO']['telegram_token']
telegram_chat_id = config_object['TELEGRAM_INFO']['telegram_chat_id']


def load_database(dir_name, base_filename, pass_filename):
    """
    Load database
    :return:
    """
    filename = os.path.join(dir_name, base_filename)
    print(filename)

    kp = PyKeePass(filename, password=pass_filename)
    return kp


def find_group(kp_db=None, name_db='email', first_db=True):
    """
    Find any group by its name
    :param kp_db:
    :param name_db:
    :param first_db:
    :return:
    """
    if kp_db is None:
        raise "Database not defined"

    return kp_db.find_groups(name=name_db, first=first_db)


def find_entries(kp_group = None):
    """
    Get the entries in a group
    :param kp_group:
    """
    if kp_group is None:
        raise "Group not defined"
    kp_entries = group.entries
    # print(*entries, sep = "\n")   # Print all entries
    # Entry: "AntonioB/email/FEUP - cunha.barbosa (ei03023@fe.up.pt)"
    # Entry: "AntonioB/email/Gmail - acbarbosamail (acbarbosamail@gmail.com)"
    # Entry: "AntonioB/email/Gmail - antoniocunhabarbosa (antoniocunhabarbosa@gmail.com)"
    return kp_entries


def email_entries_outlook():
    """

    :return:
    """
    email_list = []
    try:
        outlook = win32com.client.Dispatch('outlook.application')
        mapi = outlook.GetNamespace("MAPI")

        for account in mapi.Accounts:
            email_account: object = account.DeliveryStore.DisplayName
            # print(email_account)
            email_list.append(email_account)
    except Exception as e:
        raise e

    return email_list


def check_entries_outlook(list_outlook, list_keepass):
    """
    Check
    :param list_outlook:
    :param list_keepass:
    """
    if list_outlook is None and list_keepass is None:
        raise "One of the lists is None"

    result_outlook = []
    for keepass in list_keepass:
        exists = any(keepass in string for string in list_outlook)
        message_outlook = keepass + " : " + str(exists)
        # print(f"{message}!")
        result_outlook.append(message_outlook)

    return result_outlook


if __name__ == '__main__':
    initial_time = benchmark.benchmark_ini()  # Begin benchmark

    database = load_database(keepass_directory, keepass_filename, keepass_password)
    group = find_group(database, keepass_group)
    entries = find_entries(group)

    my_email_list = []
    for entry in entries:
        # Entry: "AntonioB/email/FEUP - cunha.barbosa (ei03023@fe.up.pt)"
        # Title:
        # Username: "ei03023@fe.up.pt
        title = entry.title  # FEUP - cunha.barbosa
        title_sub = title.split(" - ", 1)[0]  # FEUP
        username = entry.username
        try:
            title_user = title.split(" - ", 1)[1]  # cunha.barbosa
        except (Exception,):
            pass

        # todo: Definition
        email_not_to_check = ['Clix', 'FEUP', 'Google Account', 'Google Apps', 'INESCTEC', 'Live ID'
                            , 'Microsoft Account', 'Office365', 'Mail.ru', 'ProtonMail']
        if any(title_sub in string for string in email_not_to_check):
            continue

        my_email_list.append(username)

    my_email_list.sort()

    outlook_entries = email_entries_outlook()
    outlook_existences = check_entries_outlook(outlook_entries, my_email_list)
    # print(*outlook_entries, sep='\n')

    message = "My list of emails: \n"
    for i in outlook_existences:
        email = i.split(" : ", 1)[0]  # cunha_barbosa@outlook.pt
        result = i.split(" : ", 1)[1]  # False

        if result == 'True':
            result += ' 👍 '
        if result == 'False':
            result += ' ❌ '

        message += email + " : " + result  + "\n"

    message += "Total emails: " + str(len(outlook_existences))

    print(message)
    telegram.notify_telegram(telegram_token, telegram_chat_id, message)

    benchmark.benchmark_end(initial_time, sys.argv[0])  # End benchmark and end of script
