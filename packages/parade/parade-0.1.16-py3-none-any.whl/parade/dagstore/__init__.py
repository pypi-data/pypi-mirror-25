from ..core.task import Task
from ..utils.log import logger


class DAGStore(object):
    """
    The dagstore to support task-flow scheduling
    """

    @staticmethod
    def parse_forests(*tasks):
        """
        util method to build flow forest
        :param tasks: the specified tasks to form the flow
        :return: the tasks are not dependent by others
        """
        task_roots = dict()
        try:
            for task in tasks:
                assert isinstance(task, Task), 'Invalid task-module [{}] provided'.format(task.__class__.__name__)
                for dep in task.deps:
                    task_roots[dep] = task.name
        except RuntimeError as e:
            logger.exception(str(e))

        forests = list(filter(lambda x: x.name not in task_roots, tasks))
        logger.debug('Task forests generated [{}]'.format(', '.join(map(lambda x: x.name, forests))))
        return forests

    def create(self, *tasks, cron=None, dag_key=None):
        """
        schedule the task-flow
        :param dag_key: the flow name
        :param cron: the cron string to schedule the flow
        :return:
        """
        raise NotImplementedError

    def delete(self, flow_name):
        """
        unschedule the task-flow
        :param flow_name: the flow name
        :return:
        """
        pass

    def __init__(self, context):
        self.context = context
