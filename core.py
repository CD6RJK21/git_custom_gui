# coding: utf-8
import sys
from subprocess import Popen, PIPE, STDOUT

from PyQt5.QtWidgets import QInputDialog, QMessageBox, QFileDialog

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    return str(exctype) + str(value) + str(traceback)


sys.excepthook = exception_hook


def output_to_plain_text(obj, messege):
    obj.console_output.appendPlainText(messege + '\n' + ('-' * 52) + '\n')


def execute(obj, command):  # v2
    import subprocess
    try:
        result = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)  # with shell=True,
        result = result.stdout.read()  # FileNotFoundError is not displays
        output_to_plain_text(obj, '>>{}\n'.format(command) + str(result, encoding='utf-8'))
    except subprocess.CalledProcessError as e:
        output_to_plain_text(obj, '>>{}\n'.format(command) + 'CalledProcessError')
    except FileNotFoundError as fnfe:
        output_to_plain_text(obj, '>>{}\n'.format(command) + 'FileNotFoundError')
    except BaseException as be:
        output_to_plain_text(obj, '>>{}\n'.format(command) + str(be))


def explore_working_directory():
    from os import getcwd, system
    system('explorer.exe {}'.format(getcwd()))


def create_branch(widget):
    branch_name, okBtnPressed = QInputDialog.getText(
        widget, "Create Branch", "Enter branch name:"
    )
    if okBtnPressed:
        reply = Popen('git branch {}'.format(branch_name), shell=True, stdout=PIPE, stderr=STDOUT)
        reply = str(reply.stdout.read(), encoding='utf-8')
        output_to_plain_text(widget, 'Created new branch')


def checkout_branch(widget):
    names = Popen(' '.join(['git', 'branch']), shell=True, stdout=PIPE, stderr=STDOUT)
    names = str(names.stdout.read(), encoding='utf-8').split('\n')
    names1 = []
    for name in names:
        if name.startswith('*'):
            name = name[1:]
        name = name.strip()
        if name != '':
            names1.append(name)
    names = tuple(names1)
    branch_name, okBtnPressed = QInputDialog.getItem(
        widget, "Checkout Branch", "Select branch :", names, 1
    )
    if okBtnPressed:
        reply = Popen(' '.join(['git', 'checkout', branch_name]), shell=True, stdout=PIPE, stderr=STDOUT)
        reply = str(reply.stdout.read(), encoding='utf-8')
        output_to_plain_text(widget, reply)


def rename_current_branch(widget):
    branch_name, okBtnPressed = QInputDialog.getText(
        widget, "Rename Current Branch", "Enter new branch name:"
    )
    if okBtnPressed:
        reply = Popen(' '.join(['git', 'branch', '-m', branch_name]), shell=True, stdout=PIPE, stderr=STDOUT)
        reply = str(reply.stdout.read(), encoding='utf-8')
        output_to_plain_text(widget, reply)


def commit_all(widget, message):
    reply = Popen(' '.join(['git', 'commit', '-a', '-m', '"{}"'.format(message)]), shell=True, stdout=PIPE,
                  stderr=STDOUT)
    reply = str(reply.stdout.read(), encoding='utf-8')
    output_to_plain_text(widget, reply)


def commit(widget, file_name, message):
    reply = Popen(' '.join(['git', 'commit', '"{}"'.format(file_name), '-m', '"{}"'.format(message)]), shell=True,
                  stdout=PIPE, stderr=STDOUT)
    reply = str(reply.stdout.read(), encoding='utf-8')
    output_to_plain_text(widget, reply)


def select_working_directory(widget):
    from os import chdir
    try:
        path = QFileDialog.getExistingDirectory(widget, "Select Working Directory", "")
        chdir(path)
    except BaseException as be:
        # QMessageBox.warning(widget, 'Warning', 'Error: {}'.format(str(be)))
        pass


def current_branch_name():
    names = Popen(' '.join(['git', 'branch']), shell=True, stdout=PIPE, stderr=STDOUT)
    names = str(names.stdout.read(), encoding='utf-8').split('\n')
    names1 = ''
    for name in names:
        if name.startswith('*'):
            name = name[1:].strip()
            names1 = name[:]
    return names1


def refresh_tracked_files(widget):
    # names = Popen('git ls-tree --full-tree -r --name-only HEAD', shell=True, stdout=PIPE, stderr=STDOUT)
    names = Popen('git ls-files -m', shell=True, stdout=PIPE, stderr=STDOUT)
    names = str(names.stdout.read(), encoding='utf-8').split('\n')
    names1 = []
    for name in names:
        if name.startswith('*'):
            name = name[1:]
        if not name == '':
            names1.append(name.strip())
    widget.comboBox.clear()
    widget.comboBox.addItems(names1)


def view_file(widget, file_name):
    reply = Popen(' '.join(['git', 'diff', '"{}"'.format(file_name)]), shell=True, stdout=PIPE, stderr=PIPE)
    reply = str(reply.stdout.read(), encoding='utf-8')
    widget.plainTextEdit_2.setPlainText(reply)


def view_log(widget):
    reply = Popen(' '.join(['git', 'log', '--all', '--graph']), shell=True, stdout=PIPE, stderr=STDOUT)
    reply = str(reply.stdout.read(), encoding='utf-8')
    log = ScrollMessageBox(QMessageBox.Critical, "Log View", reply)


def read_file(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    return text


class ScrollMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        from PyQt5.QtWidgets import QScrollArea, QGridLayout, QLabel
        QMessageBox.__init__(self, *args, **kwargs)
        chldn = self.children()
        scrll = QScrollArea(self)
        scrll.setWidgetResizable(True)
        grd = self.findChild(QGridLayout)
        lbl = QLabel(chldn[1].text(), self)
        lbl.setWordWrap(True)
        scrll.setWidget(lbl)
        scrll.setMinimumSize(400, 600)
        grd.addWidget(scrll, 0, 1)
        chldn[1].setText('')
        self.exec_()
