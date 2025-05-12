import logging
import os
import sys
import time
import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client
from telethon import TelegramClient

StartTime = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:

    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", None)
    DB_URI = os.environ.get("DATABASE_URL")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

else:
    from config import *

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    DB_URI = Config.DATABASE_URL
    MONGO_DB_URI = Config.MONGO_DB_URI
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    BOT_TOKEN = Config.BOT_TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

DRAGONS.add(OWNER_ID)

updater = tg.Updater(BOT_TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("VIP_INNOCENT", API_ID, API_HASH)

pbot = Client("VIP_INNOCENT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,in_memory=True)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

DRAGONS = list(DRAGONS) + list(DEV_USERS) 
