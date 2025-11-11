from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader


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
        
    def on_add_cliked(self):
        print("Add")

    def on_delete_cliked(self):
        print("Delete")

    def on_done_cliked(self):
        print("Done")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()