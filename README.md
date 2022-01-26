# VerifyOutlookKeepass

Check if all my email accounts in the Keepass file are configured in Microsoft Outlook and send the result via Telegram

## Algorithm
- Open KeePass file in Documents folder
- Get the list of emails saved in group **email**
- Remove emails that can't be configured in Microsoft Outlook, like:
  - Clix
  - FEUP
  - Google Account
  - Google Apps
  - Live ID
  - Microsoft Account
  - Office 365
  - Deleted accounts
- Check if each Outlook entry exists in email list
  - If **Yes**: set a value _True_
  - If **No**: set a value _False_
- Send results by Telegram

### Extras
* Benchmark

## Installation
Recommended use the Miniconda environment.

```sh
conda create -n VerifyOutlookKeepass python=3.10 -y
conda activate VerifyOutlookKeepass
```

Install the necessary packages
```sh
pip install pykeepass python-telegram-bot pypiwin32
```

Verify installation
```sh
python \library\verify_installation.py
```

Error:
```sh
The following modules caused an error:
Version installed : pykeepass 4.0.0
Version required  : pykeepass==4.0.1
```

OK:
```sh
All project dependencies were correctly installed!
```


## Usage

### Settings.ini
Using file **settings_example.ini** create a new file with the name **settings.ini** and update accordingly.


## Author
Antonio Barbosa – cunha.barbosa@gmail.com


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
