# Scripts

This directory contains the changelog and release notes generation tools.

## Main Script

The primary script to be executed is `generate-notes.sh`.

### Usage

This script is designed to be run from the root of a Git repository. It can be in this directory, or you can call it via its full path from another repository.

```bash
# Example: Running from the root of another project
/path/to/release-notes/scripts/generate-notes.sh
```

For a full list of all available commands and flags, please see the main `README.md` in the root of this project.

## Core Logic

The core logic is contained in the `notes_generator.py` Python script. The `generate-notes.sh` script is a simple, portable wrapper that executes this Python script. All command-line arguments are passed directly to the Python script.
