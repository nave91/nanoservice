import multiprocessing
import time

class Worker(dict):
    pass


class ProcessManager(object):

    def __init__(self, CodeManager, num_of_workers):
        self.num_of_workers = num_of_workers
        self.workers = Worker()
        self.code_manager = CodeManager()

    def update_queue(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def code(self, input_queue, output_queue, name):
        print("Entered code of {}".format(name))
        assert self.code_manager is not None
        code_manager =  self.code_manager
        model = code_manager.train()
        while True:
            value = input_queue.get()
            assert type(value) is tuple
            assert len(value) == 2
            request_id = value[0]
            model_input = value[1]
            validated_input = code_manager.validate_input(model_input)
            output = code_manager.test(model, validated_input)
            output_queue.put({request_id: (name, output)})

    def create_process(self, name):
        process = multiprocessing.Process(target=self.code, name=name, args=(self.input_queue, self.output_queue, name))
        process.daemon = True
        process.start()
        return process

    def start_manager(self):
        for i in range(0, self.num_of_workers):
            name = 'NanoProcess-{}'.format(i)
            process = self.create_process(name)
            self.workers[process.pid] = process

    def query(self, input):
        request_id = time.time()
        self.input_queue.put((request_id, input))
        output = self.output_queue.get()
        if request_id in output:
            return output[request_id]
        elif time.time() - list(output)[0] <= 1:
            self.output_queue.put(output)
        else:
            raise TimeoutError
