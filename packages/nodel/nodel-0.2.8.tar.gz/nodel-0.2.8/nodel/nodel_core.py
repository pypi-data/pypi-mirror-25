import sys
import os
from dotenv import load_dotenv

from . import framework

functions = {}


def register(group=None, action=None, description=None):
	def decorator(view_func):
		if not group in functions:
			functions[group] = {}
		if action:
			functions[group][action] = {"description": description, "function": view_func}
		else:
			functions[group]['default'] = {"description": description, "function": view_func}
		return view_func

	return decorator


def django(params):
	os.system("python ./core/manage.py " + params)


def execute(command):
	os.system(command)


def method_not_found(method):
	print("method not found: %s" % method)


from .functions import *


def root_path():
	return os.path.dirname(os.path.abspath(sys.argv[0]))


def run():
	args = sys.argv

	dotenv_path = os.path.join(root_path(), '.env')
	load_dotenv(dotenv_path)

	if len(args) > 1:
		method = args[1].split(':')

		if method[0] in functions:
			if len(method) > 1:
				if method[1] in functions[method[0]]:
					functions[method[0]][method[1]]['function'](args[2:])
				else:
					method_not_found(args[1])
			else:
				functions[method[0]]['default']['function'](args[2:])
		else:
			method_not_found(args[1])
