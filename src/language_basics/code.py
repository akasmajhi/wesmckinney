import pandas as pd
from ..common import constants

def read_bhav():
    daily_bhav_raw = pd.read_csv("/home/akasmajhi/cm06JUL2023bhav.csv")
    print(daily_bhav_raw)
    print(constants.BASE_URL)

