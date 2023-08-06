import argparse
import os
import re
import sys
from shutil import copyfile
import unidecode


class CsvFileCleaner:
    """
    Constructor for the CsvFileCleaner object

    file_to_process: path to the file that you want to clean
    separator: character used as separator fro the CSV file
    """

    def __init__(self, file_to_process, separator):
        self.file_to_process = file_to_process
        self.separator = separator
        self.tmp_file = "/tmp/tmp_text_file.txt"
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)

    """
    Method to start cleaning the file
    MUST be called after calling the constructor
    """

    def process(self):
        if self is None:
            raise Exception("First you must instantiate an object of type CsvFileCleaner")
        file_to_process = open(self.file_to_process, 'r')
        for line in file_to_process.readlines():
            text_to_write = self.__clean(line)
            write_to_file(self.tmp_file, text_to_write)
        return copyfile(self.tmp_file, self.file_to_process)

    def __clean(self, text):
        result = ""
        for token in text.split(self.separator):
            token = unidecode.unidecode(token)
            token = token.lower().replace("\n", "")
            text = re.sub('[^0-9a-zA-Z]+', ' ', token)
            result += text + self.separator
        return result[:-1]


def write_to_file(file, text):
    file_to_write = open(file, "a")
    file_to_write.write(text + "\n")


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('file_to_process', type=str, help='Path of the CSV file that you want to clean')
    parser.add_argument('--separator', type=str, help='Separator of the CSV file', default=",")

    return parser.parse_args(argv)


def main(args):
    file_to_process = args.file_to_process
    separator = args.separator
    fc = CsvFileCleaner(file_to_process, separator)
    fc.process()


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
