__author__ = 'Sid'

import re, os
from FSSorter import Sorter
from datetime import datetime
from glob import glob

class PictureInfo(object):
    """
    Hold relevant info for picture
    to do the sorting as needed
    """

    def __init__(self, path, timestamp):
        self.path = path  # String
        self.timestamp = timestamp  # datetime


class PictureSorter(Sorter):
    """
    Class to sort your pictures into folders
    """

    # Pattern matching file names with full timestamp in format yyyy.dd.mm.hh.mm.dd (Dot can be replaced by any char)
    full_timestamp = re.compile(r'(^|\D)(?P<year>\d{4})\D?(?P<month>\d{2})\D?(?P<day>\d{2})\D?(?P<hour>\d{2})\D?(?P<minute>\d{2})\D?(?P<second>\d{2})(\D|$)')
    date_stamp = re.compile(r'(^|\D)(?P<year>\d{4})\D?(?P<month>\d{2})\D?(?P<day>\d{2})(\D|$)')

    def __init__(self, base_directory, destination_directory='.', sub_dirs=False, group_by='day'):
        """
        :param base_directory: string - Directory to sort
        :param sub_dirs: boolean - sort also sub directories
        :param group_by: string - second/minute/hour/day/month/year to sort pictures in folders
        """
        super(PictureSorter, self).__init__(base_directory, destination_directory, sub_dirs)
        self.group_by = group_by

    def sort(self):
        """
        :return: Dictionary - files who were successfully moved and failed
                 Keys are: success / failure
        """

        picture_paths = glob(os.path.join(self.base_directory, '*'))
        picture_infos = list()
        for picture_path in picture_paths:
            timestamp = self.get_timestamp_from_picture(picture_path)
            picture_infos.append(PictureInfo(picture_path, timestamp))

        result_dict = self._redistribute(picture_infos)
        return result_dict


    def _redistribute(self, picture_infos, destination_directory):
        """
        :param picture_infos: List of PictureInfos'
        :param destination_directory: Base directory where we want the new folders to be created
        :return: Dictionary - files who were successfully moved and failed
                 Keys are: success / failure
        This method redistributes the pictures based on their timestamp
        """




    @classmethod
    def get_timestamp_from_picture(cls, picture_path):
        """
        :param picture_path: Path to picture
        :return: Timestamp associated with path
        """
        timestamp = cls.get_timestamp_from_picture_path(picture_path)

        #TODO: Add timestamp from meta if previous is empty

        return timestamp

    @classmethod
    def get_timestamp_from_picture_path(cls, picture_path):
        """
        :param picture_path: String - Path to picture
        :return: datetime - extracted from picture if possible
        """
        match = cls.full_timestamp.search(picture_path)
        if not match:
            # Try partial match (just date)
            match = cls.date_stamp.search(picture_path)
            if not match:
                return None

        # Turn timestamp values to integers
        match_dict = match.groupdict()
        for k, v in match_dict.iteritems():
            match_dict[k] = int(v)

        return datetime(**match_dict)
