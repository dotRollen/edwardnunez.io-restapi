#!/bin/sh

# Download requirements to build cache
env/bin/pip download -d build-py/ -r requirements/dev.txt --no-input

# Install application test requirements
env/bin/pip  install --no-index -f build-py/ -r requirements/dev.txt

# Run test.sh arguments
exec $@