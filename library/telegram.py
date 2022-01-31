"""
Library to access the Telegram platform

Author: Antonio Barbosa
E-mail: cunha.barbosa@gmail.com
Version: 2022-01-31
"""
import telegram


# https://medium.com/@mycodingblog/get-telegram-notification-when-python-script-finishes-running-a54f12822cdc

def notify_telegram(token: str, chat_id: str, telegram_message: str) -> None:
    """
    Send message via Telegram
    :param str token: Authentication token for sending messages
    :param str chat_id: Destination id
    :param str telegram_message: Message to be sent
    :exception notify_telegram_error: Not possible to send message
    """

    print("Notify by telegram: ", end='')
    try:
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id, text=telegram_message)
        print("ok!")
    except Exception as notify_telegram_error:
        print("not ok...")
        print(notify_telegram_error)

if __name__ == '__main__':
    print("Telegram test")

    # my_token = "asd"
    # my_chat_id = "asd"
    # my_message = "It's a test!"
    # notify_telegram(my_token, my_chat_id, my_message)

