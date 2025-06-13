import asyncio
from telethon import TelegramClient, events
import os
import logging
from telegram.bot import Bot

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()  # 确保日志输出到标准输出
    ]
)
logger = logging.getLogger(__name__)

# 从环境变量读取配置
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SOURCE_CHAT_IDS = list(map(int, os.environ.get('SOURCE_CHAT_IDS', '').split(',')))  # 默认为空列表
TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# 创建 Telegram 客户端
user_client = TelegramClient('session_name', API_ID, API_HASH)

# 创建机器人客户端
bot = Bot(BOT_TOKEN)

@user_client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):
    # 获取消息文本
    message_text = event.message.text
    if not message_text:
        logger.info("收到非文本消息，跳过复制")
        return

    try:
        # 使用机器人发送消息到目标群组
        await bot.send_message(TARGET_CHAT_ID, message_text)
        logger.info(f"消息已通过机器人发送到目标群组: {message_text}")
    except Exception as e:
        logger.error(f"发送消息出错: {e}")

async def main():
    await user_client.start()
    logger.info("监控已启动")
    await user_client.run_until_disconnected()

if __name__ == "__main__":
    with user_client:
        user_client.loop.run_until_complete(main())