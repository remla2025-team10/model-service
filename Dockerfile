FROM python:3.12.9-slim

WORKDIR /model-service

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model-service/ .
CMD ["python", "app.py"]