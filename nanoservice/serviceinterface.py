import os
import logging, sys
from multiprocessing.managers import SyncManager

try:
    from processmanager import ProcessManager
except ImportError:
    from nanoservice.processmanager import ProcessManager


logger = logging.getLogger('nanoservice')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class ServiceInterface:

    def __init__(self):
        self.process_managers = {}

    def create_process_manager(self, CodeManager, num_of_workers, callerpid):
        if CodeManager.id() not in self.process_managers:
            process_manager = ProcessManager(CodeManager=CodeManager, num_of_workers=num_of_workers,
                                             callerpid=callerpid, parentpid=os.getpid())
            self.process_managers[CodeManager.id()] = process_manager

    def start_process(self, name):
        from multiprocessing import Queue
        input_queue = Queue()
        output_dict = Queue()
        self.process_managers[name].update_queue(input_queue, output_dict)
        self.process_managers[name].start_manager()

    def query(self, name, input):
        return self.process_managers[name].query(input)

    def train(self, name):
        return self.process_managers[name].train()

    def get_workers(self):
        return {id_: {worker.name: pid for pid, worker in process_manager.workers.items()} for id_, process_manager in self.process_managers.items()}

    def get_process_managers(self):
        return self.process_managers.keys()


SyncManager.register('service_interface', ServiceInterface)
service_manager = SyncManager(address=('localhost', 50000), authkey=b'Vf6x132R0W3Ogp')
