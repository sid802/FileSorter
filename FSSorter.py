__author__ = 'Sid'

import os

class Sorter(object):
    def __init__(self, base_directory, recursive=False):
        """
        :param directory: string - Directory to sort
        :param sub_dirs: boolean - sort also sub directories
        """
        abs_path = os.path.abspath(base_directory)
        if not os.path.isdir(abs_path):
            raise IOError("Directory does not exist! `{0}`".format(abs_path))
        self.base_directory = os.path.abspath(base_directory)
        self.recursive = recursive

