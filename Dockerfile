FROM python:3.8-slim

WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y gcc

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制脚本文件
COPY bot.py .

# 创建会话文件目录
RUN mkdir -p /app/sessions

# 设置会话文件路径
ENV SESSION_FILE=/app/sessions/session_name

CMD ["python", "bot.py"]