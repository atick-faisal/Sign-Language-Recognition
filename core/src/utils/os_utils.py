import os


def get_file_count(path: str) -> int:
    file_count = 0

    for _, _, files in os.walk(path):
        file_count += len(files)

    return file_count
