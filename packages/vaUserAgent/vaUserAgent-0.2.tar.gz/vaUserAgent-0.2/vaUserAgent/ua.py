import random

def rr():
    return random.choice(open('vaUserAgent/ua.txt').readlines()).strip().decode('utf-8')

def out():
    print(random.choice(open('vaUserAgent/ua.txt').readlines()).strip().decode('utf-8'))

print(rr())
out()