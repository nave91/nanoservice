import multiprocessing
import time
import queue
import sys
import psutil
import logging


logger = logging.getLogger('nanoservice')


class Worker(dict):
    pass


class ProcessManager(object):

    def __init__(self, CodeManager, num_of_workers, callerpid, parentpid):
        logger.info('Initialized ProcessManager of CodeManager: {code_manager},'
                    ' workers: {num_of_workers}, callerpid: {callerpid},'
                    ' parentpid: {parentpid}'.format(code_manager=CodeManager,
                                                     num_of_workers=num_of_workers,
                                                     callerpid=callerpid,
                                                     parentpid=parentpid))
        self.num_of_workers = num_of_workers
        self.workers = Worker()
        self.code_manager = CodeManager()
        self.trained_model = None
        self.input_queue = None
        self.output_queue = None
        self.callerpid = callerpid
        self.parentpid = parentpid

    def update_queue(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def load(self):
        logger.info('Training on CodeManager: {code_manager} callerpid: {callerpid}'.format(code_manager=self.code_manager,
                                                                                            callerpid=self.callerpid))
        self.trained_model = self.code_manager.load()
        if self.trained_model:
            return True
        else:
            False

    def code(self, code_manager, trained_model, input_queue, output_queue, process_name):
        """
        This function is deployed as a new process.
        :param code_manager: Extended CodeManager, for reference check codemanager.CodeManager.
        :param trained_model: Trained analytical model (python object) which is held to be in memory.
        :param input_queue: Multiprocessing queue object that stores input as tuples (request_id, validated_input)
        :param output_queue: Multiprocessing queue object that returns dictionary {request_id: (process_name, output)}
        :param process_name: Name of worker process that runs this code.
        :return: None
        """
        logger.info('Entered code of CodeManager: {code_manager}, '
                    'trained_model: {trained_model}, name: {name}'.format(code_manager=code_manager,
                                                                          trained_model=trained_model,
                                                                          name=process_name))
        assert code_manager is not None
        assert trained_model is not None
        assert input_queue is not None
        assert output_queue is not None
        waiting = True
        while waiting:
            if (not psutil.pid_exists(self.callerpid)) or (self.callerpid == self.parentpid):
                logger.warn('Killing process of CodeManager: {code_manager}, '
                            'trained_model: {trained_model}, name: {name}'.format(code_manager=code_manager,
                                                                          trained_model=trained_model,
                                                                          name=process_name))
                sys.exit()
            try:
                value = input_queue.get(block=True)
                assert type(value) is tuple
                assert len(value) == 2
                request_id = value[0]
                validated_input = value[1]
                output = code_manager.evaluate(trained_model, validated_input)
                output_queue.put({request_id: (process_name, output)})
            except queue.Empty:
                continue

    def create_process(self, name):
        logger.warn('Creating Process for CodeManager: {code_manager}, '
                    'name: {name}, callerpid: {callerpid}'.format(code_manager=self.code_manager,
                                                                  callerpid=self.callerpid,
                                                                  name=name))
        process = multiprocessing.Process(target=self.code, name=name, args=(self.code_manager, self.trained_model,
                                                                             self.input_queue, self.output_queue, name))
        process.daemon = True
        process.start()
        return process

    def start_manager(self):
        """
        Using individual processes instead of multiprocessing.Pool since we are not "map"ping inputs to workers.
        Workers grab input themselves and serve the required functionality.
        """
        logger.info('Starting process manager for CodeManager: {code_manager}, '
                    'callerpid: {callerpid}'.format(code_manager=self.code_manager,
                                                    callerpid=self.callerpid))
        for i in range(0, self.num_of_workers):
            process_name = 'NanoProcess-{}-{}'.format(self.code_manager, i)
            process = self.create_process(process_name)
            self.workers[process.pid] = process

    def query(self, input):
        logger.info('Querying CodeManager: {code_manager}, '
                    'callerpid: {callerpid}, input: {input}'.format(code_manager=self.code_manager,
                                                                    callerpid=self.callerpid,
                                                                    input=input))
        request_id = time.time()
        self.input_queue.put((request_id, input))
        output = self.output_queue.get()
        if request_id in output:
            return output[request_id]
        elif time.time() - list(output)[0] <= 1:
            self.output_queue.put(output)
        else:
            raise TimeoutError
