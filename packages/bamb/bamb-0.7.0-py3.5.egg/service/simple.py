from domain import base as ab
import random
import time
from common import constants
from domain import exceptions


class SimpleNativeExecutor(ab.Invokable):

    def __init__(self):
        ab.Invokable.__init__(self)

    def on_invoking(self):
        r = {}
        task_id = self.parameters[constants.PARM_TASK_ID].value
        task_path = self.parameters[constants.PARM_CURRENT_PATH].value
        r[constants.PARM_TASK_ID] = task_id
        r[constants.PARM_CURRENT_PATH] = task_path
        ip = self.target.ip
        if ip[-1] == "3":
            raise exceptions.IllegalOperationException("can not execute on xx3 host!")
        r["ip"] = ip
        r["scheduling"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sleep = random.randint(0, 2)
        time.sleep(sleep)
        r["finished"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(r)
        return r


class SimpleEventConsumer(ab.Listener):

    def __init__(self, *args, **kwargs):
        pass

    @property
    def filters(self):
        return [ab.SimpleEventFilter(topics=[constants.EVENT_ID_TASK_STATE_CHANGED])]

    def on_event(self, e, queue=""):
        print("event received from queue " + queue + " : " + str(e))

    @property
    def queue_suffix(self):
        return "test"

    @property
    def callback_name(self):
        return "simple_event_consumer"