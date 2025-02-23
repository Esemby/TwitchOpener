import imaplib
import ssl
import sys
import logging
from datetime import datetime, timedelta
import time
import webbrowser
import configparser
import os
import signal
import email
import pyautogui

class TwitchOpenerController:
    def __init__(self):
        self.APP_PASS = None
        self.BROWSER = webbrowser.get()
        self.EMAIL_USER = None
        self.HOST = None
        self.LINK = "https://www.twitch.tv/"
        self.ERROR_RETRIES = None
        self.LOG_FILE_PATH = None
        self.MAILBOX = None
        self.mail = None
        self.next_run_time = None

    def setup(self):
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.cfg')
        config.read(config_path)

        self.EMAIL_USER = config['DEFAULT']['EMAIL_USER']
        self.APP_PASS = config['DEFAULT']['APP_PASS']
        self.LOG_FILE_PATH = config['DEFAULT']['LOG_FILE_PATH']
        self.MAILBOX = config['DEFAULT'].get('MAILBOX', 'Twitch')
        self.HOST = config['DEFAULT'].get('HOST', 'imap.gmail.com')
        self.ERROR_RETRIES = int(config['DEFAULT'].get('ERROR_RETRIES', 10))

        self.mail = imaplib.IMAP4_SSL(self.HOST)
        self.next_run_time = datetime.now()
        # Setup logging
        logging.basicConfig(
            filename=self.LOG_FILE_PATH,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        # Ensure EMAIL_USER is set
        if not self.EMAIL_USER:
            email_user_error_string = "EMAIL_USER environment variable is not set"
            logging.error(email_user_error_string)
            print(email_user_error_string)
            sys.exit(1)

        # Ensure APP_PASS is set
        if not self.APP_PASS:
            app_pass_error_string = "APP_PASS environment variable is not set"
            logging.error(app_pass_error_string)
            print(app_pass_error_string)
            sys.exit(1)

        try:
            self.mail.login(self.EMAIL_USER, self.APP_PASS)
        except imaplib.IMAP4.error as e:
            logging.error(f"App password login failed: {e}")
            sys.exit(1)

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

    def graceful_shutdown(self, signum, frame):
        logging.info("Shutting down gracefully...")
        self.mail.logout()
        sys.exit(0)

    # notification usually comes in at the full minute, this ensures we the most optimal time to check for new mail
    def next_minute(self) -> datetime:
        return (datetime.now() + timedelta(minutes=1)).replace(second=5, microsecond=0)

    def reconnect_mail(self) -> imaplib.IMAP4_SSL:
        succesful_reconnect = False
        self.mail.logout()
        while not succesful_reconnect:
            new_mail = imaplib.IMAP4_SSL(self.HOST)
            try:
                new_mail.login(self.EMAIL_USER, self.APP_PASS)
                succesful_reconnect = True
            except imaplib.IMAP4.error as e:
                logging.error(f"Re-login failed: {e}")
                time.sleep(60)
            self.mail = new_mail
            return self.mail
    

    def process_unseen_emails(self, message: bytes) -> None:
        for num in message.split():
            status, msg_data = self.mail.fetch(num, "(RFC822)")
            if status != "OK":
                logging.error(f"Failed to fetch email: {num}")
                continue
            for response_part in msg_data:
                if not isinstance(response_part, tuple):
                    continue
                msg = email.message_from_bytes(response_part[1])
                subject = msg["subject"]
                if not subject:
                    continue
                first_word = subject.split()[0]
                if first_word.startswith("=?UTF-8?Q?"):
                    first_word = first_word[10:].split('_')[0]
                url = self.LINK + first_word
                if url:
                    logging.info(f"Opening: {url}")
                    self.BROWSER.open_new(url)
                    time.sleep(10)
                    pyautogui.press('m')


    def loop(self):
        fail_counter = 0
        # just use ctrl+c to stop the script
        while True:
            try:
                if datetime.now() < self.next_run_time:
                    time.sleep(1)
                    continue

                logging.debug(f"Checking for new emails in: {self.MAILBOX}")
                self.next_run_time = self.next_minute()
                try:
                    status, _ = self.mail.select(self.MAILBOX)
                    if status != "OK":
                        logging.error(f"Failed to select mailbox: {self.MAILBOX}")
                        continue

                    status, messages = self.mail.search(None, "UNSEEN")
                    if status != "OK":
                        logging.error("Failed to search for unseen emails")
                        continue
                except (imaplib.IMAP4.abort, ssl.SSLError) as e:
                    logging.error(f"IMAP/SSL error: {e}")
                    self.reconnect_mail()
                    continue
                fail_counter = 0
                if not messages[0]:
                    logging.debug("No new unseen emails found")
                    continue
                self.process_unseen_emails(messages[0])
            except Exception as e:
                logging.error(f"Error: {e}")
                fail_counter += 1
                if fail_counter >= self.ERROR_RETRIES:
                    logging.error("Too many login retries, shutting down")
                    sys.exit(1)
                time.sleep(60)