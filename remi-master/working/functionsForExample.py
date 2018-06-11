from random import randint, getrandbits
import time, threading
from datetime import datetime


def myrandomfunction():
    while True:
        return randint(1,9)

def returntime():
    return datetime.now().strftime('%Y-%m-%d \n %H:%M')

def init_test():
    time.sleep(3)
    return bool(getrandbits(1))

