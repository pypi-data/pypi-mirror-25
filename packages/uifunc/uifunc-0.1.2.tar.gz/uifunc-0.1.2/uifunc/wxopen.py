from enum import Enum
from os import getcwd
from os.path import expanduser
from typing import Union, List, Iterable

try:
    # noinspection PyPackageRequirements
    import wx
    # noinspection PyPackageRequirements
    from wx.lib.agw import multidirdialog as mdd
except ImportError:
    wx, mdd = None, None
    raise ImportError('install wx to use wx ui functions')

# noinspection PyArgumentList
DialogStyle = Enum('DialogStyle', 'open save multiple')

_file_dialog_style = {DialogStyle.open: wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                      DialogStyle.save: wx.FD_SAVE,
                      DialogStyle.multiple: wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST}


def _select_item(dialog, style: DialogStyle) -> Union[str, List[str]]:
    dialog.SetSize(0, 0, 200, 50)
    result = dialog.ShowModal()
    if result == wx.ID_CANCEL:
        raise KeyboardInterrupt
    if style == DialogStyle.multiple:
        chosen_path = dialog.GetPaths()
    else:
        chosen_path = dialog.GetPath() if hasattr(dialog, 'GetPath') else dialog.GetPaths()[0]
    dialog.Destroy()
    return chosen_path


def file_to_open(ext: Union[str, List[str]] = "", default_dir: str = getcwd(),
                 style: DialogStyle = DialogStyle.open) -> Union[str, List[str]]:
    if isinstance(ext, str):
        wildcard = "{0}|*{1}".format(ext[1:], ext)  # no space between pipe and wildcard
    elif isinstance(ext, list) or isinstance(ext, tuple):  # Default (*) | * would not give anything
        wildcard = "{0}|{1}".format(ext[0][1:], ';'.join('*' + x for x in ext))
    else:
        raise ValueError('file filter error: ' + str(ext))
    _ = wx.App()
    open_file_dialog = wx.FileDialog(None, "Select File", defaultDir=default_dir, wildcard=wildcard,
                                     style=_file_dialog_style[style])
    return _select_item(open_file_dialog, style)


def files_to_open(ext: Union[str, List[str]] = "", default_dir: str = getcwd()) -> List[str]:
    return file_to_open(ext, default_dir, DialogStyle.multiple)


def file_to_save(ext: Union[str, List[str]] = "", default_dir: str = getcwd()) -> str:
    return file_to_open(ext, default_dir, DialogStyle.save)


_folder_dialog_style = {DialogStyle.open: mdd.DD_DIR_MUST_EXIST,
                        DialogStyle.save: mdd.DD_NEW_DIR_BUTTON,
                        DialogStyle.multiple: mdd.DD_DIR_MUST_EXIST | mdd.DD_MULTIPLE}


def _folder_dialog_filter(folder: str) -> str:
    return expanduser('~' + folder[14:]) if folder.startswith('Home directory') else folder


def folder_to_open(default_dir: str = getcwd(), style: DialogStyle = DialogStyle.open) -> Union[str, Iterable[str]]:
    _ = wx.App()
    open_folder_dialog = wx.lib.agw.multidirdialog.MultiDirDialog(
        None, "Select Folder", defaultPath=default_dir, agwStyle=_folder_dialog_style[style])
    selection = _select_item(open_folder_dialog, style)
    if isinstance(selection, str):
        return _folder_dialog_filter(selection)
    elif isinstance(selection, Iterable):
        return (_folder_dialog_filter(x) for x in selection)


def folders_to_open(default_dir: str = getcwd()) -> Iterable[str]:
    return folder_to_open(default_dir, style=DialogStyle.multiple)


def folder_to_save(default_dir: str = getcwd()) -> str:
    return folder_to_open(default_dir, style=DialogStyle.save)
