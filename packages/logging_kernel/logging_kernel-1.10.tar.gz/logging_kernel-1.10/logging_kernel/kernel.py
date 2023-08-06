from ipykernel.ipkernel import IPythonKernel
import multiprocessing
import queue
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
                r = requests.post("https://zl2mi32xg5.execute-api.us-east-1.amazonaws.com/dev/postLogging", data=item, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            except queue.Empty:
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
        if 'code' in json_code:
            self.q.put(code)
            new_code = json_code["code"][0]
            return super().do_execute(new_code, silent, store_history, user_expressions, allow_stdin)
        else:
            return super().do_execute(code, silent, store_history, user_expressions, allow_stdin)

    def do_shutdown(self, restart):
        self.data_queue.terminate()
        return super().do_shutdown(restart)
