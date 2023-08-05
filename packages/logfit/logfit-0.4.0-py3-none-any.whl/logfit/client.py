import json
import logging
import os
import requests
from time import sleep

import magic

from logfit.daemon import Daemon
from logfit.tail import TailedFile


class LogFit(Daemon):
    def __init__(self, **kwargs):
        self.tails = {}
        self.config = kwargs.pop('config')
        kwargs['log_level'] = self.config.log_level
        kwargs['log_file'] = self.config.log_file
        super().__init__(**kwargs)

    def run(self):
        self.find_log_files()
        while True:
            sleep(5)
            self.read_logs()

    def stop(self, *args, **kwargs):
        for file_path, tail in self.tails.items():
            tail.close()
        if self.is_running():
            super().stop(*args, **kwargs)

    def read_logs(self):
        for path, tail in self.tails.items():
            while True:
                line = tail.readline()
                if not line:
                    break
                self.send_line(path, line)

    def find_log_files(self):
        for root, _, file_names in os.walk(self.config.watch_directory):
            for file_name in file_names:
                path = os.path.join(root, file_name)
                if self.config.is_ignored_path(path):
                    continue
                self.tail_file(path)

    def tail_file(self, file_path):
        try:
            open(file_path, 'r').close()
        except IOError as e:
            return
        mime_type = magic.from_file(file_path, mime=True)
        if mime_type not in self.config.allowed_mime_types:
            return
        tail = TailedFile(file_path)
        self.tails[file_path] = tail
        self.log("Tailing " + file_path, logging.DEBUG)

    def send_line(self, path, line):
        data = {
            'source': self.config.source,
            'path': path,
            'row_data': line,
        }
        data = json.dumps(data)
        requests.post(self.config.ingest_endpoint, data=data)
        self.log("Sending data from " + path, logging.DEBUG)
