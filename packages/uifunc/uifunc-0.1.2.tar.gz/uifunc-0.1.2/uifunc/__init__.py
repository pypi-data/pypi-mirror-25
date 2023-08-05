# provide decorators for functions that reads a folder/file name/list as the only argument
import sys
from typing import Callable, Optional, TypeVar

try:
    from .wxopen import *
    multi_folder = False
except ImportError:
    from .tkopen import *
    multi_folder = True


T = TypeVar('T')


class FolderSelector(object):  # Folder(s)Selector doesn't take arguments, so the init argument is the callable
    __func__ = folder_to_open

    def __init__(self, func: Callable[[str], T]):
        self.func = func

    def __call__(self)-> T:
        folder = type(self).__func__() if len(sys.argv) == 1 else sys.argv[1]
        return self.func(folder)


class SaveFolderSelector(FolderSelector):
    __func__ = folder_to_save


class FoldersSelector(object):
    def __init__(self, func: Callable[[List[str]], T]):
        self.func = func
        if not multi_folder:
            raise ImportError("multi-folder selection require wxPython!")

    def __call__(self) -> T:
        folders = folders_to_open() if len(sys.argv) == 1 else sys.argv[1:]
        return self.func(folders)


class FilesSelector(object):
    __func__ = files_to_open

    def __init__(self, filters: Optional[List[str]]=None):
        self.filters = filters

    def __call__(self, func: Callable[[List[str]], T]) -> Callable[[], T]:
        def temp():
            filters = self.filters
            if len(sys.argv) > 1:
                filters = sys.argv[1:]
            elif filters and filters[0].startswith('.'):
                filters = type(self).__func__(filters)
            elif filters is None:
                raise ValueError("supply a list of files or file filters in argument or command line arguments")
            return func(filters)
        return temp


class FileSelector(object):
    __func__  = file_to_open

    def __init__(self, filters: Optional[List[str]]=None):
        self.filters = filters

    def __call__(self, func: Callable[[str], T]) -> Callable[[], T]:
        def temp():
            filters = self.filters
            if len(sys.argv) == 2:
                filters = sys.argv[1]
            elif filters and filters[0].startswith('.'):
                filters = type(self).__func__(filters)
            elif filters is None:
                raise ValueError("supply a list of files or file filters in argument or command line arguments")
            return func(filters)
        return temp


class SaveSelector(FilesSelector):
    __func__ = file_to_save
