import os
import base64
from pathlib import Path
import requests

# Passing in a real face Image
with open(str(Path(__file__).resolve().parent) + '/images/1.png', 'rb') as img_file:
    my_string = base64.b64encode(img_file.read())

r = requests.post("http://0.0.0.0:5000/v2/facereality",
                  data={'image': my_string})

assert r.status_code == 200

# Passing in a fake Image
with open(str(Path(__file__).resolve().parent) + '/images/57.png', 'rb') as img_file:
    my_string = base64.b64encode(img_file.read())

r = requests.post("http://0.0.0.0:5000/v2/facereality",
                  data={'image': my_string})

assert r.status_code == 403
