import os
import json


class JSONGrabber:
    def __init__(self, filename=None):
        if not filename:
            filename = 'results.json'

        self._file = open(filename, 'w', encoding='utf-8')
        self._file.write('[\n]\n')
        self._first_write = True

    def write(self, item: dict):
        self._file.seek(self._file.tell() - 2, os.SEEK_SET)

        if self._first_write:
            self._first_write = False
        else:
            self._file.write(',\n')

        json.dump(item, self._file, sort_keys=True, indent=4)
        self._file.write('\n]')

    def destruct(self):
        self._file.close()
