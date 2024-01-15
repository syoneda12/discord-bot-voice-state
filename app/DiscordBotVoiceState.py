# DiscordBot.py
import discord
import os
import logging
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# log フォルダのパスを設定
log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')

# log フォルダが存在しない場合は作成
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# ロガーの設定
logger = logging.getLogger("DiscordBotVoiceState")
logger.setLevel(logging.DEBUG)

# ファイルハンドラの設定
file_handler = logging.FileHandler(os.path.join(log_folder, "DiscordBotVoiceState.log"))
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("log start.")

# .envファイルを読み込む
load_dotenv()  

# BOTトークン
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    logger.error("Token not found. Please check the .env file.")
# テキストチャンネル - ボイスチャンネル通知
TEXT_CHANNEL_VOICE_CHANNEL_NOTIFICATION = int(os.getenv("TEXT_CHANNEL_VOICE_CHANNEL_NOTIFICATION"))
if not TEXT_CHANNEL_VOICE_CHANNEL_NOTIFICATION:
    logger.error("TEXT_CHANNEL_VOICE_CHANNEL_NOTIFICATION not found. Please check the .env file.")
# ボイスチャンネル - Gaming
VOICE_CHANNEL_GAMING = int(os.getenv("VOICE_CHANNEL_GAMING"))
if not VOICE_CHANNEL_GAMING:
    logger.error("VOICE_CHANNEL_GAMING not found. Please check the .env file.")
# ボイスチャンネル - 一般(ロビー)
VOICE_CHANNEL_ROBY = int(os.getenv("VOICE_CHANNEL_ROBY"))
if not VOICE_CHANNEL_ROBY:
    logger.error("VOICE_CHANNEL_ROBY not found. Please check the .env file.")
# LINEトークン
LINE_TOKEN = os.getenv("LINE_TOKEN")
if not LINE_TOKEN:
    logger.error("LINE_TOKEN not found. Please check the .env file.")

# LINEへ通知
def send_line_msg(msg):
    acc_token = LINE_TOKEN
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + acc_token}
    payload = {'message': msg}
    requests.post(url, headers=headers, params=payload)

intents = discord.Intents.all()
intents.presences = True 
intents.members = True 
client = discord.Client(intents=intents)


# client = discord.Client()
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
 
# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after): 
    try:
        # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
        if before.channel != after.channel:
            now = datetime.utcnow() + timedelta(hours=9)
            # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
            botRoom = client.get_channel(TEXT_CHANNEL_VOICE_CHANNEL_NOTIFICATION)
            # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
            announceChannelIds = [VOICE_CHANNEL_ROBY, VOICE_CHANNEL_ROBY] 
            # 退室通知
            if before.channel is not None and before.channel.id in announceChannelIds:
                await botRoom.send('▲**' + member.display_name  + '** が `' + before.channel.name + '` から退出しました。 (' + f'{now:%m/%d %H:%M:%S})')
            # 入室通知
            if after.channel is not None and after.channel.id in announceChannelIds:
                await botRoom.send('▼**' + member.display_name  + '** が `' + after.channel.name + '` に参加しました。 (' + f'{now:%m/%d %H:%M:%S})')
                send_line_msg(member.display_name  + 'が' + after.channel.name + 'に参加しました。')
    except Exception as e:
        logger.error(f"Error in on_voice_state_update: {e}")

# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run(DISCORD_BOT_TOKEN)