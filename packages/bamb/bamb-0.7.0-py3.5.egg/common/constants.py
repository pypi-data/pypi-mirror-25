import sys


class Constants:

    class ConstError(TypeError):pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind const (%s)" %name)
        self.__dict__[name]=value

sys.modules[__name__] = Constants()

Constants.STATE_PENDING = 0
Constants.STATE_FINISHED = 1
Constants.STATE_RUNNING = 2
Constants.STATE_WAIT = 3
Constants.STATE_PAUSED = 4
Constants.STATE_TERMINATED = 5

Constants.MASK_HIGH_VALUE = 0xFFFFFFFF
Constants.MASK_LOW_VALUE = 0xFFFFFFFF

Constants.MASK_RESULT_UNKNOWN = 0
Constants.MASK_RESULT_SUCCESS = 1
Constants.MASK_RESULT_PARTIAL_SUCCESS = 2
Constants.MASK_RESULT_FAILED = 3

Constants.MASK_TASK_ATTR_ROOT = 0b1
Constants.MASK_TASK_ATTR_OPERATION = 0b10
Constants.MASK_TASK_ATTR_RUNTIME = 0b100
Constants.MASK_TASK_ATTR_FLATTENED = 0b1000
Constants.MASK_TASK_ATTR_TEMPLATE = 0b11000

Constants.MASK_INVOKABLE_TARGET_MANDATORY = 0b1
Constants.MASK_INVOKABLE_IGNORE_RESULT = 0b10

Constants.KEYWORD_DWI = "__dwi"
Constants.KEYWORD_CLASS_NAME = "__class_name"
Constants.KEYWORD_MODULE_NAME = "__module_name"
Constants.KEYWORD_FROM_LIST = "__froms"
Constants.KEYWORD_DICT_UPDATED = "__dict_updated"
Constants.KEYWORDS_ES_ALL = {Constants.KEYWORD_DWI, Constants.KEYWORD_CLASS_NAME, Constants.KEYWORD_MODULE_NAME,
                             Constants.KEYWORD_FROM_LIST, Constants.KEYWORD_DICT_UPDATED}
Constants.KEYWORDS_ES_MANDATORY = {Constants.KEYWORD_CLASS_NAME, Constants.KEYWORD_MODULE_NAME,
                                   Constants.KEYWORD_FROM_LIST}
Constants.KEYWORD_SKIPKEYS = "skipkeys"
Constants.KEYWORD_ZERO_BASED = "zero_based"
Constants.KEYWORD_CHILDREN_AS_DICT = "children_as_dict"

Constants.MSG_IMPROPER_OPERATION = "invalid operation!"
Constants.MSG_ILLEGAL_ARGUMENT = "invalid argument!"
Constants.MSG_INVALID_TYPE = "invalid type!"
Constants.MSG_DUPLICATED = "invalid type!"

Constants.FIELD_ID = "_id"
Constants.FIELD_CHILDREN = "_ListTree__lt_children"

Constants.DEFAULT_SKIPKEYS = ["_EasySerializable__module_name", "_EasySerializable__class_name",
                              "_EasySerializable__froms", "_EasySerializable__dwi", "_EasySerializable__dict_updated",
                              "_ListTree__lt_parent_element"]

Constants.EVENT_ID_TASK_STATE_CHANGED = "TASK_STATE"
Constants.EVENT_ID_NEW_JOURNAL = "JOURNAL"
Constants.EVENT_ID_BROADCAST_COMMAND = "BROADCAST_COMMAND"

Constants.SERVICE_BACKGROUND_EXECUTOR = "background_executor"
Constants.SERVICE_BACKGROUND_EVENT_DISPATCHER = "background_event_dispatcher"
Constants.SERVICE_BACKGROUND_BROADCAST = "background_broadcast"
Constants.SERVICE_EVENT_MANAGER = "event_manager"
Constants.SERVICE_USER_MANAGER = "user_manager"
Constants.SERVICE_TASK = "task"
Constants.SERVICE_COMMAND_PROCESSOR = "command_processor"

Constants.PARM_TASK_ID = "task_id"
Constants.PARM_CURRENT_PATH = "current_path"

Constants.PARM_APP = "app"

Constants.QUEUE_BACKGROUND = "bamb_background_tasks"
Constants.QUEUE_PREFIX_FOR_BACKGROUND_EVENTS = "bamb_event_"
Constants.QUEUE_EVENTS = "bamb_events"

Constants.PARM_EVENT_TAG = "tag"
Constants.PARM_EVENT_ID = "id"
Constants.PARM_EVENT_DATA = "data"
Constants.PARM_EVENT_CMD = "cmd"

Constants.LISTENER_TASK = "task"

Constants.COMMAND_PREPARE_LISTENER_FOR_USER = "user_listener"