from ipykernel.ipkernel import IPythonKernel
import multiprocessing
import requests
from urllib.parse import parse_qs


class DataQueue(multiprocessing.Process):
    q = None

    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q

    def run(self):
        while True:
            try:
                item = self.q.get()
                r = requests.post("https://logkernel.mentoracademy.org/post_logging", data=item, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            except:
                continue


class LoggingIPythonKernel(IPythonKernel):
    q = multiprocessing.Queue()
    data_queue = DataQueue(q)

    implementation = 'Logging Kernel'
    implementation_version = '1.0'
    language_info = {
        'name': 'python',
        'mimetype': 'text/x-python',
        'file_extension': '.py',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_queue.start()

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        json_code = parse_qs(code)
        # Below if condition is to check if the logging extension
        # is enabled and appending the metadata to the code or not
        if 'code' in json_code:
            self.q.put(code)
            new_code = json_code["code"][0]
            return super().do_execute(new_code, silent, store_history, user_expressions, allow_stdin)
        else:
            return super().do_execute(code, silent, store_history, user_expressions, allow_stdin)

    def do_shutdown(self, restart):
        self.data_queue.terminate()
        return super().do_shutdown(restart)
