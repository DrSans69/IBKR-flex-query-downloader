import logging
import logging.handlers
import os
import tkinter as tk

from src.config import LOG_BACKUPS, LOG_DIR, LOG_FILENAME, LOG_SIZE

logger_main = logging.getLogger("main")

simple_formater = logging.Formatter(
    '%(levelname)-8s | %(name)s | %(message)s'
)
detailed_formater = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(simple_formater)

    log_path = os.path.join(LOG_DIR, LOG_FILENAME)
    os.makedirs(LOG_DIR, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=LOG_SIZE,
        backupCount=LOG_BACKUPS,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formater)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)


class TkinterHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

        self.text_widget.configure(state='disabled')
        self.setLevel(logging.INFO)
        self.setFormatter(simple_formater)
        logger_main.addHandler(self)

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)

        self.text_widget.after(0, append)
