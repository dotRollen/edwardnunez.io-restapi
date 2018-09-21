FROM python:3.7-alpine

# Add and switch to user for application security
RUN adduser -D -g /bin/bash devblog
USER devblog

# Change default directory
WORKDIR /home/devblog

COPY --chown=devblog wheels /wheelhouse

RUN python -m venv env \
 && . env/bin/activate \
 && pip install --no-index -f /wheelhouse devblog \
 && chmod +x scripts/boot.sh

# Set defaults for entrypoint and command string
EXPOSE 5000
ENTRYPOINT ["./dev.sh"]