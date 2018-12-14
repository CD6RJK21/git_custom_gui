# git custom gui
Программа представляет собой графический интерфейс для управления репозиториями. Основное отличие от встроенного графаческого интерфейса git-gui - наличие консоли для ручного ввода команд.
# Возможности
Выбор рабочей папки; показ истории репозитория; создание, переключение и переименование веток; просмотр изменений в файлах со времени последнего коммита; коммит для всех файлов или для определённых; использование консоли для выполнения команд.
# Файлы
    core.py     содержит функции для работы программы
    ui_file.py  файл с интерфейсом
    program.py  связывает два предыдущих файла и организизует выполнение программы 
# Необходимые программы
* python 3.6
* git
# И библиотеки
* PyQt5
* subprocess
* os
* sys
