from pathlib import Path
import json
import os

# Define local directories to be used for storage.
# Abstract this away from the relevant download files.
CURRENT_DIR=Path(__file__).resolve().parent
PROJECT_ROOT=CURRENT_DIR
DOWNLOAD_DIR=PROJECT_ROOT / 'data'
