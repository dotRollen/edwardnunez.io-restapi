FROM python:3.7-alpine as base

FROM base as builder

RUN apk update \
 && apk upgrade

# Add and switch to user for application security
RUN adduser -D -g /bin/bash devblog
USER devblog

# Change default directory
WORKDIR /home/devblog

COPY --chown=devblog . /home/devblog

# Create virtual enviornment and folders for volume with user
RUN python -m venv env \
 && env/bin/pip install --upgrade pip \
 && mkdir wheelhouse build reports cache \
 && chmod +x scripts/dev.sh

# PIP environment variable (NOTE: must be set after install wheel)
ENV WHEELHOUSE=/home/devblog/wheelhouse \
    PIP_WHEEL_DIR=/home/devblog/wheelhouse \
    PIP_FIND_LINKS=/home/devblog/wheelhouse \
    XDG_CACHE_HOME=/home/devblog/cache 

# OUTPUT: Build artefacts (Wheels) are output here
VOLUME /home/devblog/wheelhouse

# OUTPUT: Build cache
VOLUME /home/devblog/build

# OUTPUT: Test reports are output here
VOLUME /home/devblog/reports

# Set defaults for entrypoint and command string
EXPOSE 5000
ENTRYPOINT ["./scripts/dev.sh"]