from domain import base as ab


class SaltExecutor(ab.Invokable):

    def __init__(self):
        ab.Invokable.__init__(self)

    def on_invoking(self, *args, **kwargs):
        pass