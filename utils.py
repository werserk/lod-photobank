import os
import string
import random


def generate_filename():
    filename = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    return filename


def generate_folder_name():
    return generate_filename() + '/'


def read_files(files):
    paths = []
    for file in files:
        filename = os.path.join('data/images', generate_filename())
        with open(filename, 'wb') as f:
            f.write(file.getvalue())
            paths.append(filename)
    return paths
