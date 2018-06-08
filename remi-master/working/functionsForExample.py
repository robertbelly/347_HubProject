from random import randint
import time, threading
from datetime import datetime


def myrandomfunction():
    while True:
        return randint(1,9)

def returntime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

