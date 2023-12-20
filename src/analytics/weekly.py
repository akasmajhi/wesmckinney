import pandas as pd 

import common.helper as helper

# from common import helper
f_name = __file__.split('/')[-1]

def weekly_price_gainers(filter: dict):
    m_name = "weekly_price_gainers"
    log_append = f"File: {f_name} Module: {m_name}"
    result = {
        "gainers":  pd.DataFrame(),
        "losers": pd.DataFrame,
        "no_change": pd.DataFrame(),
    }
    print(f"{log_append} filter: [{filter}]")
    if filter["duration"] == 'WEEK':
        print(f"{log_append} Start of weekly price gainers")
        data = helper.prepare_weekly_data(filter["start_date"], 'EQ')
        result['gainers'] = data[data["pct_change"] > 0]
        result['losers'] = data[data["pct_change"] < 0]
        result['no_change'] = data[data["pct_change"] == 0]
        return result
    print(f"{log_append} Invalid duration {filter["duration"]}passed.")
    return None 

