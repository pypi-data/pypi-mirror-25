# -*- coding: utf-8 -*-
"""reactjo.reactjo: provides entry point main()."""
__version__ = "1.0.0"

import sys, os, subprocess
from reactjo.helpers.config_manager import get_cfg, set_cfg, build_cfg
from reactjo.helpers.worklist import print_worklist, worklist
from reactjo.helpers.extend import extend
from reactjo.helpers.update import update

def initialize():
	if not os.path.exists('reactjorc'):
		os.mkdir('reactjorc')
	if not os.path.exists('reactjorc/extensions'):
		os.mkdir('reactjorc/extensions')
	if not os.path.exists('reactjorc/config.json'):
		build_cfg()
		worklist('Created reactjorc/')
		worklist('Created reactjorc/extensions/')

	project_root = get_cfg()['paths']['project_root']
	if not os.path.exists(project_root):
		os.mkdir(project_root)
		worklist('Created ' + project_root + '/')

def main():
	cmd = sys.argv[1]
	if cmd in ['init', 'initialize', 'i']:
		initialize()
		update()
	elif cmd in ['update', 'u']:
		update()
	elif cmd in ['extend', 'extension', 'e']:
		extend()
	else:
		cfg = get_cfg()
		for ext in cfg['extensions']:
			path = os.path.join(
				cfg['paths']['reactjorc'],
				'extensions',
				ext['rc_home'],
				'entry.py'
			)
			subprocess.run(['python', path, cmd])

	print_worklist()
