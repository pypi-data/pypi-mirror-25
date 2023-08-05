import bamb
from domain import base


from domain import exceptions
from bamb import Bamb
from common import constants

import bson
from domain import task
from . import repositories
from . import utils
from . import built_in_executors as be

class TaskService:

    def load(self, task_id):
        return self.repo.load(task_id)

    def save(self, t, key=None):
        if isinstance(t, task.Task):
            task_id = self.repo.save(t, key)
            if isinstance(task_id, bson.ObjectId):
                t._id = task_id.__str__()

    def run(self, t, target=None, parm=None):
        if not isinstance(t, task.Task):
            raise exceptions.IllegalArgumentException("it is not a task instance!")
        if t.is_root:
            if t.current_path is None:
                # this is the first running of root task
                ctx = task.Context()
                ctx.target = target
                ctx.parameters = parm
                t.context = ctx
                t.mark_operations()
                last_op = None
            else:
                ctx = t.context
                last_op = t.current_operation()
        else:
            raise exceptions.IllegalOperationException("this method is only applicable for root task")

        op = t.fetch_next_operation()
        if t.is_root:
            self.repo.save(t)

        if op is not None:
            self.execute(op, ctx, last_op)

        # TODO : on task finished

    # foreground

    def execute(self, op, ctx, last_op):
        if not isinstance(op, task.Task):
            raise exceptions.IllegalArgumentException("operation is not an instance of task!")
        target = self.get_target(op, ctx, last_op)
        parameters = self.get_parameters(op, ctx, last_op)
        op.target = target
        op.parameters = parameters

        # check whether the operation can roll out

        executor = Bamb.bean(op.executor_name)
        if executor is None:
            raise exceptions.NotFoundException("can not find the executor : " + op.executor_name)
        if not isinstance(executor, base.Invokable):
            raise exceptions.InvalidTypeException("invalid type of executor : " + op.executor_name)
        if target is None:
            if executor.is_target_sensitive:
                return

        if op.is_leaf:
            op.state = constants.STATE_RUNNING
        p = base.Parameter(parm_name=constants.PARM_TASK_ID, parm_value=op.lt_root().object_id)
        parameters[constants.PARM_TASK_ID] = p
        p = base.Parameter(parm_name=constants.PARM_CURRENT_PATH, parm_value=op.lt_path())
        parameters[constants.PARM_CURRENT_PATH] = p

        # TODO : more information can be passed in parameters, e.g context, last operation.

        if not op.is_runtime_task:
            op.insert_atom_operations()

        executor = self.background_executor
        if not isinstance(executor, be.BackgroundExecutor):
            raise exceptions.AppException("injection of background executor is invalid!'")
        if isinstance(target, base.EasySerializable):
            target_dict = target.es_to_dict()
        else:
            target_dict = None
        if not op.is_runtime_task:
            self.repo.save(op)
        executor.execute(op.executor_name, target_dict, base.EasySerializable.es_any_to_primary(parameters), eager=op.native_execution)

    def get_target(self, op, ctx, last_op):
        if isinstance(op.target, str):
            target = self.parse(op, ctx, last_op, op.target)
            return target
        else:
            target = op.target
            if target is None:
                if isinstance(ctx, task.Context):
                    target = ctx.target
            if target is None:
                root = op.lt_root()
                target = root.target
            return target

    def get_parameters(self, op, ctx, last_op):
        if op.parameters is None:
            op.parameters = {}
        for k, p in op.parameters.items():
            if not p.value_available:
                p.value = self.parse(op, ctx, last_op, p.expression)
        return op.parameters

    def parse(self, op, ctx, last_op, expr):
        if len(expr) > 0:
            if expr[0:6] == "$LAST.":
                r = None
                if isinstance(last_op, task.Task):
                    r = last_op.get_all_result()
                if r is None:
                    return None
                if expr[len(expr)-7:] == ".TARGET":
                    if expr == "$LAST.SUCC.TARGET":
                        result_state = constants.MASK_RESULT_SUCCESS
                    else:
                        result_state = constants.MASK_RESULT_FAILED
                    t = last_op.target.lt_copy(matcher=task.TaskMatchers.result_state_matcher, match_with=r, result_state=result_state)
                    return t
            return None
        else:
            if isinstance(op, task.Task):
                return op.target
        return None

    @property
    @bamb.auto_wired(repositories.TaskRepository)
    def repo(self):
        return None

    @property
    @bamb.auto_wired(constants.SERVICE_BACKGROUND_EXECUTOR)
    def background_executor(self):
        return None
