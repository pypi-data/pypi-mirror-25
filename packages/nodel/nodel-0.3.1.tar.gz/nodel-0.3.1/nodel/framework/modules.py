import os
import re
import codecs
from collections import OrderedDict

__escape_decoder = codecs.getdecoder('unicode_escape')
__posix_variable = re.compile('\$\{[^\}]*\}')


def decode_escaped(escaped):
	return __escape_decoder(escaped)[0]


def parse_module(module_path):
	with open(module_path) as f:
		for line in f:
			line = line.strip()

			if line.startswith('-r'):
				yield line, ''
			if not line or line.startswith('#') or line.startswith('-') or '==' not in line:
				continue

			k, v = line.split('==', 1)
			k, v = k.strip(), v.strip().encode('unicode-escape').decode('ascii')

			if len(v) > 0:
				quoted = v[0] == v[len(v) - 1] in ['"', "'"]

				if quoted:
					v = decode_escaped(v[1:-1])

			yield k, v


def module_values(module_path):
	values = OrderedDict(parse_module(module_path))
	return values


def set_module(module_path, module_to_set, version_to_set):
	module_to_set = str(module_to_set)
	version_to_set = str(version_to_set)
	if not os.path.exists(module_path):
		return None, module_to_set, version_to_set
	dotenv_as_dict = OrderedDict(parse_module(module_path))
	dotenv_as_dict[module_to_set] = version_to_set
	success = flatten_and_write(module_path, dotenv_as_dict)
	return success, module_to_set, version_to_set


def remove_module(module_path, module_to_unset):
	module_to_unset = str(module_to_unset)
	if not os.path.exists(module_path):
		return None, module_to_unset
	dotenv_as_dict = module_values(module_path)
	if module_to_unset in dotenv_as_dict:
		dotenv_as_dict.pop(module_to_unset, None)
	else:
		return None, module_to_unset
	success = flatten_and_write(module_path, dotenv_as_dict)
	return success, module_to_unset


def flatten_and_write(module_path, dotenv_as_dict):
	with open(module_path, "w") as f:
		for k, v in dotenv_as_dict.items():
			if k.startswith('-r'):
				f.write("%s\n" % k)
			else:
				f.write("%s==%s\n" % (k, v))
	return True
