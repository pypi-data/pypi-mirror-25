import random

def rr():
    return random.choice(open('ua/vaUserAgent/ua.txt').readlines()).strip()

def out():
    print(random.choice(open('ua/vaUserAgent/ua.txt').readlines()).strip())