import threading
import os
from telebot import TeleBot 

class Notifier:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Notifier, cls).__new__(cls)
        return cls._instance

    def __init__(self, token: str = None, chat_id: int = None):
        if getattr(self, "_initialized", False):
            return
        if token is None:
            token = os.getenv("TELEGRAMTOKEN")
        if chat_id is None:
            chat_id = 6427739134
        self.token = token
        self.chat_id = chat_id
        self.bot = TeleBot(token=self.token)
        self._initialized = True

    def send_notification(self, text: str):
        if not self.chat_id or not self.token:
            raise RuntimeError("Notifier not configured: no chat_id or token.")
        try:
            self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to send notification: {e}")

# def notify(text: str):
#     notifier = NotifierSingleton()
#     notifier.send_notification(text)
