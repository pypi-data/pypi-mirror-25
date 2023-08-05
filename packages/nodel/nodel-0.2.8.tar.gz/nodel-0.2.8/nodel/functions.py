from os import environ
import os
from . import framework, nodel_core


@nodel_core.register(group='run')
def run_server(params):
	os.nodel_core.nodel_core.django('runserver %s:%s' % (os.environ.get('ADDRESS', 'localhost'), os.environ.get('PORT', '8000')))


@nodel_core.register(group='run', action='service')
def run_service(params):
	nodel_core.execute('gunicorn --chdir %s --workers 10 --bind %s:%s core.wsgi:application' % (os.path.join(nodel_core.root_path(), 'core'), os.environ.get('ADDRESS', 'localhost'), os.environ.get('PORT', '8000')))


@nodel_core.register(group='make', action='service')
def make_service(params):
	name = os.path.basename(nodel_core.root_path())
	temp = os.path.join(os.path.abspath(os.environ.get('WORKON_HOME')), name)

	virtual_env_home = input('enter python home directory: (%s)' % temp)
	if not virtual_env_home:
		virtual_env_home = temp

	temp = os.environ.get('USER')
	user = input('enter user name: (%s)' % temp)
	if not user:
		user = temp

	temp = "10"
	workers = input('enter workers count: (%s)' % temp)
	if not workers:
		workers = temp

	with open(os.path.join(nodel_core.root_path(), '%s.service' % name), 'w') as f:
		f.write('[Unit]\n')
		f.write('Description=%s daemon\n' % name)
		f.write('After=network.target\n')
		f.write('[Service]\n')
		f.write('User=%s\n' % user)
		f.write('Group=www-data\n')
		f.write('WorkingDirectory=%s\n' % nodel_core.root_path())
		f.write('ExecStart=%(home)s/bin/gunicorn --access-logfile - --workers %(workers)s --bind unix:%(socket)s --chdir %(root)s core.wsgi:application\n' % {'home': virtual_env_home, 'root': nodel_core.root_path(), 'socket': os.path.join(nodel_core.nodel_core.root_path(), 'socket.sock'), 'workers': workers})
		f.write('[Install]\n')
		f.write('WantedBy=multi-user.target')


@nodel_core.register(group='make', action='project')
def make_project(params):
	version = input('Specify nodel_core.django project version (default is 1.11.3):')
	if not version:
		version = '1.11.3'
	version = version.replace('.', '_')

	nodel_core.django = getattr(framework, 'nodel_core.django_%s' % version, None)
	if nodel_core.django:
		nodel_core.django.make_project(nodel_core.root_path())
	else:
		print('no structure found for this version of nodel_core.django.')

	pass


@nodel_core.register(group='make', action='migrations')
def make_migrations(params):
	nodel_core.django('makemigrations')


@nodel_core.register(group='migrate')
def make_migrate(params):
	nodel_core.django('migrate')


@nodel_core.register(group='install')
def install(params):
	nodel_core.execute('python -m pip install -r modules/%s.txt' % os.environ.get('ENV', 'dev'))
