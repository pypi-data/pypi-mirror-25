from . import base
class RequestData(base.EasySerializable):
    pass

class SendingData(base.EasySerializable):

    def __init__(self, view="", data={}):
        base.EasySerializable.__init(self)
        self.view = view
        self.data = data

