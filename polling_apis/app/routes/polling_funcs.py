import json
import logging
import os
from models.singleton import Singleton
import sys

class Polling(metaclass = Singleton):
    def __init__(self, config_file):
        self.config = {}
        self.log = logging.getLogger('polling_app')
        if not os.path.exists(config_file):
            print("invalid config path")
            sys.exit()
        with open(config_file, "r") as inpf:
            self.config = json.load(inpf)
        print("Polling service running")

    def print_hello(self):
        print("hello")

