FROM python:3.10.9-slim
COPY requirements.txt /opt/notify-bot
WORKDIR /opt/notify-bot
RUN pip install -r requirements.txt
COPY . /opt/notify-bot
CMD ["python", "./notify_sender.py"]