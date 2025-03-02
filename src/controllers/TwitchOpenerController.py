import imaplib
import sys
import logging
from datetime import datetime, timedelta
import time
import os
import signal
import email
import pyautogui
from typing import Any, Callable, List
from dao.TwitchOpenerConfig import TwitchOpenerConfig
from controllers.TwitchWindowController import TwitchWindowController
from pynput import keyboard  # Replace the import for keyboard event handling

class TwitchOpenerController:

    def __init__(self):
        self.config = TwitchOpenerConfig()
        self.window_controller = TwitchWindowController()

    def setup(self) -> None:
        print("Running setup")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.dirname(script_dir)
        config_path = os.path.join(script_dir, 'config/config.cfg')
        print(f"Config path: {config_path}")
        self.config.from_config(config_path)

        self.config.mail = imaplib.IMAP4_SSL(self.config.HOST)
        self.config.next_run_time = datetime.now()
        
        if not self.config.EMAIL_USER:
            logging.error("EMAIL_USER environment variable is not set")
            sys.exit(1)

        if not self.config.APP_PASS:
            logging.error("APP_PASS environment variable is not set")
            sys.exit(1)

        try:
            self.config.mail.login(self.config.EMAIL_USER, self.config.APP_PASS)
        except imaplib.IMAP4.error as e:
            logging.error(f"App password login failed: {e}")
            sys.exit(1)
        
        # Register key up event for 'a' key
        listener = keyboard.Listener(on_release=self.on_key_up)
        listener.start()

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

    def on_key_up(self, key: Any) -> None:
        try:
            if key.char == 'a':
                self.window_controller.arrange_windows()
        except AttributeError:
            pass

    def graceful_shutdown(self, signum: int, frame: Any) -> None:
        logging.info("Shutting down gracefully...")
        self.config.mail.logout()
        sys.exit(0)

    # notification usually comes in at the full minute, this ensures we the most optimal time to check for new mail
    def next_minute(self) -> datetime:
        return (datetime.now() + timedelta(minutes=1)).replace(second=5, microsecond=0)

    def reconnect_mail(self, imap_ssl_instance: Callable[[], imaplib.IMAP4_SSL]) -> imaplib.IMAP4_SSL:
        print("Running reconnect_mail")
        succesful_reconnect = False
        while not succesful_reconnect:
            new_mail = imap_ssl_instance()
            try:
                self.config.mail.logout()
                new_mail.login(self.config.EMAIL_USER, self.config.APP_PASS)
                succesful_reconnect = True
            except Exception as e:
                logging.error(f"Exception during mail login: {e}")
                time.sleep(60)
            self.config.mail = new_mail
        return self.config.mail
    
    def process_unseen_emails(self, message: bytes) -> None:
        for num in message.split():
            status, msg_data = self.config.mail.fetch(num, "(RFC822)")
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
                url = self.config.LINK + first_word
                if url:
                    logging.info(f"Opening: {url}")
                    self.config.BROWSER.open_new(url)
                    time.sleep(10)
                    pyautogui.press('m')
                    pyautogui.hotkey('alt', 't')
        self.window_controller.arrange_windows()


    def check_for_unseen_emails(self, mail: imaplib.IMAP4_SSL) -> List[Any]:
        try:
            status, _ = mail.select(self.config.MAILBOX)
            if status != "OK":
                logging.error(f"Failed to select mailbox: {self.config.MAILBOX}")
                return None
        except Exception as e:
            logging.error(f"Select mail error: {e}")
            self.reconnect_mail(lambda: imaplib.IMAP4_SSL(self.config.HOST))
            return None
        try:
            status, messages = mail.search(None, "UNSEEN")
            if status != "OK":
                logging.error("Failed to search for unseen emails")
                return None
            return messages
        except Exception as e:
            logging.error(f"Search mail error: {e}")
            self.reconnect_mail(lambda: imaplib.IMAP4_SSL(self.config.HOST))
            return None

    def loop(self) -> None:
        logging.debug("Running loop")
        self.config.failed_retries = 0
        self.config.next_run_time = datetime.now()
        # just use ctrl+c to stop the script
        while True:
            if self.config.next_run_time > datetime.now():
                time.sleep(1)
                continue
            self.config.next_run_time = self.next_minute()
            logging.debug(f"Checking for new emails in: {self.config.MAILBOX}")
            try:
                messages = self.check_for_unseen_emails(self.config.mail)
                fail_counter = 0
                if not messages[0]:
                    logging.debug("No new unseen emails found")
                    continue
                self.process_unseen_emails(messages[0])
            except Exception as e:
                logging.error(f"Error: {e}")
                fail_counter += 1
                if fail_counter >= 10:
                    logging.error("Too many login retries, shutting down")
                    sys.exit(1)