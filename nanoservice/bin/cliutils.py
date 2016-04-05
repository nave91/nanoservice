import argparse
import sys

from nanoservice.interfaces import service_manager


class Initialize(object):

    def __init__(self):
        self.server = None
        self.code_dir = ''

    def set_code_dir(self, code_dir):
        self.code_dir = code_dir

    def run(self):
        if self.code_dir != '':
            sys.path.append(self.code_dir)
        self.server = service_manager.get_server()
        self.server.serve_forever()

    def set_args(self, args):
        code_dir = args.code_dir
        if code_dir is not None and len(code_dir) > 0:
            self.set_code_dir(code_dir)


class Parser:
    
    options = [
        {
            'long': '--CODE_DIR',
            'short': '-c',
            'help': 'Location of code for nanoservice to recognize.',
            'action': 'store',
            'type': str,
            'dest': 'code_dir',
        },
    ]

    
    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser(description='Service to hold python objects in memory',
                                         add_help=True)
        for option in cls.options:
            parser.add_argument(option['long'], option['short'], action=option['action'], help=option['help'], type=option['type'], dest=option['dest'])
        return parser
