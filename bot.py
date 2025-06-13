import asyncio
from telethon import TelegramClient, events
import os
import logging

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
TARGET_CHAT_ID = int(os.environ.get('TARGET_CHAT_ID'))

# 创建 Telegram 客户端
client = TelegramClient('session_name', API_ID, API_HASH)


@client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):
    # 获取消息文本
    message_text = event.message.text
    if not message_text:
        logger.info("收到非文本消息，跳过复制")
        return

    try:
        # 复制消息到目标群组
        await client.send_message(TARGET_CHAT_ID, message_text)
        logger.info(f"消息已复制并发送到目标群组: {message_text}")
    except Exception as e:
        logger.error(f"发送消息出错: {e}")


async def main():
    await client.start()
    logger.info("监控已启动")
    await client.run_until_disconnected()

# 运行主函数
with client:
    client.loop.run_until_complete(main())