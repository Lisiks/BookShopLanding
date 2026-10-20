FROM python:3.14-slim

WORKDIR /backend_app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .


CMD ["python3", "main.py"]