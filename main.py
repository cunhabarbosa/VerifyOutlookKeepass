"""
Check if all my email accounts in the Keepass file are configured in Microsoft Outlook and send the result via Telegram

Author: Antonio Barbosa
E-mail: cunha.barbosa@gmail.com
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
keepass_ignore_list = list(config_object['KEEPASS_FILE']['IGNORE_LIST'].split(','))

# Telegram info
telegram_token = config_object['TELEGRAM_INFO']['telegram_token']
telegram_chat_id = config_object['TELEGRAM_INFO']['telegram_chat_id']


def load_database(dir_name: str, base_filename: str, pass_filename: str) -> PyKeePass:
    """
    Load database from Keepass file
    :param str dir_name: Directory where the file is located
    :param str base_filename: Name of file (must include filename extension)
    :param str pass_filename: Password
    :return: Link to Keepass file
    :rtype: pykeepass.pykeepass.PyKeePass
    """
    # @todo: Set default values and validate input arguments
    # @todo: Implement try-except

    # pass_filename = "asd"
    try:
        filename = os.path.join(dir_name, base_filename)
        print(filename)

        kp = PyKeePass(filename, password=pass_filename)
    except Exception as error_load_database:
        raise error_load_database

    return kp


def find_group(kp_db: PyKeePass = None, name_db: str ='email', first_db: bool =True) -> PyKeePass.groups:
    """
    Search for a group by its name
    :param PyKeePass kp_db: Link to Keepass file
    :param str name_db: Name of group
    :param bool first_db: Returns the first result or all results
    :return: Link to a specific group
    :rtype: pykeepass.group.Group
    """
    if kp_db is None:
        raise "Database not defined"
    # @todo: Validate input arguments
    # @todo: Implement try-except

    try:
        kp_group = kp_db.find_groups(name=name_db, first=first_db)
    except Exception as error_find_group:
        raise error_find_group

    return kp_group


def find_entries(kp_group: PyKeePass.groups = None) -> list[PyKeePass.groups]:
    """
    Get the entries in a group, like this:
    Entry: "AntonioB/email/Gmail - username1 (username1@gmail.com)"
    Entry: "AntonioB/email/Gmail - username2 (username2@gmail.com)"
    Entry: "AntonioB/email/Gmail - username3 (username3@gmail.com)"
    :param PyKeePass.groups kp_group: Name of group
    :return: List of existing entries
    :rtype: list[PyKeePass.groups]
    """
    if kp_group is None:
        raise "Group not defined"

    try:
        kp_entries = group.entries
    except Exception as error_find_entries:
        raise error_find_entries
    # print(*entries, sep = "\n")   # Print all entries
    return kp_entries


def email_entries_outlook() -> list[object]:
    """
    Get from the Microsoft Outlook program the list of emails that are configured
    :return: Configured email list
    :rtype: list[object]
    """
    email_list = []
    try:
        outlook = win32com.client.Dispatch('outlook.application')
        mapi = outlook.GetNamespace("MAPI")

        for account in mapi.Accounts:
            email_account: object = account.DeliveryStore.DisplayName
            # print(email_account)
            email_list.append(email_account)
    except Exception as error_email_entries_outlook:
        raise error_email_entries_outlook

    return email_list


def check_entries_outlook(list_outlook: list[object], list_keepass: list[str]) -> list[str]:
    """
    Checks if list_keepass exists in list_outlook
    :param list[object] list_outlook: List of emails configured in Microsoft Outlook
    :param list[str] list_keepass: List of existing emails in Keepass file
    :return Keepass list with results
    :rtype: list[str]
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

    # --- Read the existing entries in the Keepass file ---
    entries=[]
    try:
        database = load_database(keepass_directory, keepass_filename, keepass_password)
        group = find_group(database, keepass_group)
        entries = find_entries(group)
    except Exception as error:
        print(error)

    my_email_list = []
    for entry in entries:
        # Entry: "AntonioB/email/Gmail - username (username@gmail.com)"
        # Title: "Gmail - username"
        # Username: "username@gmail.com"
        title = entry.title  # Gmail - username
        title_sub = title.split(" - ", 1)[0]  # Gmail
        username = entry.username
        try:
            title_user = title.split(" - ", 1)[1]  # username
        except (Exception,):
            pass

        # If the entry is in ignore list, move on to the next
        email_not_to_check = keepass_ignore_list
        if any(title_sub in string for string in email_not_to_check):
            continue

        my_email_list.append(username)

    my_email_list.sort()

    # --- Scan emails configured in Microsoft Outlook ---
    outlook_existences = ()
    try:
        outlook_entries = email_entries_outlook()
        outlook_existences = check_entries_outlook(outlook_entries, my_email_list)
        # print(*outlook_entries, sep='\n')
    except Exception as e:
        print(e)
        exit(-1)

    # --- Compare both lists ---
    message = "My list of emails: \n"
    for i in outlook_existences:
        email = i.split(" : ", 1)[0]  # username@gmail.com
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
