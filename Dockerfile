FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]