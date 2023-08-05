import os

# Directories
APP_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOG_ROOT = os.path.join(APP_ROOT, "logs")
CONFIG_ROOT = os.path.join(APP_ROOT, "config")
ENTITIES_ROOT = os.path.join(CONFIG_ROOT, "entities")
RULES_ROOT = os.path.join(CONFIG_ROOT, "rules")

# Files
CONFIG_FILE = os.path.join(CONFIG_ROOT, "config.yml")
REQUIREMENTS_FILE = os.path.join(APP_ROOT, "requirements.txt")

# Exit codes
CLEAN_EXIT_ERROR_CODE = 0
GENERAL_ERROR_CODE = 1
MANUAL_EXIT_ERROR_CODE = 130
MANUAL_RESTART_ERROR_CODE = 131

