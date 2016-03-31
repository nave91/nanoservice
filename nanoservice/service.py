from multiprocessing.managers import SyncManager

try:
    from processmanager import ProcessManager
except ImportError:
    from nanoservice.processmanager import ProcessManager
#from code import MyCodeManager


class ServiceInterface:

    def __init__(self):
        self.process_managers = {}

    def create_process_manager(self, CodeManager, num_of_workers):
        if CodeManager.name not in self.process_managers:
            self.process_managers[CodeManager.name()] = ProcessManager(CodeManager, num_of_workers)

    def start_process(self, name):
        from multiprocessing import Queue
        input_queue = Queue()
        output_dict = Queue()
        self.process_managers[name].update_queue(input_queue, output_dict)
        self.process_managers[name].start_manager()

    def query(self, name, input):
        return self.process_managers[name].query(input)


SyncManager.register('service_interface', ServiceInterface)
service_manager = SyncManager(address=('localhost', 50000), authkey=b'Vf6x132R0W3Ogp')

