import os
import base64
from pathlib import Path
import requests

# Passing in a real face Image
with open(str(Path(__file__).resolve().parent) + '/Images/1.png', 'rb') as img_file:
    my_string = base64.b64encode(img_file.read())

r = requests.post("http://0.0.0.0:5000/facereality", data={'image': my_string})

print(r.status_code)

# Passing in a fake Image
with open(str(Path(__file__).resolve().parent) + '/Images/57.png', 'rb') as img_file:
    my_string = base64.b64encode(img_file.read())

r = requests.post("http://0.0.0.0:5000/facereality", data={'image': my_string})

print(r.status_code)
