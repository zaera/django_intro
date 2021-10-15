import csv


class CSVGrabber:
    def __init__(self, filename=None, headers=None):

        if headers is None:
            headers = ()

        if not filename:
            filename = 'results.csv'

        self._file = open(filename, 'w')
        self.writer = csv.DictWriter(self._file, headers)

    def set_headers(self, headers):

        if not self.writer.fieldnames:
            self.writer.fieldnames = headers
            self.writer.writeheader()

    def write(self, item: dict):
        self.set_headers(sorted(list(item.keys())))

        # write the data
        self.writer.writerow(item)

    def destruct(self):
        self._file.close()
