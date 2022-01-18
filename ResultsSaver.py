
import os
import platform
from datetime import datetime
import shutil
import json
import matplotlib.pyplot as plt


class ResultsSaver:

    def __init__(self):
        self.output_dir_path = self.__create_output_dir()

    def save_results_to_files(self, paths_found, args=None, pheromones=None):
        now_time = datetime.now().strftime("%d-%m__%H-%M-%S")
        dirname = str(args.get("n")) + "__" + now_time
        self.__create_dir(dirname)
        paths_found = list(map(self.__get_path_as_str, paths_found))
        self.__save_to_json(dirname, "results.json", paths_found)
        self.__save_to_json(dirname, "args.json", args)
        pheromones = {str(edge): phero for edge, phero in pheromones.items()}
        self.__save_to_json(dirname, "pheromones.json", pheromones)
        self.__update_results_json(f"{str(args.get('n'))}.json", paths_found)

    def get_results_by_n(self, n):
        path = self.output_dir_path
        file_name = f"{str(n)}.json"
        file_path = os.path.join(path, file_name)
        return self.__load_from_json(file_path)

    def __get_path_as_str(self, path):
        return list(map(str, path))

    def __create_output_dir(self):
        """ creating main output directory if not exists"""
        if platform.system() == "Windows":
            dest_path = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'output')
        else:
            dest_path = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        return dest_path

    def __create_dir(self, dir_name):
        """ creating directory with given name, inside output directory """
        dir_path = os.path.join(self.output_dir_path, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)

    def __save_to_json(self, dirname, filename, value):
        """ saving to json file on given directory name """
        if not value:
            return
        dirpath = os.path.join(self.output_dir_path, dirname)
        filepath = os.path.join(dirpath, filename)

        with open(filepath, 'w') as f:
            json.dump(value, f, indent=4, ensure_ascii=False)

    def __update_results_json(self, filename, results):
        """ saving to json file on given directory name """
        if not results:
            return
        filepath = os.path.join(self.output_dir_path, filename)
        if os.path.exists(filepath):
            data_exists = self.__load_from_json(filepath)
        else:
            data_exists = []
        for result in results:
            if result not in data_exists:
                data_exists.append(result)
        with open(filepath, 'w') as f:
            json.dump(data_exists, f, indent=4, ensure_ascii=False)

    def __load_from_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)