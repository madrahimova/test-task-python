FROM python:3.9-alpine3.15

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update && apk upgrade
RUN apk add --no-cache sqlite
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 12345
CMD [ "python3", "server.py" ]