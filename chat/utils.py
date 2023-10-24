import re
import time
import subprocess
import threading
import pypinyin
from pypinyin import pinyin, Style
from django.core.exceptions import ValidationError


def is_chinese(text):
    """
    check if the input text contains chinese
    """
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    match = pattern.search(text)
    return match is not None


def format_link(link:str):
    link = link.replace("https://", "").replace("http://", "").replace("www.", "").replace('/', '_').replace('\\', '_').replace('?', '_').replace('.','_')
    if not link.endswith("_"):
        link += "_"
    return link


def https_link(link:str):
    link = link.replace("https://", "").replace("http://", "").replace("www.", "")
    link = "https://" + link
    return link


def get_first_pinyin_letter(chinese):
    pinyin = pypinyin.pinyin(chinese[0], style=pypinyin.STYLE_NORMAL)[0][0]
    return pinyin[0].upper()


def convert_size(size):
    KB = 1024
    MB = KB ** 2
    GB = KB ** 3

    if size < KB:
        return f"{size} B"
    elif size < MB:
        return f"{size / KB:.2f} KB"
    elif size < GB:
        return f"{size / MB:.2f} MB"
    else:
        return f"{size / GB:.2f} GB"
    

def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size cannot exceed 5MB.")


class cmds:
    """
    command class
    """
    def __init__(self):
        self.procs = dict()
        self.pids = dict()

    def run_command(self, command, command_name, timeout=5):
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, universal_newlines=True)
        self.pids[command_name] = proc.pid
        self.procs[command_name] = proc

        def wait_for_completion():
            # Wait for the process to complete or timeout
            start_time = time.time()
            while timeout is None or (time.time() - start_time) < timeout:
                if proc.poll() is not None:
                    break
                time.sleep(0.1)

            # If the process is still running, terminate it
            if proc.poll() is None:
                print("The subprocess (pid={}) is terminated".format(proc.pid))
                proc.terminate()

            # Wait for the process to terminate and get the return code
            proc.wait()

        thread = threading.Thread(target=wait_for_completion)
        thread.start()

    def add_download_subprocess(self, url, save_path):
        command = ['python', 'chat/download_facvion.py', '--url', url, '--save_path', save_path]
        self.run_command(command, 'download_{}'.format(url), timeout=5)
        
        
def chinese_to_pinyin(input_text):
     pinyin_list = []
     for char in input_text:
         if '\u4e00' <= char <= '\u9fff':
             pinyin_list.extend(pinyin(char, style=Style.NORMAL))
         elif char.isalnum():
             pinyin_list.append([char])

     pinyin_str = ''.join([item[0] for item in pinyin_list])
     return pinyin_str