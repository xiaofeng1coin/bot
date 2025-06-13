import logging
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

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
YOUR_BOT_TOKEN = os.environ.get('YOUR_BOT_TOKEN')
TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID')
FORWARDED_CHATS = os.environ.get('FORWARDED_CHATS', '').split(',')  # 默认为空列表
MESSAGE_LIMIT = int(os.environ.get('MESSAGE_LIMIT', 10))  # 默认每分钟 10 条消息
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

# 消息频率控制
message_counts = {}

def forward_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id
    user_id = update.effective_user.id

    # 检查是否来自要监控的聊天
    if str(chat_id) not in FORWARDED_CHATS:
        logger.info(f"收到消息来自未监控的群组: {chat_id}")
        return

    try:
        # 获取消息文本
        text = update.effective_message.text
        if not text:
            logger.info(f"收到非文本消息，跳过转发")
            return

        # 消息频率控制
        current_time = time.localtime()
        key = f"{user_id}-{current_time.tm_min}"
        if key in message_counts:
            message_counts[key] += 1
            if message_counts[key] > MESSAGE_LIMIT:
                logger.warning(f"用户 {user_id} 在 1 分钟内发送了超过 {MESSAGE_LIMIT} 条消息")
                if ADMIN_CHAT_ID:
                    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"用户 {user_id} 在 1 分钟内发送了超过 {MESSAGE_LIMIT} 条消息。")
                return
        else:
            message_counts[key] = 1

        # 转发消息
        context.bot.forward_message(chat_id=TARGET_CHAT_ID, from_chat_id=chat_id, message_id=message_id)
        logger.info(f"成功转发消息: 来自群组 {chat_id}，消息 ID {message_id}")

    except Exception as e:
        logger.error(f"转发消息出错: {e}")
        if ADMIN_CHAT_ID:
            try:
                context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"转发消息出错: {e}")
            except Exception as e:
                logger.error(f"发送错误通知出错: {e}")

def error_handler(update: Update, context: CallbackContext):
    logger.error(f"更新 {update} 引发错误 {context.error}")
    try:
        if ADMIN_CHAT_ID:
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"更新 {update} 引发错误 {context.error}")
    except Exception as e:
        logger.error(f"发送错误通知出错: {e}")

def main():
    if not YOUR_BOT_TOKEN or not TARGET_CHAT_ID or not FORWARDED_CHATS:
        logger.error("缺少必要的环境变量配置！")
        return

    updater = Updater(YOUR_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))
    dp.add_error_handler(error_handler)
    updater.start_polling()
    logger.info("机器人已启动，开始监听消息")
    updater.idle()

if __name__ == '__main__':
    main()