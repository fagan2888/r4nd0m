import bitstring
import pandas
import numpy


class BinaryFrame:
    def __init__(self, data):
        """
        Initialization method for a Binary Frame object
        :param data: a pandas DataFrame to convert
        """
        assert isinstance(data, pandas.DataFrame)
        self.data = data
        self.bin_data = {}
        self.columns = self.data.columns

    def convert_basis_points_unbiased(self, convert=True):
        """

        :return:
        """
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if convert:
                    el = int(self.data[c][i] * 100)
                else:
                    el = self.data[c][i]
                cbin_data += self.to_binary_string(el)
            self.bin_data[c] = cbin_data

    def to_binary_string(self, x: int):
        if x < 0:
            bit_string = str(int(bin(x)[3:]))
            bit_string = bit_string.replace('1', '2').replace('0', '1').replace('2', '0')
            return bit_string
        elif x > 0:
            bit_string = str(int(bin(x)[2:]))
            return bit_string
        else:
            return "01"

    def convert_unbiased(self):
        """
        A method for converting a floating point binary pandas DataFrame into a Dictionary of binary strings
        1) Convert the floating points as per the IEEE 754 standard
        2) Check if the first bit is 1 or 0 (+ or -)
        3) If negative flip the bits in the string
        4) Special case - if the floating point number is 0, then return an unbiased string
        :return:
        """
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if self.data[c][i] != 0.0:
                    bin_r = bitstring.BitArray(float=self.data[c][i], length=32)
                    bit_string = str(bin_r._getbin())
                    if bit_string[0] == '1':
                        bit_string = bit_string[1::]
                        bit_string = bit_string.replace('1', '2').replace('0', '1').replace('2', '0')
                        bit_string = '1' + bit_string
                    cbin_data += bit_string
                else:
                    cbin_data += "0101010101010101010101010101010101010101010101010101010101010101"
            self.bin_data[c] = cbin_data

    def discretize(self):
        """
        A method for discretizing a pandas DataFrame into a Dictionary of Binary Strings
        1) If the return is +, then set the equivalent bit to 1
        2) If the return is -, then set the equivalent bit to 0
        Note that using this method compresses the data significantly
        :return:
        """
        for c in self.data.columns:
            cbin_data = ""
            for i in range(len(self.data[c])):
                if self.data[c][i] > 0.0:
                    cbin_data += '1'
                if self.data[c][i] < 0.0:
                    cbin_data += '0'
                else:
                    cbin_data += '01'
            self.bin_data[c] = cbin_data


def test_unbiased_conversion():
    f, sum_one, sum_zero = -1.0, 0, 0
    bit_count = numpy.zeros(63)
    for i in range(21):
        if f != 0.0:
            bin_r = bitstring.BitArray(float=f, length=64)
            bstring = str(bin_r._getbin())

            if bstring[0] == '1':
                bstring = bstring[1::]
                bstring = bstring.replace('1', '2').replace('0', '1').replace('2', '0')
                bstring = '1' + bstring

            z = bstring.count("0")
            o = bstring.count("1")
            sum_one += o
            sum_zero += z

            for j in range(63):
                bit_count[j] += int(bstring[j])

            print(f, "\t", bstring, z, o)
        f = round(f + 0.1, 1)

    print(sum_one, sum_zero, sum_zero-sum_one)
    print(bit_count)


def test_bp_convert():
    start = -1000
    ones, zeros = 0, 0
    for i in range(2001):
        if start < 0:
            bit_string = str(int(bin(start)[3:]))
            bit_string = bit_string.replace('1', '2').replace('0', '1').replace('2', '0')
        elif start > 0:
            bit_string = str(int(bin(start)[2:]))
        else:
            bit_string = "01"
        print(start, bit_string)
        for c in bit_string:
            if c == '1':
                ones += 1
            else:
                zeros += 1
        start += 1
    print(ones, zeros)


if __name__ == '__main__':
    # test_unbiased_conversion()
    test_bp_convert()
