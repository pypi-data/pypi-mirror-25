from reactjo.helpers.config_manager import get_cfg, set_cfg
import os, shutil, subprocess
from reactjo.helpers.worklist import worklist as wl

def update():
	cfg = get_cfg()
	extensions = os.path.join(cfg['paths']['reactjorc'], 'extensions')

	# Remove all extensions and reinstall them.
	if os.path.exists(extensions):
		shutil.rmtree(extensions)
	os.mkdir(extensions)

	for ext in cfg['extensions']:
		path = os.path.join(extensions, ext['rc_home'])

		if 'branch' in ext:
			subprocess.call(['git', 'clone', '-b', ext['branch'], ext['uri'], path])
		else:
			subprocess.call(['git', 'clone', '-b', 'master', ext['uri'], path])

		dependencies = path + '/requirements.txt'
		if os.path.exists(dependencies):
			deps = open(dependencies, 'r').read()
			if len(deps) > 0:
				subprocess.call(['pip', 'install', '-r', dependencies])

	wl('Replaced or reinstalled extensions')
