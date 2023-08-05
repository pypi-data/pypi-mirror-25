from reactjo.helpers.config_manager import get_cfg, set_cfg

def print_worklist():
	cfg = get_cfg()
	if 'worklist' in cfg:
		wl = cfg['worklist']
		if len(wl) > 0:
			print(" ")
			print("Here's what Reactjo just did for you")
			for item in wl:
				print(item)

			print("Enjoy :-)")
			print(" ")

		cfg['worklist'] = []
		set_cfg(cfg)
