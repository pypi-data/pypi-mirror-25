import random
import requests
import os.path

def rr():
    _uaFile()
    return random.choice(open('ua.txt').readlines()).strip()

def _uaFile():
    if os.path.isfile("ua.txt"):
        print("1111")
    else:    
        url = "https://raw.githubusercontent.com/wayne4v/useragent/master/useragent.txt"
        response = requests.get(url)
        with open('ua.txt', 'wb') as out:
            out.write(response.content)
        out.close()