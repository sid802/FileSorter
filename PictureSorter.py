__author__ = 'Sid'

import re
from FSSorter import Sorter

class PictureSorter(Sorter):
    """
    Class to sort your pictures into folders
    """

    # Pattern matching file names with full timestamp in format yyyy.dd.mm.hh.mm.dd (Dot can be replaced by any char)
    full_timestamp = re.compile(r'\D(?P<year>\d{4})\D?(?P<month>\d{2})\D?(?P<day>\d{2})\D?(?P<hour>\d{2})\D?(?P<minute>\d{2})\D?(?P<second>\d{2})\D')
    date_stamp = re.compile(r'\D(?P<year>\d{4})\D?(?P<month>\d{2})\D?(?P<day>\d{2})\D')

    def __init__(self, base_directory, sub_dirs=False, group_by='day'):
        """
        :param base_directory: string - Directory to sort
        :param sub_dirs: boolean - sort also sub directories
        :param group_by: string - second/minute/hour/day/month/year to sort pictures in folders
        """
        super(PictureSorter, self).__init__(base_directory, sub_dirs)
        self.group_by = group_by

