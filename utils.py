import os
import string
import random


def generate_folder_name():
    return ''.join(random.choice(string.ascii_letters) for _ in range(8)) + '/'


def read_files(files):
    paths = []
    for file in files:
        filename = os.path.join('data/images', file.name)
        with open(filename, 'wb') as f:
            f.write(file.getvalue())
            paths.append(filename)
    return paths
