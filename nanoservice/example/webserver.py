# from service import service_manager
# from processmanager import ProcessManager
from nanoservice.example.code_example import MyCodeManager
from nanoservice.clientinterface import client_interface

# service_manager.connect()
# service_interface = service_manager.service_interface()
# pm = ProcessManager(MyCodeManager)
# service_interface.start_process(pm)

client_interface.register(CodeManager=MyCodeManager, num_of_workers=1)

while True:
    str = input("what did ya say?\n")
    output = client_interface.service_interface.query('svc', str)
    print(output)
