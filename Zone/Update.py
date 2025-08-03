# coding=utf-8
from tkinter import filedialog
from tkinter import Tk
import Zone.Config as Config
import requests
import glob
import time
import json
import os
import re


class GSPath:
    @classmethod
    def choose_file(cls):
        window = Tk()
        window.withdraw()
        path = filedialog.askopenfilename()
        print(path)
        return path

    @classmethod
    def join(cls, *paths):
        return os.path.join(*paths).replace('\\', '/')

    @classmethod
    def parse(cls, path: str) -> (str, str, str, str):
        folder, name = os.path.split(path)
        basename, extension = os.path.splitext(name)
        return folder, name, basename, extension.lower()

    @classmethod
    def folder_path(cls, path: str):
        folder, name, basename, extension = cls.parse(path)
        return folder

    @classmethod
    def exist(cls, path: str):
        return os.path.exists(path)

    @classmethod
    def glob_all(cls, folder: str):
        search_dir = GSPath.join(folder, '**')
        return glob.glob(search_dir, recursive=True)

    @classmethod
    def all_file(cls, folder: str):
        return [path for path in cls.glob_all(folder) if os.path.isfile(path)]

    @classmethod
    def read_class(cls, folder: str, extension: str):
        files = cls.glob_all(folder)
        result = []
        for file_path in files:
            if file_path.upper().endswith('.{}'.format(extension.upper())) and os.path.isfile(file_path):
                result.append(file_path)
        return result

    @classmethod
    def read(cls, path: str):
        if not cls.exist(path):
            return None
        with open(path, 'r', encoding='utf-8', errors='ignore') as handle:
            return handle.read()

    @classmethod
    def write(cls, path: str, content: str):
        folder = cls.folder_path(path)
        if not cls.exist(folder):
            os.makedirs(folder)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(content)

    @classmethod
    def json_str_to_obj(cls, json_str: str):
        if json_str is None:
            return None
        return json.loads(json_str)

    @classmethod
    def obj_to_json_str(cls, json_obj, indent=4):
        return json.dumps(json_obj, ensure_ascii=False, indent=indent, sort_keys=True)

    @classmethod
    def read_json(cls, path: str):
        json_str = cls.read(path)
        return cls.json_str_to_obj(json_str)

    @classmethod
    def write_json(cls, path, content):
        json_str = cls.obj_to_json_str(content)
        GSPath.write(path, json_str)

    @classmethod
    def download_file(cls, url, use_proxy: bool = False):
        print('RequestUrl = {}'.format(url))
        response = requests.get(url, headers=Config.header, proxies=Config.proxies if use_proxy else None)
        content = response.content if response.status_code == 200 else None
        response.close()
        time.sleep(3)
        return content


class Update:
    @classmethod
    def download(cls, path=None, parse=False):
        if path is None:
            info_path = GSPath.choose_file()
        else:
            info_path = path

        info_folder = GSPath.folder_path(info_path)
        info_dict = GSPath.read_json(info_path)

        main = info_dict.get('main')
        if not main:
            return 'MAIN读取错误'

        main_name = 'main.qxr' if parse else 'main.qxf'
        main_path = GSPath.join(info_folder, main_name)
        if not GSPath.exist(main_path):
            download = GSPath.download_file(url=main, use_proxy=True)
            if download:
                GSPath.write(main_path, download.decode())
            else:
                return '下载MAIN失败'

        if parse:
            script_dict = info_dict.get('script')
            if not script_dict:
                stop = False
                script_dict = {}
                for line in GSPath.read(main_path).splitlines():
                    line = line.strip()
                    if 'github' in line and \
                            not line.startswith('//') and \
                            not line.startswith('#') and\
                            not line.startswith('> '):
                        pattern = r'[^;](https?://[^/\s]*github[^/\s]*\.com[^\s"]*)'
                        r = re.search(pattern, line)
                        if r:
                            url = r.groups()[0].strip()
                            d, n, b, e = GSPath.parse(url)
                            if url not in script_dict.values():
                                if n not in script_dict.keys():
                                    script_dict[n] = url
                                else:
                                    t = int(time.time() * 10000000)
                                    name = '{}-{}'.format(n, t)
                                    script_dict[name] = url
                                    stop = True
                info_dict['script'] = script_dict
                GSPath.write_json(info_path, info_dict)
                if stop:
                    return '需要编辑INFO'

            path_url = {}
            for name, url in script_dict.items():
                path = GSPath.join(info_folder, 'Script', name)
                if GSPath.exist(path):
                    path_url[path] = url
                else:
                    download = GSPath.download_file(url=url, use_proxy=True)
                    if download:
                        path_url[path] = url
                        GSPath.write(path, download.decode())
                    else:
                        return '下载{}失败'.format(name)

            qxr_content = GSPath.read(main_path)
            for path, url in path_url.items():
                qxr_content = qxr_content.replace(url, path)
            GSPath.write(main_path, qxr_content)

        qxc_content = GSPath.read(Config.qxc_path)
        qxc_content = qxc_content.replace(main, main_path)
        GSPath.write(Config.qxc_path, qxc_content)
        return '流程成功'

    @classmethod
    def create_rewrite(cls, name, url):
        info_dict = {'main': url}
        info_path = GSPath.join(Config.root_path, 'Rewrite', name, 'info.json')
        if not GSPath.exist(info_path):
            GSPath.write_json(info_path, info_dict)
        print(Update.download(info_path, True))

    @classmethod
    def create_filter(cls, name, url):
        info_dict = {'main': url}
        info_path = GSPath.join(Config.root_path, 'Filter', name, 'info.json')
        if not GSPath.exist(info_path):
            GSPath.write_json(info_path, info_dict)
        print(Update.download(info_path, False))


if __name__ == '__main__':
    GSPath.choose_file()
