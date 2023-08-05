import multiprocessing
import time

from .resource_consumer import ResourceConsumer

lock = multiprocessing.Lock()


class DefaultResourceManager:
    def __init__(self, consumers: list):
        assert type(consumers) == list, \
            "consumers must be ResourceConsumer list type"
        self.processes = []
        for consumer in consumers:
            assert type(consumer) == ResourceConsumer, \
                "Element in consumers must be ResourceConsumer type"
            self.processes.append(consumer)

    def run(self):
        try:
            while True:
                # check not started process
                not_alive = [process for process in self.processes
                             if not process.is_alive()]
                for process in not_alive:
                    # Not started process
                    if not process.has_resource:
                        if self.allocate_resource(process):
                            process.update_kwargs(process.resource)
                            process.start()

                    # Finished process
                    else:
                        # Deallocate resource
                        self.deallocate_resource(
                            process.uuid, process.namespace)

                        # Make new process
                        p = ResourceConsumer(**process.get_args())
                        self.processes.append(p)

                        # Remove from process list
                        process.terminate()
                        process.join()
                        self.processes.remove(process)
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.terminate_processes()

    def terminate_processes(self):
        living_process = [process for process in self.processes
                          if process.is_alive()]
        for process in living_process:
            self.deallocate_resource(process.uuid, process.namespace)
            process.terminate()

        for process in living_process:
            process.join()

    @staticmethod
    def get_resource(pid, namespace):
        raise NotImplementedError("Implement get_resource method")

    @staticmethod
    def deallocate_resource(pid, namespace):
        raise NotImplementedError("Implement deallocate_resource method")

    def allocate_resource(self, process):
        resource = self.get_resource(process.uuid, process.namespace)
        if resource:
            process.resource = resource
            process.has_resource = True
            return True
        else:
            return False
