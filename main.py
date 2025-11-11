from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PySide6.QtUiTools import QUiLoader
from database import session, Task

def refresh_table(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.load_tasks()
        return result
    return wrapper

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("main_window.ui", None)
        #Window settings
        self.setCentralWidget(self.ui)
        self.setFixedSize(520, 350)
        self.setWindowTitle("To do")
        #Binds
        self.ui.addButton.clicked.connect(self.on_add_cliked)
        self.ui.deleteButton.clicked.connect(self.on_delete_cliked)
        self.ui.doneButton.clicked.connect(self.on_done_cliked)

        self.load_tasks()

    @refresh_table    
    def on_add_cliked(self):
        print("Add")

    @refresh_table
    def on_delete_cliked(self):
        task = self._get_task()
        if task:
            session.delete(task)
            session.commit()

    @refresh_table
    def on_done_cliked(self):
        task = self._get_task()
        if task:
            task.done = True
            session.commit()

    def _get_task(self):
        row = self.ui.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Choose task")
            return
        
        task_id_item = self.ui.tableWidget.item(row, 0)
        task_id = int(task_id_item.text())
        task = session.query(Task).get(task_id)
        return task

    def load_tasks(self):
        self.ui.tableWidget.setRowCount(0)

        tasks = session.query(Task).all()
        for task in tasks:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)

            #Id
            id_item = QTableWidgetItem(str(task.id))
            self.ui.tableWidget.setItem(row, 0, id_item)
            #Name
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(task.name))
            #Description
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(task.description))
            #Due date
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(task.due_date)))
            #Priority
            priority_map = {1: "Low", 2: "Medium", 3: "High"}
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(priority_map.get(task.priority)))
            #Done?
            task_status = "✔" if task.done else "✖"
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(task_status))

        self.ui.tableWidget.hideColumn(0)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()