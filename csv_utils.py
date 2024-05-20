import pandas as pd


def read_from_csv(file_name):
    # Open the CSV file
    with open(file_name, "r") as file:
        # Read from csv with a pd dataframe
        df = pd.read_csv(file)
        return df


def save_to_csv(filename, df):
    df.to_csv(filename, index=False)
