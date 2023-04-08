FROM python:3.10.9-slim
COPY requirements.txt .
WORKDIR .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "./notify_sender.py"]