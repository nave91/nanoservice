import psutil
from multiprocessing.managers import SyncManager

try:
    from processmanager import ProcessManager
except ImportError:
    from nanoservice.processmanager import ProcessManager


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

    def train(self, name):
        return self.process_managers[name].train()

    def get_workers(self, name):
        return {worker.name: pid for pid, worker in self.process_managers[name].workers.items()}


SyncManager.register('service_interface', ServiceInterface)
service_manager = SyncManager(address=('localhost', 50000), authkey=b'Vf6x132R0W3Ogp')


class ClientInterface:

    def __init__(self):
        self.service_interface = None

    def connect(self):
        service_manager.connect()
        self.service_interface = service_manager.service_interface()


    def register(self, CodeManager, train=False, start=False, num_of_workers=1, **kwargs):
        self.connect()
        self.service_interface.create_process_manager(CodeManager, num_of_workers)
        if train:
            self.train(CodeManager)
        if start:
            self.start_process_manager(CodeManager)

    def get_workers(self, code_manager_name):
        return self.service_interface.get_workers(code_manager_name)

    def train(self, CodeManager):
        return self.service_interface.train(CodeManager.name())

    def start_process_manager(self, CodeManager):
        self.service_interface.start_process(CodeManager.name())

    def query(self, CodeManager, input):
        return self.service_interface.query(CodeManager.name(), input)

    def controller(self, code_manager_name):
        controller = {}
        workers = self.get_workers(code_manager_name)
        for name, pid in workers.items():
            controller[name] = psutil.Process(pid)
        return controller


client_interface = ClientInterface()
