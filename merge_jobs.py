from typing import Optional
import pandas as pd
import pathlib
import re

from csv_utils import read_from_csv, save_to_csv
from metadata_utils import read_metadata, save_metadata
from pipeline_config import JOBS_NEW_CSV, JOBS_SEEN_CSV, JOBS_SOURCES_CSV
from source_file_utils import num_to_source_file_path, source_file_path_to_num


def extend(jobs_1: pd.DataFrame, jobs_2: pd.DataFrame) -> pd.DataFrame:
    """Extend the first dataframe with the second dataframe."""
    return pd.concat([jobs_1, jobs_2], ignore_index=True)


def get_source_files_nums():
    # Find jobs_{num}.csv files in the data/ directory with pathlib
    glob_pattern = "jobs_*.csv"
    source_indexes = []
    for file in pathlib.Path("data").glob(glob_pattern):
        file_num = source_file_path_to_num(file)
        if file_num is not None:
            source_indexes.append(file_num)
    return sorted(source_indexes)


if __name__ == "__main__":
    # Read the CSV files that have `jobs_{num}.csv` as name and combine them into one dataframe
    if pathlib.Path(JOBS_SOURCES_CSV).exists():
        jobs = read_from_csv(JOBS_SOURCES_CSV)
    else:
        jobs = pd.DataFrame()

    metadata = read_metadata()
    last_parsed_source = metadata["last_parsed_source"]
    file_nums = get_source_files_nums()
    for file_num in file_nums:
        file_path = num_to_source_file_path(file_num)
        if file_num > last_parsed_source:
            # Read the CSV file and append it to the jobs dataframe
            jobs_from_source = read_from_csv(file_path)
            jobs = extend(jobs, jobs_from_source)
            last_parsed_source = file_num
            print(f"Parsed {file_path}")
            print(f"Added {len(jobs_from_source)} jobs")

    # Save the dataframe to a CSV file
    save_to_csv(jobs, JOBS_SOURCES_CSV)
    # Update the last parsed source in the metadata
    metadata["last_parsed_source"] = last_parsed_source
    save_metadata(metadata)
