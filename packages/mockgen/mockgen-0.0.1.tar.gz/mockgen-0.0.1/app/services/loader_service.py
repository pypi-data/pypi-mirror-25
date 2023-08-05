import re
import json
import requests
from app.loaders import postman_loader

def load(loader, source):
    data = load_data(source)
    if loader == 'postman':
        return postman_loader.tranpose(data)

def load_data(source):
    matches = re.findall(r'^https?:\/\/', source)
    if len(matches) > 0:
        r = requests.request('GET', source)
        return r.json()
    else:
        with open(source, 'r') as f:
            return json.load(f)
