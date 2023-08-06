from functools import partial
from os import getcwd
from typing import Union, List, Iterable, Callable

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWidgets import QListView, QAbstractItemView, QTreeView


class App(QMainWindow):
    file_name = None
    close_later = pyqtSignal(name="close_later")

    def __init__(self, func):
        # noinspection PyArgumentList
        super(App, self).__init__()
        self.func = func
        self.close_later.connect(self.close)

    @pyqtSlot(name='show_ui')
    def show_ui(self):
        result = self.func(self)
        self.file_name = result if (isinstance(result, str) or isinstance(result, list)) else result[0]
        self.show()
        self.close_later.emit()


def _open_dialog(func: Callable[[], Union[List[str], str]]) -> Union[str, List[str]]:
    app = QApplication(list())
    window = App(func)
    # noinspection PyTypeChecker,PyCallByClass
    QTimer.singleShot(0, window.show_ui)
    app.exec_()
    return window.file_name


def _convert_filter(ext: Union[str, List[str]]) -> str:
    if isinstance(ext, str):
        return "{0} (*{1})".format(ext[1:], ext)
    elif isinstance(ext, Iterable):
        return ';;'.join("{0} (*{1})".format(x[1:], x) for x in ext)


def file_to_open(ext: Union[str, List[str]], default_dir: str=getcwd()) -> str:
    params = {'caption': "Open file", 'directory': default_dir, 'filter': _convert_filter(ext)}
    func = partial(QFileDialog.getOpenFileName, **params)
    return _open_dialog(func)


def files_to_open(ext: Union[str, List[str]], default_dir: str=getcwd()) -> List[str]:
    params = {'caption': "Open files", 'directory': default_dir, 'filter': _convert_filter(ext)}
    func = partial(QFileDialog.getOpenFileNames, **params)
    return _open_dialog(func)


def file_to_save(ext: Union[str, List[str]], default_dir: str=getcwd()) -> str:
    params = {'caption': "Save file", 'directory': default_dir, 'filter': _convert_filter(ext)}
    func = partial(QFileDialog.getSaveFileName, **params)
    return _open_dialog(func)


def folder_to_open(default_dir: str=getcwd()) -> str:
    params = {'caption': "Open folder", 'directory': default_dir}
    func = partial(QFileDialog.getExistingDirectory, **params)
    return _open_dialog(func)


def folder_to_save(default_dir: str=getcwd()) -> str:
    return file_to_save('.*', default_dir)


class MultiFolderApp(QMainWindow):
    file_names = None
    close_later = pyqtSignal(name="close_later")

    def __init__(self, default_dir: str, caption: str='Open folders'):
        # noinspection PyArgumentList
        super(MultiFolderApp, self).__init__()
        self.close_later.connect(self.close)
        self.caption = caption
        self.default_dir = default_dir

    @pyqtSlot(name="show_ui")
    def show_ui(self):
        file_dialog = QFileDialog(self, self.caption, self.default_dir)
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setDirectory(self.default_dir)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # to make it possible to select multiple directories:
        file_view.setSelectionMode(QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

        # execute the modified file dialog and return result
        self.close_later.emit()
        if file_dialog.exec():
            self.file_names = file_dialog.selectedFiles()


def folders_to_open(default_dir: str=getcwd()) -> Iterable[str]:
    app = QApplication(list())
    window = MultiFolderApp(default_dir)
    # noinspection PyTypeChecker,PyCallByClass
    QTimer.singleShot(0, window.show_ui)
    app.exec_()
    return window.file_names
