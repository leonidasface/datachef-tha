import datetime
import pandas

def read_csv(file: str):
    return pandas.read_csv(file)

def csv_by_minute():
    minute = datetime.datetime.now().minute
    if (minute < 15):
        return 1
    elif(15 <= minute < 30):
        return 2
    elif(30 <= minute < 45):
        return 3
    else:
        return 4