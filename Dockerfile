FROM python:3.8-alpine

WORKDIR '/app'

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN pytest

CMD [ "flask", "--app", "main", "run", "--host=0.0.0.0"]
