import os
import logging
from controllers.TwitchOpenerController import TwitchOpenerController


def main():
    log_file_path = os.path.join(os.path.dirname(__file__), 'TwitchOpener.log')
    logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    logging.info("Application started")
    twitchOpenerController = TwitchOpenerController()
    twitchOpenerController.setup()
    twitchOpenerController.loop()

if __name__ == "__main__":
    main()
