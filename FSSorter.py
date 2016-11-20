__author__ = 'Sid'

import os

class Sorter(object):
    def __init__(self, base_directory, target_directory='.', recursive=False):
        """
        :param directory: string - Directory to sort
        :param destination_directory: Base directory where we want the new folders to be created
        :param recursive: boolean - sort also sub directories
        """
        abs_base_path = os.path.abspath(base_directory)
        if not os.path.isdir(abs_base_path):
            raise IOError("Directory does not exist! `{0}`".format(abs_base_path))

        abs_target_path = os.path.abspath(target_directory)
        if not os.path.isdir(abs_target_path):
            raise IOError("Directory does not exist! `{0}`".format(abs_target_path))

        self.base_directory = abs_base_path
        self.target_directory = abs_target_path
        self.recursive = recursive

