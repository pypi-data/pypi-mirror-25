from service import task_service
from service import salt
from service import simple
from common import constants
from service import event_service
from service import user_service
from service import command_service


beans = {
    constants.SERVICE_TASK: task_service.TaskService,
    "simple": simple.SimpleNativeExecutor,
    constants.SERVICE_EVENT_MANAGER: event_service.EventManager,
    constants.SERVICE_USER_MANAGER: user_service.UserManager,
    constants.SERVICE_COMMAND_PROCESSOR: command_service.Processor,
}