import logging
import os
import sys
import time
import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client
from telethon import TelegramClient
from config import *

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
    
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    LOAD = os.environ.get("LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "worldwide_friend_zone")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    BOT_TOKEN = os.environ.get("TOKEN", None)
    WORKERS = int(os.environ.get("WORKERS", 8))

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "2145093972").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

else:

    API_ID = config.API_ID
    API_HASH = config.API_HASH
    ALLOW_CHATS = config.ALLOW_CHATS
    ALLOW_EXCL = config.ALLOW_EXCL
    DB_URI = config.DATABASE_URL
    DEL_CMDS = config.DEL_CMDS
    EVENT_LOGS = config.LOGGER_ID
    LOAD = config.LOAD
    MONGO_DB_URI = config.MONGO_DB_URI
    NO_LOAD = config.NO_LOAD
    STRICT_GBAN = config.STRICT_GBAN
    SUPPORT_CHAT = config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = config.TEMP_DOWNLOAD_DIRECTORY
    BOT_TOKEN = config.TOKEN
    WORKERS = config.WORKERS

    try:
        OWNER_ID = int(config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in config.BL_CHATS or [])
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in config.DEMONS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in config.TIGERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in config.WOLVES or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")


DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)


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
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from VIP_INNOCENT.utils.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
