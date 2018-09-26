#!/bin/sh

# Download requirements to build cache
env/bin/pip download -d build/ -r requirements/dev.txt --no-input

# Install application test requirements
env/bin/pip  install --no-index -f build/ -r requirements/dev.txt

# Run test.sh arguments
exec $@