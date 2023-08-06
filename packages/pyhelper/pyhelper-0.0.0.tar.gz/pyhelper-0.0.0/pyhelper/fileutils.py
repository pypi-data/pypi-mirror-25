# coding=utf-8

import os
import platform
import tempfile


def get_temp_path(subdir=None):
    """
    返回临时文件路径
    :return:
    """
    tempdir = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()
    return tempdir if subdir is None else tempdir + os.sep + subdir


def get_temp_filename(subdir, filename):
    """
    返回临时文件名称
    :return:
    """
    tempdir = get_temp_path()
    if subdir is None or len(subdir) == 0:
        return tempdir + os.sep + filename
    else:
        return tempdir + os.sep + subdir + os.sep + filename


def textfile_to_int_set(filename):
    """
    读取文本文件，每行一个数据，返回集合
    :param filename:
    :return:
    """
    # 读取并构造集合
    data = set()
    with open(filename, 'r') as f:
        for line in f.readlines():
            n = len(line)
            if n > 0 and line[n - 1] == '\n':
                line = line[:n - 1]
                n -= 1
            if n == 8:
                data.add(int(line))
    return data
