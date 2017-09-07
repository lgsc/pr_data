import pandas as pd
import csv


def parse_csv(file_path):
	data = []
	n = 0
	with open(file_path, 'rt') as sd:
		r = csv.DictReader(sd)
		for line in r:
			data.append(line)
	return data

def get_df_from_csv(file_path):
    data = parse_csv(file_path)
    df = pd.DataFrame(data)
    return df
