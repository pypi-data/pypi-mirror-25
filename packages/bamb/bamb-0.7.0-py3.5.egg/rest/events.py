from domain import base
import urllib3
from common import constants
from domain import exceptions
from bamb import Bamb
from bamb import Config
from service import event_service
from celery.exceptions import Retry


class EventRedirect(base.Listener):

    def on_event(self, e, queue=""):
        # TODO determine the user id from queue name, post event when user's websocket is available.
        # otherwise raise Retry (need insert task to the top of the queue)
        user_id = queue[len(constants.QUEUE_PREFIX_FOR_BACKGROUND_EVENTS):]
        if len(user_id) == 0:
            raise exceptions.IllegalArgumentException("can not determine user id from queue name : " + queue)
        conf = Bamb.singleton().conf
        if not isinstance(conf, Config):
            raise exceptions.AppException("app is not configured !")
        url = conf.SERVER_PATH + "events/" + user_id
        params = str(e)
        headers = {"Content-type":"application/json", "Accept": "application/json"}
        http = urllib3.PoolManager()
        r = http.request("POST", url, params, headers)
        if r.status != 200:
            # TODO stop consuming from the worker, and then retry the task
            #raise Retry("event post failed for user " + user_id + ", try again.")
            pass
