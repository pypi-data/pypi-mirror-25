from persist import task_repo
from common import constants
from rest import background

beans = {
    constants.SERVICE_BACKGROUND_EXECUTOR: background.BackgroundExecutorImpl,
    constants.SERVICE_BACKGROUND_EVENT_DISPATCHER: background.BackgroundEventDispatcher,
    constants.SERVICE_BACKGROUND_BROADCAST: background.BackgroundBroadcastDeliver,
}