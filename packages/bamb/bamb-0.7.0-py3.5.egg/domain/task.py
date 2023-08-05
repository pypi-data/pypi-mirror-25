import domain.base
from . import base
from common import constants
import time
from domain import exceptions
from bson import ObjectId
import copy


class Task(base.EasySerializable, base.ListTree, base.Invokable):

    def __init__(self, name="", init_dict=None):
        self.__id = 0
        self.__state = constants.STATE_PENDING
        self.__flags = 0
        self.name = ""
        self.full_name = ""
        self.desc = ""
        self.appendix = None
        self.__current_path = None
        self.template_path = []
        self.__modified = False
        self.__last_updated = time.time()
        self.__last_scheduled = 0
        self.context = None
        base.ListTree.__init__(self)
        base.Invokable.__init__(self)
        base.EasySerializable.__init__(self, init_dict)

        if not self.es_dict_updated:
            self.name = name

    @property
    def state(self):
        s = -1
        ss = []
        for t in self.lt_children:
            ss.append(t.state)
        if len(ss) > 0:
            fcount = 0
            for s in reversed(ss):
                if s > constants.STATE_FINISHED:
                    return s
                if s == constants.STATE_FINISHED:
                    fcount += 1
            if fcount == 0:
                return constants.STATE_PENDING
            if fcount == len(ss):
                return constants.STATE_FINISHED
            return constants.STATE_RUNNING
        else:
            return self.__state

    @state.setter
    def state(self, value):
        if self.is_leaf:
            if self.__state != value:
                self.__state = value
        else:
            raise exceptions.IllegalOperationException("can not set state for parent task!")


    @property
    def task_id(self):
        oid = self.object_id
        if isinstance(oid, ObjectId):
            return oid.__str__()
        else:
            if isinstance(oid, str):
                return oid
            else:
                return ""

    @property
    def is_template(self):
        return self.__flags & constants.MASK_TASK_ATTR_TEMPLATE

    @property
    def is_runtime_task(self):
        return self.__flags & constants.MASK_TASK_ATTR_RUNTIME

    @is_template.setter
    def is_template(self, value):
        self.__flags |= constants.MASK_TASK_ATTR_TEMPLATE

    @property
    def is_operation(self):
        return self.__flags & constants.MASK_TASK_ATTR_OPERATION

    @property
    def current_path(self):
        return self.__current_path

    def current_operation(self):
        if not self.is_root:
            raise exceptions.IllegalOperationException("operation locating is only applicable for root task!")
        return self.child(self.__current_path)

    def fetch_next_operation(self):
        if self.is_root:
            if self.__current_path is None:
                t = self.lt_next(matcher=TaskMatchers.operation_matcher, try_self=True)
                if isinstance(t, Task):
                    self.__current_path = t.lt_path()
                return t
            else:
                t = self.child(self.__current_path)
        else:
            t = self
        if isinstance(t, Task):
            if t.is_operation:
                t = t.lt_next(matcher=TaskMatchers.operation_matcher, try_self=False)
            else:
                t = t.lt_first(matcher=TaskMatchers.operation_matcher)
            if isinstance(t, Task):
                self.lt_root().__current_path = t.lt_path()
                return t
        return None

    @property
    def flattened(self):
        return self.__flags & constants.MASK_TASK_ATTR_FLATTENED

    @flattened.setter
    def flattened(self, value):
        self.__flags |= constants.MASK_TASK_ATTR_FLATTENED

    @property
    def is_modified(self):
        return self.__modified

    @property
    def last_updated(self):
        return self.__last_updated

    @property
    def last_scheduled(self):
        return self.__last_scheduled

    @last_scheduled.setter
    def last_scheduled(self, value):
        self.__last_scheduled = value

    def get_all_result(self):
        if self.result is None:
            r = base.Result()
        else:
            d = self.result.es_to_dict()
            r = base.EasySerializable.es_load(d)
        for t in self.lt_children:
            r.lt_add_child(t.get_all_result())
        return r

    def get_host_ip_by_state(self, result_state):
        ips = []
        t = self.lt_next(try_self=True)
        while t is not None:
            state = constants.MASK_RESULT_UNKNOWN
            if t.result is not None:
                state = t.result.state
            if state == result_state:
                ips.append(t.target.ip)
            t = t.lt_next()
            if t is not None:
                if len(t.lt_path()) <= len(self.lt_path()):
                    break
        return ips

    def on_change(self):
        r = self.lt_root()
        if r.__state != constants.STATE_PENDING and r.__state != constants.STATE_TERMINATED:
            raise exceptions.IllegalOperationException("can not modify body information to a running task!")
        self.__modified = True
        self.__last_updated = time.time()

    def mark_operations(self):
        for t in self.lt_iterator():
            if len(t.lt_children) == 0:
                t.__flags |= constants.MASK_TASK_ATTR_OPERATION

    def insert_atom_operations(self):
        if not isinstance(self.target, domain.base.Target):
            return
        for t in self.target.lt_children:
            ts = Task()
            ts.copy_execution_info(self, target=t.clone())
            ts.__flags |= constants.MASK_TASK_ATTR_RUNTIME
            ts.insert_atom_operations()
            self.lt_add_child(ts)


class Context(base.EasySerializable):

    def __init__(self, *args, **kwargs):
        self.target = None
        self.parameters = {}
        self.user = None
        base.EasySerializable.__init__(self, *args, **kwargs)


class TaskMatchers(object):

    @staticmethod
    def operation_matcher(t):
        if not isinstance(t, Task):
            return False
        return t.is_operation

    @staticmethod
    def result_state_matcher(t, r, result_state=constants.MASK_RESULT_UNKNOWN):
        if not isinstance(t, base.Target):
            return False
        if not isinstance(r, base.Result):
            return False
        if not t.is_leaf:
            return True
        return r.state == result_state
