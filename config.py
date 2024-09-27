import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN = os.environ.get('ADMIN')
GROUP_CHAT_ID = os.environ.get('GROUP_CHAT_ID')
