FROM python:3.6-alpine

RUN adduser -D devblog

# Change default directory
WORKDIR /home/devblog

# Create virtual environment
# Upgrade PIP in virtual environment to latest version
# Install requirements
COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements/dev.txt

# OUTPUT: Build artefacts (Wheels) are output here
VOLUME /wheelhouse

# OUTPUT: Build cache
VOLUME /build

# OUTPUT: Test reports are output here
VOLUME /reports

COPY app app
COPY migrations migrations
COPY devblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP devblog.py

RUN chown -R devblog:devblog ./
USER devblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

LABEL application=devblog
