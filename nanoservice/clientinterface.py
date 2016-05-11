import psutil
import logging, sys

try:
    from serviceinterface import create_service_manager
except ImportError:
    from nanoservice.serviceinterface import create_service_manager

logger = logging.getLogger('nanoservice')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class ClientInterface:

    def __init__(self, connect=False):
        self.service_interface = None
        if connect:
            self.connect()

    def connect(self):
        service_manager = create_service_manager()
        service_manager.connect()
        self.service_interface = service_manager.service_interface()

    def register(self, CodeManager, callerpid, load=False, start=False, num_of_workers=1, **kwargs):
        logger.info('Registering CodeManager: {code_manager} with client interface,'
                    ' callerpid: {callerpid}'.format(code_manager=CodeManager,
                                                     callerpid=callerpid))
        if not self.service_interface:
            raise RuntimeError('Not connected to nanoservice. Please call client_interface.connect().')
        self.service_interface.create_process_manager(CodeManager, num_of_workers, callerpid)
        if load:
            self.load(CodeManager)
        if start:
            self.start_process_manager(CodeManager)

    def get_workers(self):
        return self.service_interface.get_workers()

    def load(self, CodeManager):
        return self.service_interface.load(CodeManager.id())

    def start_process_manager(self, CodeManager):
        self.service_interface.start_process(CodeManager.id())

    def query(self, code_manager_id, input):
        return self.service_interface.query(code_manager_id, input)

    def controller(self):
        controller = {}
        workers = self.get_workers()
        for project_name, nano_workers in workers.items():
            controller.setdefault(project_name, {})
            for name, pid in nano_workers.items():
                controller[project_name][name] = psutil.Process(pid)
        return controller


client_interface = ClientInterface()