import pandas as pd
import csv


def parse_csv(file_name):
    data = []
    with open(file_name, 'rt') as sd:
        r = csv.DictReader(sd)
        for line in r:
            data.append(line)
    return data


def get_df_from_csv(file_name):
    data = parse_csv(file_name)
    df = pd.DataFrame(data)
    return df
