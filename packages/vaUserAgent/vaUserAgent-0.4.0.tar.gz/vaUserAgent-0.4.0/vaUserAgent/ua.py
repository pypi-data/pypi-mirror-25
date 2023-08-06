import random
import requests
import os.path

def rr():
    _uaFile()
    return random.choice(open('/tmp/ua.txt').readlines()).strip()

def _uaFile():
    if os.path.isfile("/tmp/ua.txt"):
        pass
    else:    
        url = "https://raw.githubusercontent.com/wayne4v/useragent/master/useragent.txt"
        response = requests.get(url)
        with open('/tmp/ua.txt', 'wb') as out:
            out.write(response.content)
        out.close()