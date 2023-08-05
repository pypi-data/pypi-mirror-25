import os

import random
import string


def create_init_file(base_dir):
	open(os.path.join(base_dir, '__init__.py'), 'a').close()


def create_file(base_dir, name, other):
	with open(os.path.join(base_dir, name), 'w') as f:
		with open(other) as o:
			f.write(o.read())


def create_git_ignore(base_dir):
	path = os.path.join(base_dir, '.gitignore')
	if not os.path.exists(path):
		with open(path, 'w') as f:
			f.write(
				"*.py[co]\n*.egg*\nbuild\ncache\n.script\nconfig.json\n*.db\n*.log\n.project\n.pydevproject\n.settings\n*~\n\#*\#\n/.emacs.desktop\n/.emacs.desktop.lock\n.elc\nauto-save-list\ntramp\n.\#*\n*.swp\n*.swo\n.DS_Store\n._*\nThumbs.db\nDesktop.ini\n.idea\nnode_modules\n.env\nstatic")
		pass


def generate_key():
	return ''.join([random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, "!#$%&'()*+,-./:;<>?@[]^_{|}~")) for i in range(50)])
