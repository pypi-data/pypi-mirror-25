import random
import requests
import os.path

def rr():
    return random.choice(open('ua.txt').readlines()).strip()
