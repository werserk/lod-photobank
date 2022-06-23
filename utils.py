import os
import string
import random


def generate_folder_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(7)) + '/'


def read_files(files):
    # creating folder for user
    folder_name = generate_folder_name()
    path = 'images/' + folder_name
    os.makedirs(path, exist_ok=True)

    paths = []
    for file in files:
        paths.append([])
        with open(path + file.name, 'wb') as f:
            f.write(file.getvalue())

            paths[-1].append(path + file.name)
    return paths, folder_name