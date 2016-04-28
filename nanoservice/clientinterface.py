import psutil
import logging, sys

try:
    from serviceinterface import service_manager
except ImportError:
    from nanoservice.serviceinterface import service_manager

logger = logging.getLogger('nanoservice')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class ClientInterface:

    def __init__(self):
        self.service_interface = None
        self.connect()

    def connect(self):
        service_manager.connect()
        self.service_interface = service_manager.service_interface()


    def register(self, CodeManager, callerpid, train=False, start=False, num_of_workers=1, **kwargs):
        logger.info('Registering CodeManager: {code_manager} with client interface,'
                    ' callerpid: {callerpid}'.format(code_manager=CodeManager,
                                                     callerpid=callerpid))
        self.service_interface.create_process_manager(CodeManager, num_of_workers, callerpid)
        if train:
            self.train(CodeManager)
        if start:
            self.start_process_manager(CodeManager)

    def get_workers(self):
        return self.service_interface.get_workers()

    def train(self, CodeManager):
        return self.service_interface.train(CodeManager.id())

    def start_process_manager(self, CodeManager):
        self.service_interface.start_process(CodeManager.id())

    def query(self, CodeManager, input):
        return self.service_interface.query(CodeManager.id(), input)

    def controller(self):
        controller = {}
        workers = self.get_workers()
        for project_name, nano_workers in workers.items():
            controller.setdefault(project_name, {})
            for name, pid in nano_workers.items():
                controller[project_name][name] = psutil.Process(pid)
        return controller


client_interface = ClientInterface()
