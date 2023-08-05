"""
Bit Doodle!

Description:
    Bit Doodle is a class designed for working with variable length bit fields.  While the class can technically be
    used for anything, it is catered towards IPv4 and IPv6 addresses.  The main methods are join and disjoin, which
    will take a list of variable length fields and a list of values and join them together to a single value, or
    disjoin which will take a single value and a list of bit lengths, and break the original value into its multiple
    parts.
"""

import ipaddress


class BitDoodle(object):
    def __init__(self, _format):
        """initialize the format

        Args:
            _format (list): List of integers, each one representing a bit length
        """
        self._format = _format
        self.total_bit_length = sum(self._format)

    def join(self, values):
        """Given a list of bit lengths, and a list of values, join the values into a single number.  If the bit lengths
        are exactly 32 or 128 bits, an IpAddress object is returned instead.

        Args:
            values (list): list of integers.

        Returns:
            IpAddress:  if bitlength is 32 or 128
            int:  if bitlength is not 32 or 128
        """
        # validate lists
        self.validate_list_lengths(values)
        real_values = []
    
        for index, bit_length in enumerate(self._format):
            # validate values
            self.validate_value(values[index], bit_length)
    
            shift_distance = self.get_bit_shift_distance(self._format, index)
            real_value = values[index] << shift_distance
            real_values.append(real_value)
    
        if self.total_bit_length == 32 or self.total_bit_length == 128:
            return ipaddress.ip_address(sum(real_values))
        else:
            return sum(real_values)

    def disjoin(self, value):
        """Given a single value and a list of bit lengths, disjoin the value into its bit length values.

        Args:
            value (int): number that you want broken into its pieces designed in self._format

        Returns:
            list: list of integers

        """
        piece_values = []
        for index, bit_length in enumerate(self._format):
            mask = (self.get_max_value(bit_length) << self.get_bit_shift_distance(self._format, index)) #creates a mask of all 1's for only the relevant bits
            real_value = value & mask
            piece_value = real_value >> self.get_bit_shift_distance(self._format, index)
            piece_values.append(piece_value)
        return piece_values

    def validate_value(self, value, bit_length):
        if 0 <= value <= self.get_max_value(bit_length):
            return True
        raise Exception("{} out of range (0 -> {})".format(value, self.get_max_value(bit_length)))

    def validate_list_lengths(self, values):
        if len(self._format) != len(values):
            raise Exception("Format List Length ({}) is not equal to Values List Length ({})".format(
                len(self._format), len(values))
            )
        if len(self._format) == 0:
            raise Exception("List length can not be 0")
        return True

    @staticmethod
    def get_bit_shift_distance(_format, index):
        shift_distance = sum(_format[index+1::])
        return shift_distance

    @staticmethod
    def get_max_value(bit_length):
        return (1 << bit_length) - 1
