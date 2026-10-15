import time
from datetime import datetime
from main import extract, transform, load


interval = 15

def pipline():
    print(datetime.now())
    data =  extract()
    df =  transform(data)
    load(df)
    print(datetime.now())

while True:
    pipline()
    time.sleep(interval)