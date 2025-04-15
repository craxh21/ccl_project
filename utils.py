import hashlib

def calculate_md5(file_data):
    return hashlib.md5(file_data).hexdigest()
