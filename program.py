# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

import core
from ui_file import Ui_MainWindow


class GitCustomGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.display_current_branch()
        self.refresh_tracked_files()
        self.run()

    def run(self):
        self.console_input.returnPressed.connect(self.execute_command)
        self.actionExplore_Working_Directory.triggered.connect(core.explore_working_directory)
        self.actionCreate.triggered.connect(self.create_branch)
        self.actionCheckout.triggered.connect(self.checkout_branch)
        self.actionRename.triggered.connect(self.rename_branch)
        self.actionView_Log.triggered.connect(self.view_log)  # too height window
        self.commitButton.clicked.connect(self.commit)
        self.actionSelect_Working_Directory.triggered.connect(self.select_working_directory)
        self.comboBox.activated[str].connect(self.view_file)
        self.pushButton.clicked.connect(self.refresh)
        self.commit_all.toggled.connect(self.display_commit_one_file)
        self.commit_one_file.toggled.connect(self.display_commit_one_file)

    def display_commit_one_file(self):
        if self.commit_one_file.isChecked():
            self.commit_one_file_name.show()
            self.label_commit_one_file.show()
        else:
            self.commit_one_file_name.hide()
            self.label_commit_one_file.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.refresh()

    def refresh(self):
        self.display_current_branch()
        self.refresh_tracked_files()
        self.view_file(self.comboBox.currentText())

    def view_file(self, file_name):
        self.label_3.setText('File: {}'.format(file_name))
        core.view_file(self, file_name)

    def refresh_tracked_files(self):
        core.refresh_tracked_files(self)

    def display_current_branch(self):
        self.current_branch.setText('Current Branch: {}'.format(core.current_branch_name()))

    def select_working_directory(self):
        core.select_working_directory(self)
        self.refresh()

    def view_log(self):
        core.view_log()

    def commit(self):
        if self.commit_all.isChecked:
            core.commit_all(self, self.commitMessege.toPlainText())
        else:
            core.commit(self, self.commit_one_file_name.text(), self.commitMessege.toPlainText())
        self.refresh()

    def rename_branch(self):
        core.rename_current_branch(self)
        self.refresh()

    def checkout_branch(self):
        core.checkout_branch(self)
        self.refresh()

    def create_branch(self):
        core.create_branch(self)

    def execute_command(self):
        core.execute(self, self.console_input.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GitCustomGui()
    gui.show()
    sys.exit(app.exec_())
