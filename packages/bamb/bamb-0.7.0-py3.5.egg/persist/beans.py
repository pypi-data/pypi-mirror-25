from service.repositories import TaskRepository
from persist import task_repo

beans = {
    TaskRepository: task_repo.TaskRepositoryImpl
}