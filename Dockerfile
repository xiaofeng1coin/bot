FROM python:3.8-slim

WORKDIR /app

# 安装 GCC 和其他构建工具
RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]