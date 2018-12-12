# coding: utf-8
import sys
from subprocess import call, check_output, Popen, PIPE, STDOUT
from PyQt5.QtWidgets import QInputDialog, QMessageBox

sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    # print(exctype, value, traceback)
    # sys._excepthook(exctype, value, traceback)
    return str(exctype) + str(value) + str(traceback)
    # sys.exit(1)


sys.excepthook = exception_hook


# class writer(object):
#     def write(self, data):
#         global err_str
#         err_str = ''
#         err_str += data
#
#
# sys.stderr = writer()


def output_to_plain_text(obj, messege):
    obj.console_output.appendPlainText(messege + '\n' + ('-' * 88) + '\n')


# def execute(obj, command):  # v1
#     import subprocess
#     try:
#         output_to_plain_text(obj, '>>{}\n'.format(command) +
#                              str(check_output(command.split(), shell=True), encoding='utf-8'))
#     except subprocess.CalledProcessError as e:
#         output_to_plain_text(obj, '>>{}\n'.format(command) + str(e))
#     except FileNotFoundError as fnfe:
#         output_to_plain_text(obj, '>>{}\n'.format(command) + str(fnfe))

def execute(obj, command):  # v2
    import subprocess
    try:
        result = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)  # with shell=True,
        result = result.stdout.read()                                    # FileNotFoundError is not displays
        output_to_plain_text(obj, '>>{}\n'.format(command) + str(result, encoding='utf-8'))
    except subprocess.CalledProcessError as e:
        output_to_plain_text(obj, '>>{}\n'.format(command) + 'CalledProcessError')
    except FileNotFoundError as fnfe:
        output_to_plain_text(obj, '>>{}\n'.format(command) + 'FileNotFoundError')


def explore_working_directory():
    from os import getcwd, system
    system('explorer.exe {}'.format(getcwd()))


def create_branch(widget):
    branch_name, okBtnPressed = QInputDialog.getText(
        widget, "Create Branch", "Enter branch name:"
    )
    if okBtnPressed:
        output_to_plain_text(widget, str(check_output(['git', 'branch', branch_name]), encoding='utf-8'))


def checkout_branch(widget):
    branch_name, okBtnPressed = QInputDialog.getText(
        widget, "Checkout Branch", "Enter branch name:"
    )
    if okBtnPressed:
        output_to_plain_text(widget, str(check_output(['git', 'checkout', branch_name]), encoding='utf-8'))


def rename_branch(widget):
    branch_name, okBtnPressed = QInputDialog.getText(
        widget, "Rename Branch", "Enter new branch name:"
    )
    if okBtnPressed:
        output_to_plain_text(widget, str(check_output(['git', 'checkout', branch_name]), encoding='utf-8'))


def new_commit_all(message):
    call(['git', 'commit', '-a', '-m', '"{}"'.format(message)])


def new_commit(file_name, message):
    call(['git', 'commit', '"{}"'.format(file_name), '-m', '"{}"'.format(message)])


def view_log(widget):
    QMessageBox.about(widget, 'Log View', str(check_output(['git', 'log', '--all', '--graph']), encoding='utf-8'))


def read_file(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    return text
