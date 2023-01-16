FROM python:3.10.9-slim
WORKDIR .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "./notify_sender.py"]