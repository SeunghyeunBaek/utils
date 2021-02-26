from glob import glob
from tqdm import tqdm
import sys
import csv
import os


def inspect_directory(inspect_dir, output_path):

    print(f"[{__file__}] start inspect file from '{inspect_dir}'")
    
    path_list = get_path_list(dir_=inspect_dir)
    path_dict_list = get_path_dict_list(path_list=path_list)
    save_dict_to_csv(path_dict_list, save_path=output_path)
    
    print(f"[{__file__}] inspect {len(path_dict_list)} files, save result to '{output_path}'")


def get_path_list(dir_:str, sort:bool=True) -> list:

    dir_query = os.path.join(dir_, "**")
    path_list = glob(dir_query, recursive=True)
    path_list = sorted(path_list) if sort else path_list
    
    return path_list


def get_path_dict_list(path_list:list, splitter:str='/') -> list:

    path_dict_list = list()
    removal_ext_type_list = ['01_data', '02_weight']

    for path in tqdm(path_list):

        path_splitted = path.split(splitter)
        
        file_name = path_splitted[-1]
        file_name_splitted = file_name.split('.')
        ext = file_name_splitted[-1] if len(file_name_splitted) > 1 else ''
        ext_type = get_ext_type(ext)
        command = f'rm {path} &&' if ext_type in removal_ext_type_list else ''

        path_dict = {'path': path, 'file_name': file_name, 'ext': ext, 'ext_type': ext_type, 'command':command}
        path_dict_list.append(path_dict)

    path_dict_list = sorted(path_dict_list, key=lambda dict_: (dict_['ext_type'], dict_['ext'], dict_['path']))

    return path_dict_list


def get_ext_type(ext:str) -> str:

    data_ext = ['csv', 'json', 'png', 'jpg', 'jpeg', 'tif']
    weight_ext = ['pt', 'pth', 'h5', 'pkl', 'pickle']
    script_ext = ['py', 'sh', 'yaml']
    readme_ext = ['txt', 'md']
    ext_type = ''
    
    if ext in data_ext:

        ext_type = '01_data'
    
    elif ext in weight_ext:

        ext_type = '02_weight'
    
    elif ext in script_ext:

        ext_type = '03_script'

    elif ext in readme_ext:

        ext_type = '04_readme'

    elif ext == '':

        ext_type = '05_directory'
    
    return ext_type


def save_dict_to_csv(path_dict:dict, save_path:str) -> None:

    with open(save_path, 'w', newline='') as f:
        
        writer = csv.DictWriter(f, fieldnames=['path', 'file_name', 'ext', 'ext_type', 'command'])
        writer.writeheader()
        writer.writerows(path_dict)

    return None

if __name__ == '__main__':
    
    inspect_dir, output_path = sys.argv[1], sys.argv[2]
    inspect_directory(inspect_dir, output_path)