import os
import uuid


def generate_filename():
    filename = str(uuid.uuid4().hex)
    return filename


def generate_folder_name():
    return generate_filename() + '/'


def read_files(files):
    paths = []
    for file in files:
        filename = os.path.join('data\\images', generate_filename()+".jpg")
        with open(filename, 'wb') as f:
            f.write(file.getvalue())
            paths.append(filename)
    return paths
