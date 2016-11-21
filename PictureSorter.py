__author__ = 'Sid'

import re, os
from FSSorter import Sorter
from datetime import datetime
from glob import glob
from TimestampTrunc import TimestampTrunc
from itertools import groupby

class PictureInfo(object):
    """
    Hold relevant info for picture
    to do the sorting as needed
    """

    def __init__(self, path, timestamp):
        self.path = path  # String
        self.timestamp = timestamp  # datetime

    def __repr__(self):
        return unicode(self.path)


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

        picture_paths = [path for path in glob(os.path.join(self.base_directory, '*')) if os.path.isfile(path)]

        picture_infos = list()
        for picture_path in picture_paths:
            timestamp = self.get_timestamp_from_picture(picture_path)
            if timestamp is not None:
                picture_infos.append(PictureInfo(picture_path, timestamp))

        result_dict = self._redistribute(picture_infos)
        return result_dict


    def _redistribute(self, picture_infos):
        """
        :param picture_infos: List of PictureInfos'
        :return: Dictionary - files who were successfully moved and failed
                 Keys are: success / failure
        This method redistributes the pictures based on their timestamp
        """

        return_dict = {}
        return_dict['success'] = list()
        return_dict['failure'] = list()

        truncer = TimestampTrunc(self.group_by)

        for k, g in groupby(picture_infos, lambda picture_info: truncer.trunc(picture_info.timestamp)):
            dir_name = truncer.to_trimmed_string(k)
            picture_infos_to_transfer = list(g)
            current_results = self._move_files(dir_name, picture_infos_to_transfer)
            return_dict['success'] += current_results['success']
            return_dict['failure'] += current_results['success']

        return return_dict

    def _move_files(self, folder_name, picture_infos):
        """
        :param folder_name: string - Folder to create in target directory
        :param picture_infos: List of PictureInfo's to move
        :return: Dictionary - files who were successfully moved and failed
                 Keys are: success / failure
        """

        return_dict = {}
        return_dict['success'] = list()
        return_dict['failure'] = list()

        target_dir = os.path.join(self.base_directory, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for picture_info in picture_infos:
            dirname, filename = os.path.split(picture_info.path)
            try:
                os.rename(picture_info.path, os.path.join(target_dir, filename))
                #print "Moving {0} to {1}".format(picture_info.path, os.path.join(target_dir, filename))
                return_dict['success'].append((picture_info.path, target_dir))
            except Exception as e:
                return_dict['failure'].append((picture_info.path, target_dir, e.message))

        return return_dict

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

if __name__ == '__main__':
    pic_sorter = PictureSorter(r'C:\Users\Sid\Documents\Android\Photos', group_by='month')
    results = pic_sorter.sort()

    print "Failed to move:"
    for failure in results['failure']:
        print "`{0}` to dir `{1}`. Error: {2}".format(failure[0], failure[1], failure[2])