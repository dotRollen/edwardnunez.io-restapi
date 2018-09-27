FROM python:3.7-alpine

# Add and switch to user for application security
RUN adduser -D -g /bin/bash backend
USER backend

# Change default directory
WORKDIR /home/backend

COPY --chown=backend wheels /wheelhouse

RUN python -m venv env \
 && . env/bin/activate \
 && pip install --no-index -f /wheelhouse backend \
 && chmod +x scripts/boot.sh

# Set defaults for entrypoint and command string
EXPOSE 5000
ENTRYPOINT ["./dev.sh"]