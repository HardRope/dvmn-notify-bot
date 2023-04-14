FROM python:3.10.9-slim
COPY requirements.txt /opt/dvmn-bot/requirements.txt
WORKDIR /opt/dvmn-bot/
RUN pip install -r requirements.txt
COPY . /opt/dvmn-bot/
CMD ["python", "./notify_sender.py"]