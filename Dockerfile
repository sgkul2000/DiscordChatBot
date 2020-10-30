FROM python:3.7-alpine

WORKDIR usr/src/app

COPY . .
# COPY requirements.txt .

RUN pip install -r requirements.txt


EXPOSE 3000

CMD ["python", "main.py"]