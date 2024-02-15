import logging
from colorama import Fore, Back, Style


eLG = logging.getLogger(__name__)

class LoggerHelper:
    logging.basicConfig(
        format='%(levelname)s %(asctime)s [%(name)s]: %(message)s',
        datefmt='%b %d %H:%M:%S',
        handlers=[logging.NullHandler()]
    )

    def __init__(self):
        self.logger = self.create_logger()

    def create_logger(self, name: str = __name__, severity: str = 'info') -> logging.Logger:
        logging.root.disabled = True
        logger = logging.getLogger(name)
        match severity.lower():
            case 'debug':
                logger.setLevel(logging.DEBUG)
                formatter = logging.Formatter(Fore.BLUE + Style.DIM + '%(levelname)s %(asctime)s [%(name)s]: %(message)s')
            case 'info':
                logger.setLevel(logging.INFO)
                formatter = logging.Formatter('%(levelname)s %(asctime)s [%(name)s]: %(message)s')
            case 'warn' | 'warning':
                logger.setLevel(logging.WARNING)
                formatter = logging.Formatter(Back.YELLOW + '%(levelname)s %(asctime)s [%(name)s]: %(message)s')
            case 'error':
                logger.setLevel(logging.ERROR)
                formatter = logging.Formatter(format=Fore.RED + '%(levelname)s %(asctime)s [%(name)s]: %(message)s')
            case 'critical':
                logger.setLevel(logging.CRITICAL+1)
                formatter = logging.Formatter(Fore.RED + Style.BRIGHT + '%(levelname)s %(asctime)s [%(name)s]: %(message)s')
            case _:
                eLG.exception(f"Severity must be one of debug, info, warn, error or critical, not {severity}. Defaulting to 'INFO'")
                logger.setLevel(logging.INFO)
                formatter = logging.Formatter('%(levelname)s %(asctime)s [%(name)s]: %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        return logger


if __name__ == '__main__':
    # To check if the root logger is enabled
    if logging.root.isEnabledFor(logging.INFO) and logging.root.isEnabledFor(logging.DEBUG):
        print("Root logger is enabled for INFO and DEBUG levels.")
    else:
        print("Root logger is disabled or not enabled for INFO level.")
