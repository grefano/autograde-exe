import os
import json
from appdirs import user_config_dir

app_name = 'Autograde'

config_dir = user_config_dir(app_name, appauthor='')
config_path_file = os.path.join(config_dir, "config.json")
print(f"config dir: {config_dir}")
print(f"config path: {config_path_file}")

def config_load():
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(config_path_file):
        config_default = {
            'first_use': True,
            "folder": "C:/Users/gabri/OneDrive/Code/autograde/student/files_test"
        }

        with open(config_path_file, 'w') as f:
            json.dump(config_default, f, indent=2)

        return config_default
    else:
        with open(config_path_file, 'r') as f:
            config = json.load(f)
        return config
    
def config_save(config_dict):
    config_atual = config_load()
    config_atual.update(config_dict)

    with open(config_path_file, 'w') as f:
        json.dump(config_atual, f, indent=2)

