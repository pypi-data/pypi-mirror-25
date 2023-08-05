from __future__ import absolute_import, unicode_literals
import importlib
import sys
from web import settings
from domain import base
from domain import task
from django.test import TestCase
from bamb import Bamb
from common import constants
from service import task_service
from service import event_service


class TaskTest(TestCase):

    def setUp(self):
        importlib.import_module("celery", "web")

    def tearDown(self):
        pass

    def test_single_native_operation(self):

        t = self.build_single_target_operation()
        ts = Bamb.bean(constants.SERVICE_TASK)
        self.assertTrue(isinstance(ts, task_service.TaskService))
        ts.save(t)
        task_id = t.task_id
        ts.run(t)
        t = ts.load(task_id)
        self.assertTrue(t.state == constants.STATE_FINISHED)

    def test_multi_native_operation(self):

        t = self.build_hierarchical_target_operation()
        ts = Bamb.bean(constants.SERVICE_TASK)
        self.assertTrue(isinstance(ts, task_service.TaskService))
        ts.save(t)
        task_id = t.task_id
        ts.run(t)
        t = ts.load(task_id)
        self.assertTrue(t.state == constants.STATE_FINISHED)

    def test_multi_background_operation(self):

        t = self.build_hierarchical_target_operation(True)
        ts = Bamb.bean(constants.SERVICE_TASK)
        self.assertTrue(isinstance(ts, task_service.TaskService))
        ts.save(t)
        task_id = t.task_id

        em = Bamb.bean(constants.SERVICE_EVENT_MANAGER)
        if not isinstance(em, event_service.EventManager):
            raise RuntimeError("can not get event manager")
        cmd = base.Event(source_tag=None, event_id=constants.EVENT_ID_BROADCAST_COMMAND,
                         data={"user_id": "test", "listener": "service.simple.SimpleEventConsumer"})
        cmd.command = constants.COMMAND_PREPARE_LISTENER_FOR_USER
        em.send_broadcast(cmd)

        ts.run(t)
        t = ts.load(task_id)
        if not isinstance(t, task.Task):
            self.fail("invalid task!")
        self.assertTrue(t.state == constants.STATE_FINISHED)
        r = t.get_all_result()
        self.assertTrue(r.state == constants.MASK_RESULT_SUCCESS)

    def test_complex_background_task(self):

        t = self.build_complex_task(True)
        ts = Bamb.bean(constants.SERVICE_TASK)
        self.assertTrue(isinstance(ts, task_service.TaskService))
        ts.save(t)
        task_id = t.task_id

        ts.run(t)
        t = ts.load(task_id)
        if not isinstance(t, task.Task):
            self.fail("invalid task!")
        self.assertTrue(t.state == constants.STATE_FINISHED)
        r = t.get_all_result()
        self.assertTrue(r.state == constants.MASK_RESULT_PARTIAL_SUCCESS)
        self.assertEqual(len(t.child([0]).lt_children), 3)
        self.assertEqual(len(t.child([1]).lt_children), 2)

    def build_single_target_operation(self, background=False):

        t = task.Task("single operation")
        t._id = "59a772c81d41c81d3707c181"
        tg = base.Target()
        tg.ip = "192.168.0.1"

        t.target = tg
        t.executor_name = "simple"
        if background:
            t.native_execution = False
        return t

    def build_hierarchical_target_operation(self, background=False):

        t = task.Task("multi target operation")
        t._id = "51a402c81813c81d3915d240"
        tg = base.Target(init_list=[base.Target(ip="192.168.1.1"),
                                           base.Target(ip="192.168.1.2")])
        t.target = tg
        t.executor_name = "simple"
        if background:
            t.native_execution = False
        return t

    def build_complex_task(self, background=False):

        t = task.Task("A COMPLEX TASK")
        t._id = "16a982c10864a1073925cf29"
        tg = base.Target(init_list=[base.Target(ip="192.168.3.1"),
                                    base.Target(ip="192.168.3.2"),
                                    base.Target(ip="192.168.3.3")])
        t.target = tg
        t.native_execution = (not background)

        o1 = task.Task("OPERATION 1")
        o1.executor_name = "simple"
        o1.native_execution = (not background)

        o2 = task.Task("OPERATION 2")
        o2.target = "$LAST.SUCC.TARGET"
        o2.executor_name = "simple"
        o2.native_execution = (not background)

        t.lt_extend_children([o1, o2])

        return t


