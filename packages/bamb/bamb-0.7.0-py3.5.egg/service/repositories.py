class CrudRepository(object):

    def __init__(self, app=None, *args, **kwargs):
        pass

    @property
    def table_name(self):
        return ""

    def load(self, key, *args, **kwargs):
        return None

    def delete(self, key, *args, **kwargs):
        return None

    def save(self, obj, key, *args, **kwargs):
        return None


class TaskRepository(CrudRepository):

    @property
    def table_name(self):
        return "tasks"

