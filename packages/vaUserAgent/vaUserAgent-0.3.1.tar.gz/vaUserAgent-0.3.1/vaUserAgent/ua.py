import random

def rr():
    return random.choice(open('vaUserAgent/ua.txt').readlines()).strip()

def out():
    print(random.choice(open('vaUserAgent/ua.txt').readlines()).strip()