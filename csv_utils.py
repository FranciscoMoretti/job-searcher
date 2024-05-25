import pandas as pd


# TODO: perform validation here with the schema
def read_from_csv(file_name):
    # Open the CSV file
    with open(file_name, "r") as file:
        # Read from csv with a pd dataframe
        df = pd.read_csv(file)
        return df


def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
