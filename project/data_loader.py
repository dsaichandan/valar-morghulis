class DataLoad(object):


    def readCsv(self, filename, delimiter=',', header=True):

        f = open(filename, 'r')

        data = []
        header_data = []
        line_count = 0
        for line in f.readlines():
            row = line.split(delimiter)

            if (header and 0 == line_count):
                header_data = row
            else:
                data.append(row)

            line_count += 1

        if (header):
            return header_data, data
        else:
            return data

    def convert_new_line_format(self, filename, old, new):
        data = open(filename, 'rb').read()

        new_data = data.replace(old, new)

        if new_data != data:
            f = open(filename, 'wb')
            f.write(new_data)
            f.close()
