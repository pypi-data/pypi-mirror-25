#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(dotenv_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.%s' % os.environ.get('ENV', 'dev'))

    execute_from_command_line(sys.argv)
