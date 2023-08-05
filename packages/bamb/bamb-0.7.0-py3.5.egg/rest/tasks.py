from __future__ import absolute_import
from celery import shared_task
from celery import current_app as app
from domain import base
from bamb import Bamb
from domain import base as ab
from common import constants
from service import task_service
from common import constants
from domain import task
from domain import exceptions
from service import event_service
from celery import task as ct


@shared_task(queue=constants.QUEUE_BACKGROUND, bind=True)
def execute_on_target(self, executor_name, target_dict, parm_dict):
    executor = Bamb.bean(executor_name, singleton=False)
    if not isinstance(executor, ab.Invokable):
        return
    tg = ab.EasySerializable.es_load(target_dict)
    if not isinstance(tg, base.Target):
        print("no target specified for execution of " + executor_name)
        return
    parm = ab.EasySerializable.es_load(parm_dict)
    ts = Bamb.bean(constants.SERVICE_TASK)
    if not isinstance(ts, task_service.TaskService):
        return
    task_id = parm[constants.PARM_TASK_ID].value
    path = parm[constants.PARM_CURRENT_PATH].value
    root = ts.load(task_id)
    if not isinstance(root, task.Task):
        raise exceptions.FailedToLoadException("can not load task : " + task_id)
    t = root.child(path)
    if not isinstance(t, task.Task):
        raise exceptions.AppException("can not find the child task: " + task_id + str(path))
    executor.target = tg
    executor.parameters = parm
    executor.invoke()
    t.result = base.Result(executor)
    t.state = constants.STATE_FINISHED
    ts.save(t)
    # TODO django-celery not support celery 4.0, we could not send a progress to main process
    #e = base.Event()
    #e.event_id = constants.EVENT_ID_TASK_STATE_CHANGED
    #e.source_tag = root.task_id + str(t.lt_path())
    #e.data = t.result.es_to_dict()
    #self.update_state(state="PROGRESS", meta=e)
    return


@shared_task(queue=constants.QUEUE_EVENTS, ignore_result=True)
def background_dispatch(e, queue_name, callback_service_name, *args, **kwargs):
    s = background_dispatch_queued.s(e, callback_service_name)
    s.delay(queue=queue_name)


@shared_task(ignore_result=True)
def background_dispatch_queued(e, callback_service_name, *args, **kwargs):
    callback = Bamb.bean(callback_service_name)
    if not isinstance(callback, base.Listener):
        raise exceptions.IllegalArgumentException("can not find the callback service : " + str(callback_service_name))
    callback.on_event(e)


@shared_task(queue=constants.QUEUE_BACKGROUND, ignore_result=True)
def background_broadcast_send(e_dict):
    e = base.Event(init_dict=e_dict)
    em = Bamb.bean(constants.SERVICE_EVENT_MANAGER)
    if not isinstance(em, event_service.EventManager):
        raise exceptions.AppException("can not get event manager!")
    em.dispatch(e)

