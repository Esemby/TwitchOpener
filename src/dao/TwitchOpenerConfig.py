import configparser
import imaplib
import webbrowser
from datetime import datetime

class TwitchOpenerConfig:
    def __init__(self):
        self.APP_PASS: str = None
        self.EMAIL_USER: str = None
        self.HOST: str = None
        self.LINK: str = "https://www.twitch.tv/"
        self.ERROR_RETRIES: int = None
        self.MAILBOX: str = None
        self.BROWSER = webbrowser.get()
        self.mail: imaplib.IMAP4_SSL = None
        self.next_run_time: datetime = datetime.now()
        self.failed_retries: int = 0

    def from_config(self, config_path: str) -> None:
        config = configparser.ConfigParser()
        config.read(config_path)

        self.EMAIL_USER = config['DEFAULT']['EMAIL_USER']
        self.APP_PASS = config['DEFAULT']['APP_PASS']
        self.MAILBOX = config['DEFAULT'].get('MAILBOX', 'Twitch')
        self.HOST = config['DEFAULT'].get('HOST', 'imap.gmail.com')
