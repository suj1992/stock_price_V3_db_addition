import os
from flask import send_from_directory

DOWNLOAD_CSV = 'output'

def download_csv(filename):
    file_path = os.path.join(DOWNLOAD_CSV, filename)
    if os.path.exists(file_path):
        return send_from_directory(DOWNLOAD_CSV, filename, as_attachment=True)
    else:
        return 'File not found', 404