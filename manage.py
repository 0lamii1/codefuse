#!/usr/bin/env python
import os
import sys

def main():
    # Load DEBUG_SECRET safely from env without importing settings prematurely
    from config.env import DEBUG_SECRET  

    if DEBUG_SECRET:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
