import numpy as np
import pandas as pd 
from datetime import date
import common.constants 
def greet():
    print("Starting the preliminaries")

def read_bhavcopy(trading_date: date):
    if(trading_date):
        print(f"Received the trading date as {trading_date}")

if __name__ == "__main__":
    read_bhavcopy(date(2023, 11, 11))
    # greet()

