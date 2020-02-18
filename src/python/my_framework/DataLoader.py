import pandas as pd


class DataLoader:

    def __init__(self, path):
        self.raw_data = pd.read_csv(path, parse_dates=['date'])
        print(self.raw_data.head(10))
