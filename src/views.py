from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QInputDialog, QMessageBox, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt, Signal

class MainWindow(QMainWindow):
    add_task = Signal()
    edit_task = Signal()
    delete_task = Signal()
    start_stop = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChronoList")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # table: Task name, total time, last start, last end
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Task", "Time", "Start", "End"])
        self.table.verticalHeader().setVisible(False)
        # selection behavior and edit triggers
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # disable scrollbars and stretch all columns to available width
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.btn_add = QPushButton("Add Task")
        self.btn_edit = QPushButton("Edit Task")
        self.btn_delete = QPushButton("Delete Task")
        self.btn_start_stop = QPushButton("Start")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_start_stop)

        self.btn_add.clicked.connect(self.add_task.emit)
        self.btn_edit.clicked.connect(self.edit_task.emit)
        self.btn_delete.clicked.connect(self.delete_task.emit)
        self.btn_start_stop.clicked.connect(self.start_stop.emit)

    def set_task_list(self, tasks):
        self.table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            # Task name
            item_name = QTableWidgetItem(task['name'])
            item_name.setData(Qt.UserRole, task['id'])
            self.table.setItem(row, 0, item_name)
            # Total elapsed time
            time_str = self.seconds_to_hms(task['total_seconds'])
            self.table.setItem(row, 1, QTableWidgetItem(time_str))
            # Last start and end times
            start = task.get('last_start') or ""
            end = task.get('last_end') or ""
            self.table.setItem(row, 2, QTableWidgetItem(start))
            self.table.setItem(row, 3, QTableWidgetItem(end))

    def get_selected_task_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            return None
        item = self.table.item(selected, 0)
        return item.data(Qt.UserRole)

    def prompt_task_name(self, default_text=""):
        text, ok = QInputDialog.getText(self, "Task Name", "Enter task name:", text=default_text)
        if ok and text.strip():
            return text.strip()
        return None

    def confirm_delete(self, task_name):
        reply = QMessageBox.question(
            self, "Delete Task",
            f"Are you sure you want to delete '{task_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def update_start_stop(self, running):
        if running:
            self.btn_start_stop.setText("Stop")
        else:
            self.btn_start_stop.setText("Start")

    @staticmethod
    def seconds_to_hms(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"