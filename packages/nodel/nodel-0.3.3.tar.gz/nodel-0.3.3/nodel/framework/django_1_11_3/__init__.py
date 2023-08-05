from nodel.framework.common import *
from dotenv import set_key
from nodel.framework import modules

HERE = os.path.dirname(os.path.abspath(__file__))


def make_project(base_dir):
	# create environment file
	env_file = os.path.join(base_dir, '.env')
	if not os.path.exists(env_file):
		open(env_file, 'a').close()
		set_key(env_file, 'ADDRESS', 'localhost')
		set_key(env_file, 'PORT', '8000')
		set_key(env_file, 'DJANGO_SETTINGS_MODULE', 'core.config.dev')
	set_key(env_file, 'SECRET_KEY', generate_key())

	# create git ignore
	create_git_ignore(base_dir)

	# create modules
	path = os.path.join(base_dir, 'modules')
	if not os.path.exists(path):
		os.mkdir(path)
	path_base = os.path.join(path, 'base.txt')
	if not os.path.exists(path_base):
		open(path_base, 'a').close()
	modules.set_module(path_base, "django", "1.11.3")
	modules.set_module(path_base, "python-dotenv", "0.6.5")
	path_dev = os.path.join(path, 'dev.txt')
	if not os.path.exists(path_dev):
		with open(path_dev, 'w') as f:
			f.write('-r base.txt')
	path_prod = os.path.join(path, 'prod.txt')
	if not os.path.exists(path_prod):
		with open(path_prod, 'w') as f:
			f.write('-r base.txt')
	modules.set_module(path_prod, "gunicorn", "19.7.1")

	# create core django files
	path = os.path.join(base_dir, 'core')
	if not os.path.exists(path):
		os.mkdir(path)

	create_init_file(path)
	create_file(path, 'manage.py', os.path.join(HERE, 'manage.py'))

	path = os.path.join(base_dir, 'core', 'core')
	if not os.path.exists(path):
		os.mkdir(path)
	create_init_file(path)
	create_file(path, 'urls.py', os.path.join(HERE, 'urls.py'))
	create_file(path, 'wsgi.py', os.path.join(HERE, 'wsgi.py'))

	path = os.path.join(base_dir, 'core', 'core', 'config')
	if not os.path.exists(path):
		os.mkdir(path)
	create_init_file(path)

	create_file(path, 'base.py', os.path.join(HERE, 'config_base.py'))
	create_file(path, 'dev.py', os.path.join(HERE, 'config_dev.py'))
	create_file(path, 'prod.py', os.path.join(HERE, 'config_prod.py'))
