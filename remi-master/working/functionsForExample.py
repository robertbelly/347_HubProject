from random import randint, getrandbits
import time, threading
from datetime import datetime


def myrandomfunction(decision):
    if decision == 1:
        while True:
            return randint(1,9)
    else: return "Nothing"


def returntime():
    return datetime.now().strftime('%Y-%m-%d \n %H:%M')

def init_test():
    time.sleep(1)
    return bool(getrandbits(1))

