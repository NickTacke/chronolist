import datetime
from PySide6.QtCore import QObject

class Controller(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.current_log_id = None
        self.running = False
        self.current_task_id = None
        self.start_time = None

        self.view.add_task.connect(self.on_add_task)
        self.view.edit_task.connect(self.on_edit_task)
        self.view.delete_task.connect(self.on_delete_task)
        self.view.start_stop.connect(self.on_start_stop)

        self.load_tasks()
        running_timer = self.model.get_running_timer()
        if running_timer:
            self.current_log_id = running_timer['id']
            self.current_task_id = running_timer['task_id']
            self.start_time = datetime.datetime.strptime(
                running_timer['start_time'], '%Y-%m-%d %H:%M:%S'
            )
            self.running = True
            self.view.update_start_stop(True)
            # initial UI update; periodic refresh handled in main
            self.on_timer_tick()
        else:
            self.view.update_start_stop(False)

    def load_tasks(self):
        tasks = self.model.get_tasks()
        self.view.set_task_list(tasks)

    def on_add_task(self):
        name = self.view.prompt_task_name()
        if name:
            self.model.add_task(name)
            self.load_tasks()

    def on_edit_task(self):
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            return
        tasks = self.model.get_tasks()
        current = next((t for t in tasks if t['id'] == task_id), None)
        if not current:
            return
        new_name = self.view.prompt_task_name(current['name'])
        if new_name:
            self.model.update_task(task_id, new_name)
            self.load_tasks()

    def on_delete_task(self):
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            return
        tasks = self.model.get_tasks()
        current = next((t for t in tasks if t['id'] == task_id), None)
        if not current:
            return
        if self.view.confirm_delete(current['name']):
            self.model.delete_task(task_id)
            self.load_tasks()

    def on_start_stop(self):
        if self.running:
            self.model.stop_timer(self.current_log_id)
            self.current_log_id = None
            self.running = False
            self.view.update_start_stop(False)
            # UI refresh will continue, but no elapsed is added when not running
            self.load_tasks()
        else:
            task_id = self.view.get_selected_task_id()
            if task_id is None:
                return
            log_id = self.model.start_timer(task_id)
            if log_id:
                self.current_log_id = log_id
                self.current_task_id = task_id
                self.start_time = datetime.datetime.now()
                self.running = True
                self.view.update_start_stop(True)
                # immediate UI update; periodic refresh handled in main
                self.on_timer_tick()
    
    def on_timer_tick(self):
        tasks = self.model.get_tasks()
        if self.running and self.current_task_id is not None and self.start_time:
            elapsed = int((datetime.datetime.now() - self.start_time).total_seconds())
            for t in tasks:
                if t['id'] == self.current_task_id:
                    t['total_seconds'] += elapsed
                    break
        self.view.set_task_list(tasks)