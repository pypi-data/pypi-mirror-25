from django.core.wsgi import get_wsgi_application
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.%s' % os.environ.get('ENV', 'dev'))

application = get_wsgi_application()
