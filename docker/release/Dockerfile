FROM python:3.6-alpine

RUN adduser -D devblog

WORKDIR /home/devblog

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements/prod.txt


COPY app app
COPY migrations migrations
COPY devblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP devblog.py

RUN chown -R devblog:devblog ./
USER devblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
