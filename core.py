# coding: utf-8
class CmdInteraction:
    def __init__(self):
        pass

    def execute(self, command):
        from subprocess import check_output
        return str(check_output(command.split()), encoding='utf-8')


class ExplorerInteraction:
    def __init__(self):
        pass

    def explore_working_directory(self):
        from os import getcwd, system
        system('explorer.exe {}'.format(getcwd()))


class GitInteraction:
    def __init__(self):
        pass

    def create_branch(self, branch_name):
        from subprocess import call
        call(['git', 'branch', branch_name])

    def checkout_branch(self, branch_name):
        from subprocess import call
        call(['git', 'checkout', branch_name])

    def rename_branch(self, old_name, new_name):
        from subprocess import call
        call(['git', 'branch', '-m', old_name, new_name])

    def new_commit_all(self, message):
        from subprocess import call
        call(['git', 'commit', '-a', '-m', '"{}"'.format(message)])

    def new_commit(self, file_name, message):
        from subprocess import call
        call(['git', 'commit', '"{}"'.format(file_name), '-m', '"{}"'.format(message)])

    def view_log(self):
        from subprocess import check_output
        return str(check_output(['git', 'log', '--all', '--graph']), encoding='utf-8')


class FileInteraction:
    def __init__(self):
        pass

    def read_file(self, file_name):
        with open(file_name, 'r') as file:
            text = file.read()
        return text
