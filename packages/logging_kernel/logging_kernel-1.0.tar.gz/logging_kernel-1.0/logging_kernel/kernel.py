from ipykernel.ipkernel import IPythonKernel
import multiprocessing
import queue
import requests
from urllib.parse import parse_qs

class LoggingIPythonKernel(IPythonKernel):
    q = multiprocessing.Queue()
    data_queue = None

    implementation = 'Logging Kernel'
    implementation_version = '1.0'
    language_info = {
        'name': 'python',
        'mimetype': 'text/x-python',
        'file_extension': '.py',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data_queue = DataQueue(self.q)
        data_queue.start()


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.q.put(code)
        json_code = parse_qs(code)
        new_code = json_code["code"][0]
        return super().do_execute(new_code, silent, store_history, user_expressions, allow_stdin)

class DataQueue(multiprocessing.Process):
    q = None

    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q

    def run(self):
        while True:
            try:
                item = self.q.get()
                r = requests.post("http://localhost:5000/postLogging", data=item, headers = {'Content-type': 'application/x-www-form-urlencoded'})
            except queue.Empty:
                continue
