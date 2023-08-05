import uuid
from multiprocessing import Process


class ResourceConsumer(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={},
                 namespace='', *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.uuid = str(uuid.uuid4())
        self.has_resource = False
        self.resource = None
        self.namespace = namespace
        self._origin_args = args
        self._origin_kwargs = kwargs

    @property
    def target(self):
        return self._target

    @property
    def origin_args(self):
        return self._origin_args

    @property
    def origin_kwargs(self):
        return self._origin_kwargs

    def update_args(self, args):
        self._args = tuple(list(self._args) + list(args))

    def update_kwargs(self, kwargs):
        self._kwargs.update(dict(kwargs))

    def get_args(self):
        return {
            'args': self._origin_args,
            'kwargs': self._origin_kwargs,
            'target': self._target,
            'name': self.name,
            'namespace': self.namespace,
            'daemon': self.daemon,

        }
