import os
import json

def json_read(path):
    with open(path, 'r') as file:
        return json.load(file)

def json_write(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent = 4)

def find_config_path():
	def check():
		# reactjo.json exists?
		config_file = os.path.isfile('./reactjorc/config.json')
		if config_file:
			return found()
		else:
			return bubble_up(os.getcwd())

	def bubble_up(prev_path):
		os.chdir("..")
		next_path = os.getcwd()
		if prev_path == next_path:
			# Escape the recursion if "cd .." does nothing.
			return failure()
		else:
			return check()

	def found():
		return os.getcwd() + '/reactjorc/config.json'

	def failure():
		print("Sorry, couldn't find the config.json file. cd to that directory, or a child directory.")
		print("""If there really is no config.json, you probably need to create a project. Try running:
		----------------------
		reactjo init
		----------------------
		""")

	return check()

def get_cfg():
	return json_read(find_config_path())

def set_cfg(content):
	json_write(find_config_path(), content)

def build_cfg():
    LATEST_VERSION = '2.1.1'
    project_name = ""
    while project_name == "":
        project_name = input("Please name your project: ")

    default_config = {
        "paths": {
            "super_root": os.getcwd(),
            "reactjorc": os.getcwd() + "/reactjorc",
            "project_root": os.getcwd() + "/" + project_name
        },
        "extensions": [
            {
                "rc_home": "reactjo_django",
                "uri": "https://github.com/aaron-price/reactjo-django.git",
                "branch": 'v' + LATEST_VERSION
            },
            {
                "rc_home": "reactjo_nextjs",
                "uri": "https://github.com/aaron-price/reactjo-nextjs.git",
                "branch": 'v' + LATEST_VERSION
            }
        ],
        "project_name": project_name,
        "models": [],
        "serializers": [],
        "views": [],
        "current_scaffold": {}
    }

    with open('reactjorc/config.json', 'w') as file:
        json.dump(default_config, file, indent = 4)
