from glob import glob
from tqdm import tqdm
import yaml
import sys
import csv
import os

PRJ_DIR = os.path.dirname(__file__)

def inspect_directory(inspect_dir, output_path):

    print(f"[{__file__}] start inspect file in '{inspect_dir}'")
    config = load_yaml(os.path.join(PRJ_DIR, 'config.yml'))
    print(f"[{__file__}] extract file path list in {inspect_dir}")
    path_list = get_path_list(dir_=inspect_dir)
    path_dict_list = get_path_dict_list(path_list=path_list, config=config)
    save_dict_to_csv(path_dict_list, save_path=output_path)
    
    print(f"[{__file__}] inspect {len(path_dict_list)} files, save result to '{output_path}'")


def get_path_list(dir_:str, sort:bool=True) -> list:

    dir_query = os.path.join(dir_, "**")
    path_list = glob(dir_query, recursive=True)
    path_list = sorted(path_list) if sort else path_list
    
    return path_list


def get_path_dict_list(path_list:list, config:dict, splitter:str='/') -> list:

    path_dict_list = list()
    removal_ext_type_list = ['01_data', '02_weight', '03_etc']

    for path in tqdm(path_list):

        path_splitted = path.split(splitter)
        
        file_name = path_splitted[-1]
        file_name_splitted = file_name.split('.')
        ext = file_name_splitted[-1] if len(file_name_splitted) > 1 else ''
        ext_type = get_ext_type(ext, config=config)
        size = os.path.getsize(path)
        command = f'rm {path} &&' if ext_type in removal_ext_type_list else ''

        path_dict = {'path': path, 'file_name': file_name, 'ext': ext, 'ext_type': ext_type, 'size': size, 'command':command}
        path_dict_list.append(path_dict)

    path_dict_list = sorted(path_dict_list, key=lambda dict_: (dict_['ext_type'], dict_['ext'], dict_['path']))

    return path_dict_list


def get_ext_type(ext:str, config:dict) -> str:

    ext_type = ''
    
    if ext in config['extension']['data']:

        ext_type = '01_data'
    
    elif ext in config['extension']['weight']:

        ext_type = '02_weight'

    elif ext in config['extension']['etc']:

        ext_type = '03_etc'
    
    elif ext in config['extension']['script']:

        ext_type = '04_script'

    elif ext in config['extension']['readme']:

        ext_type = '05_readme'

    elif not ext:

        ext_type = '06_directory'
    
    return ext_type


def load_yaml(path):
    
    with open(path, 'r') as f:
    
        obj = yaml.load(f, Loader=yaml.FullLoader)

    return obj


def save_dict_to_csv(path_dict:dict, save_path:str) -> None:

    with open(save_path, 'w', newline='') as f:
        
        writer = csv.DictWriter(f, fieldnames=['path', 'file_name', 'ext', 'ext_type', 'size', 'command'])
        writer.writeheader()
        writer.writerows(path_dict)

    return None

if __name__ == '__main__':
    
    inspect_dir, output_path = sys.argv[1], sys.argv[2]
    inspect_directory(inspect_dir, output_path)