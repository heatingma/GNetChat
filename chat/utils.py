import re
import time
import subprocess
import threading


def is_chinese(text):
    """
    check if the input text contains chinese
    """
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    match = pattern.search(text)
    return match is not None


###################################################
#                  Command Class                  #
###################################################

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