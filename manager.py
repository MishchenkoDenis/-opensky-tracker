import time
from datetime import datetime


def extract():
    print("Extract")


def tranform():
    print("Transform")


def load():
        print("Load")

tasks = [extract, tranform, load]


def pipelin():
    for i in tasks:
         i()


for i in range(3):
    print(f'Старт: {datetime.now()}')
    pipelin()
    time.sleep(3)

