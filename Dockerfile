FROM python:3.12.9-slim

WORKDIR /model-service

COPY requirements.txt .
RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt

COPY model-service/ .
RUN python download_models.py

EXPOSE 3000

CMD ["python", "app.py"]