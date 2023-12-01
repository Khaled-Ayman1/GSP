import pandas as pd
import numpy as np


def preprocessing(df):

    # remove whitespaces from string columns
    for col in df.columns:
        col = col.strip()
        if df[col].dtype == 'object':  # check if the column contains strings
            df[col] = df[col].str.strip()

    # drop null
    df.dropna(how='any', inplace=True)

    df.drop_duplicates(inplace=True)

    df.reset_index(drop=True, inplace=True)

    # Add checking for vertical or horizontal data + transformation


test_df = pd.read_excel('data/test_data.xlsx')

preprocessing(test_df)
