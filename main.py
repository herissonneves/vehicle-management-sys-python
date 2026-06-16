import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from gui.main_window import VehicleManagerApp
from services.database import init_db


def main() -> None:
    def excepthook(exc_type, exc_value, exc_tb):
        print("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    try:
        init_db()
    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"Could not initialize the database:\n{e}")
        sys.exit(1)

    window = VehicleManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
