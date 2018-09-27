FROM python:3.7-alpine as base

FROM base as builder

RUN apk update \
 && apk upgrade

# Add and switch to user for application security
RUN adduser -D -g /bin/bash backend
USER backend

# Change default directory
WORKDIR /home/backend

COPY --chown=backend . /home/backend

# Create virtual enviornment and folders for volume with user
RUN python -m venv env \
 && env/bin/pip install --upgrade pip \
 && mkdir wheelhouse build reports cache \
 && chmod +x scripts/dev.sh

# PIP environment variable (NOTE: must be set after install wheel)
ENV WHEELHOUSE=/home/backend/wheelhouse \
    PIP_WHEEL_DIR=/home/backend/wheelhouse \
    PIP_FIND_LINKS=/home/backend/wheelhouse \
    XDG_CACHE_HOME=/home/backend/cache 

# OUTPUT: Build artefacts (Wheels) are output here
VOLUME /home/backend/wheelhouse

# OUTPUT: Build cache
VOLUME /home/backend/build

# OUTPUT: Test reports are output here
VOLUME /home/backend/reports

# Set defaults for entrypoint and command string
EXPOSE 5000
ENTRYPOINT ["./scripts/dev.sh"]