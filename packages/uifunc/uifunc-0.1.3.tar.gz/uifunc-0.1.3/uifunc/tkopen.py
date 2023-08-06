"""convenience functions for choosing file with Tk"""
# noinspection SpellCheckingInspection
import tkinter.filedialog as tkfd
from os import path, getcwd
from tkinter import Tk
from typing import Union, List, Iterable


Filter = Union[str, List[str]]


def _choose_file(file_type: Filter, func) -> Union[str, List[str]]:
    root = Tk()
    if isinstance(file_type, str):
        default_ext, file_type_list = file_type, ((file_type, '*' + file_type),)
    elif isinstance(file_type, Iterable):
        default_ext, file_type_list = next(iter(file_type)), tuple((x, '*' + x) for x in file_type)
    else:
        raise ValueError('wrong file type :' + str(file_type))
    file_name = func(parent=root, defaultextension=default_ext, filetypes=file_type_list, initialdir=getcwd())
    root.destroy()
    return file_name


def file_to_open(file_type: Filter) -> str:
    return _choose_file(file_type, tkfd.askopenfilename)


def files_to_open(file_type: Filter) -> List[str]:
    return _choose_file(file_type, tkfd.askopenfilenames)


def file_to_save(file_type: Filter) -> str:
    return _choose_file(file_type, tkfd.asksaveasfilename)


def folder_to_open(default_dir: str=getcwd()) -> str:
    root = Tk()
    folder = tkfd.askdirectory(parent=root, initialdir=default_dir)
    root.destroy()
    return folder


folder_to_save = folder_to_open


def swap_ext(file_name: str, ext: str) -> str:
    return path.splitext(file_name)[0] + ext
