from datetime import datetime, date
import common.master_data as master_data

import pandas as pd

f_name = __file__.split('/')[-1]

def since_listing(arg_year: int | str | None):
    """Returns the % gain of stocks since listing
    Parameter
    ---------
    arg_year: str | int | None
        Year of listing for example, 2023
    Return pandas.DataFrame
        Data Frame
    """
    m_name = "since_listing"
    log_append = f"File: {f_name} Module: {m_name}" 
    # If the listing year is None then default the listing year to current year
    if arg_year is None:
        arg_year = str(datetime.today().year)
    print(f"{log_append}: Listing year: [{arg_year}]")
    # Gather all symbols that got listed in the specified year
    all_symbols = master_data.get_equity_master()
    print(f"{log_append}: All symbols count: [{len(all_symbols)}]")
    # copy is created to avoid the warning, and rightly so.
    # SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
    only_equities = all_symbols[all_symbols['SERIES'] == 'EQ'].copy()
    print(f"{log_append}: Equities count: [{len(only_equities)}]")
    # Filter out equities for the concerned year
    only_equities['ARG_YEAR'] = arg_year    
    # only_equities['LISTING_YEAR'] = 
    print(f"{log_append}: only_equities count: {len(only_equities)}")
    # For each equity, calculate the gain/loss since listing date
    # Return Empty data frame in case of error!
    return only_equities

