import random
import string


def generate_folder_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(7)) + '/'

