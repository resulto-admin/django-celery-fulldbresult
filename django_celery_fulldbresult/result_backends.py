import json

from djcelery.backends.database import DatabaseBackend


class DatabaseResultBackend(DatabaseBackend):
    """Database backend that stores enough task metadata to retry the task.
    """

    def _store_result(self, task_id, result, status, traceback, request=None):
        if request:
            # TODO Use celery json serializer
            args = json.dumps(request.args)
            kwargs = json.dumps(request.kwargs)
            task = request.task
            expires = request.expires
            routing_key = request.delivery_info.get("routing_key")
            exchange = request.delivery_info.get("exchange")
            hostname = request.hostname
        else:
            args = []
            kwargs = {}
            task = ""
            expires = None
            routing_key = None
            exchange = None
            hostname = None
        self.TaskModel._default_manager.store_result(
            task_id, result, status,
            traceback=traceback, children=self.current_task_children(request),
            task=task, args=args, kwargs=kwargs, expires=expires,
            routing_key=routing_key, exchange=exchange, hostname=hostname)
        return result
