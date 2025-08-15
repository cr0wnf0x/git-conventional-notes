#!/bin/bash

# This script is a wrapper around the robust Python script for generating release notes.
# It passes all command-line arguments directly to the Python script.

# Find the directory where the script is located
SCRIPT_DIR=$(dirname "$0")

# Execute the Python script, passing along all arguments
python3 "${SCRIPT_DIR}/notes_generator.py" "$@"
