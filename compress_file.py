import subprocess


def compress_file(file_name, new_archive):
    subprocess.run(["7z", "a", f"{new_archive}", f"{file_name}"])
    subprocess.run(["rm", f"{file_name}"])
