#!/bin/bash

# Change working directory to the path this script resides in (VMRE root)
cd "$(dirname "$0")"

# Run vmre-receiver.py only if the lockfile isn't present
flock -n vmre-receiver.lockfile ./vmre-receiver.py

