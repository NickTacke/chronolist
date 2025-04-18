import sys
import os
from PySide6.QtWidgets import QApplication
from models import Database
from views import MainWindow
from controllers import Controller
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

def main():
    app = QApplication(sys.argv)
    # set application name
    app.setApplicationName("ChronoList")
    # determine base path for assets (supports PyInstaller onefile mode)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    # load application and window icons
    icon_path = os.path.join(base_path, 'assets', 'logo.png')
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    home = os.path.expanduser("~")
    db_path = os.path.join(home, "todo_tracker.db")
    model = Database(db_path)
    view = MainWindow()
    controller = Controller(model, view)
    # ensure the main window also shows the icon
    view.setWindowIcon(app_icon)
    # UI refresh timer: update running task display every second
    refresh_timer = QTimer(view)
    refresh_timer.setInterval(1000)
    refresh_timer.timeout.connect(controller.on_timer_tick)
    refresh_timer.start()
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()