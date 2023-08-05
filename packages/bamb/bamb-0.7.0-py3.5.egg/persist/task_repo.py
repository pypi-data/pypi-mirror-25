from service import repositories
from persist import simple_repository


class TaskRepositoryImpl(simple_repository.SimpleMongoDbRepository, repositories.TaskRepository):

    def __init__(self, app=None):
        simple_repository.SimpleMongoDbRepository.__init__(self, app=app)

    @property
    def table_name(self):
        return "tasks"
