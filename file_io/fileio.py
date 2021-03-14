import pickle
import json
import yaml

def save_pickle(path, obj):
    
    with open(path, 'wb') as f:
        
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pickle(path):

    with open(path, 'rb') as f:

        return pickle.load(f)


def save_json(path, obj):

	with open(path, 'w') as f:

		json.dump(obj, f, indent=4, sort_keys=True)


def load_json(path, obj):

	with open(path, 'r') as f:

		return json.load(f)


def save_yaml(path, obj):
	
	with open(path, 'w') as f:

		yaml.dump(obj, f)
		

def load_yaml(path):

	with open(path, 'r') as f:

		return yaml.load(f, Loader=yaml.FullLoader)





