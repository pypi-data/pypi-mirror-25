#
# pyprob
# PyTorch-based library for probabilistic programming and inference compilation
# https://github.com/probprog/pyprob
#

import pyprob
from pyprob import util
import sys
import io
import os
from termcolor import colored
import random
import time

class Requester(object):
    def __init__(self, pool_path):
        self._discarded_files = []
        self._pool_path = pool_path
        num_files = len(self.current_files())
        util.log_print(colored('Protocol: working with batch pool (currently with {0} file(s)) at {1}'.format(num_files, _pool_path), 'yellow', attrs=['bold']))

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def current_files(self):
        files = [name for name in os.listdir(self._pool_path)]
        files = list(map(lambda f:os.path.join(self._pool_path, f), files))
        for f in self._discarded_files:
            files.remove(f)
        return files

    def close(self):
        num_files = len(self.current_files())
        util.log_print(colored('Protocol: leaving batch pool (currently with {0} file(s)) at {1}'.format(num_files, self._pool_path), 'yellow', attrs=['bold']))

    def send_request(self, request):
        return

    def receive_reply(self, discard_source=False):
        pool_empty = True
        pool_was_empty = False
        while pool_empty:
            current_files = self.current_files()
            num_files = len(current_files)
            if (num_files > 0):
                pool_empty = False
                if pool_was_empty:
                    util.log_print(colored('Protocol: resuming, new data appeared in batch pool (currently with {0} file(s)) at {1}'.format(num_files, self._pool_path), 'yellow', attrs=['bold']))
            else:
                if not pool_was_empty:
                    util.log_print(colored('Protocol: waiting for new data, empty batch pool at {0}'.format(self._pool_path), 'yellow', attrs=['bold']))
                    pool_was_empty = True
                time.sleep(0.5)

        current_file = random.choice(current_files)
        ret = None
        with open(current_file, 'rb') as f:
            ret = bytearray(f.read())
        if discard_source:
            self._discarded_files.append(current_file)
        return ret
