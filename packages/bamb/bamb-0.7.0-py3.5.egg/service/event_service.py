from domain import base
from bamb import auto_wired
from bamb import Bamb
from bamb import BeanFactory
from common import constants
from domain import base
from domain import exceptions
from common import utils


class EventManager(object):

    def __init__(self):

        self.__listeners = {}
        self.register(constants.LISTENER_TASK, TaskStateChangeListener())

    def register(self, key, listener):
        if key is None:
            raise exceptions.IllegalArgumentException("please assign a key to the listener")
        if not isinstance(listener, base.Listener):
            raise exceptions.IllegalArgumentException("invalid listener")
        self.__listeners[key] = listener
        if len(listener.callback_name) > 0:
            f = Bamb.singleton().bean_factory
            if not isinstance(f, BeanFactory):
                raise exceptions.AppException("can not get bean factory!")
            f.register(listener.callback_name, listener, overwrite=True)

    def register_user_listener(self, user_id, listener_full_name):
        if not isinstance(user_id, str) or len(user_id) == 0:
            raise exceptions.IllegalArgumentException("invalid user_id")
        if not isinstance(listener_full_name, str) or len(listener_full_name) == 0:
            raise exceptions.IllegalArgumentException("invalid callback_name")
        listener = utils.create_instance(listener_full_name, user_id=user_id)
        self.register(user_id, listener)

    def unregister(self, key):
        self.__listeners.pop(key, None)

    @property
    def listeners(self):
        return self.__listeners

    def dispatch(self, e):
        if not isinstance(e, base.Event):
            return

        if e.event_id == constants.EVENT_ID_BROADCAST_COMMAND:
            if e.is_command:
                if e.command == constants.COMMAND_PREPARE_LISTENER_FOR_USER:
                    user_id = e.data["user_id"]
                    listener_class = e.data["listener"]
                    self.register_user_listener(user_id, listener_class)
                else:
                    cmdp = self.command_processor
                    if not isinstance(cmdp, base.CommandProcessor):
                        raise exceptions.AppException("invalid command processor!")
                    cmdp.on_command(e.command, **e.data)
            return

        for i, l in self.__listeners.items():
            if isinstance(l, base.Listener):
                matched = False
                for f in l.filters:
                    if f.match(e):
                        matched = True
                        break
                if matched:
                    if len(l.queue_suffix) > 0:
                        dis = self.background_dispatcher
                        if not isinstance(dis, BackgroundDispatcher):
                            raise exceptions.AppException("invalid listener!")
                        dis.dispatch(e, constants.QUEUE_PREFIX_FOR_BACKGROUND_EVENTS + l.queue_suffix, l.callback_name)
                    else:
                        l.on_event(e)

    def send_broadcast(self, e):
        sender = self.background_broadcast_sender
        if not isinstance(sender, BackgroundBroadcastSender):
            raise exceptions.AppException("can not get the broadcast sender")
        sender.send(e)

    @property
    @auto_wired(constants.SERVICE_BACKGROUND_EVENT_DISPATCHER)
    def background_dispatcher(self):
        return None

    @property
    @auto_wired(constants.SERVICE_BACKGROUND_BROADCAST)
    def background_broadcast_sender(self):
        return None

    @property
    @auto_wired(constants.SERVICE_COMMAND_PROCESSOR)
    def command_processor(self):
        return None


class BackgroundDispatcher(object):

    def dispatch(self, e, queue, callback):
        pass


class BackgroundBroadcastSender(object):

    def send(self, e):
        pass


class TaskStateChangeListener(base.Listener):

    @property
    def filters(self):
        return [base.SimpleEventFilter(topics=[constants.EVENT_ID_TASK_STATE_CHANGED])]

    def on_event(self, e, queue=""):
        if not isinstance(e, base.Event):
            return
        ts = Bamb.bean(constants.SERVICE_TASK)
        root_id = e.data[constants.PARM_TASK_ID]
        root = ts.load(root_id)
        path = e.data[constants.PARM_CURRENT_PATH]
        if root.current_path != path:
            return
        op = root.child(e.data[constants.PARM_CURRENT_PATH])
        if op.state == constants.STATE_FINISHED:
            ts.run(root)
