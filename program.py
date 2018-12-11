import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import core
from ui_file import Ui_MainWindow


class GitCustomGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.console_input.returnPressed.connect(self.execute_command)
        self.actionExplore_Working_Directory.triggered.connect(core.explore_working_directory)
        self.actionCreate.triggered.connect(self.create_branch)
        self.actionCheckout.triggered.connect(self.checkout_branch)

    def checkout_branch(self):
        core.checkout_branch(self)

    def create_branch(self):
        core.create_branch(self)

    def execute_command(self):
        core.execute(self, self.console_input.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GitCustomGui()
    gui.show()
    sys.exit(app.exec_())
