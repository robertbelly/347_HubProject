from random import randint, getrandbits
import time, threading
from datetime import datetime


def myrandomfunction():
        return randint(69,73)


def returntime():
    return datetime.now().strftime('%Y-%m-%d \n %H:%M')

def init_test():
    time.sleep(1)
    return bool(getrandbits(1))

