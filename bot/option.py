import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')