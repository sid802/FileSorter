__author__ = 'Sid'

class TimestampTrunc(object):

    _possible_values = ['year', 'month', 'day', 'hour', 'minute', 'second']

    def __init__(self, trunc_to):
        if trunc_to.lower() not in self._possible_values:
            raise ValueError("trunc_to must be in: {0}".format(self._possible_values))
        self.trunc_to = trunc_to.lower()

    def trunc(self, datetime):
        max_index = self._possible_values.index(self.trunc_to) + 1
        datetime_values = []
        for i in xrange(max_index):
            value = self.to_string(getattr(datetime, self._possible_values[i]))
            datetime_values.append(value)

        date = '-'.join(datetime_values[:3])
        if len(datetime_values) > 3:
            time = ':'.join(datetime_values[3:])
            return "{0} {1}".format(date, time)
        return date

    @staticmethod
    def to_string(n):
        """
        :param n: int
        :return: left-padded with zeroes (minimum length of 2)
        """
        n_string = str(n)
        if len(n_string) < 2:
            return '0' + n_string
        return n_string

