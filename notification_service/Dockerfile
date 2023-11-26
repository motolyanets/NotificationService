FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py makemigrations

EXPOSE 8000
