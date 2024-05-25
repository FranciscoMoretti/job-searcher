"""Main pipeline definition for the job-search project."""

import os
import pathlib
from typing import List, Optional

import pandas as pd

from csv_utils import read_from_csv, save_to_csv
from filter_by_keywords import filter_by_keywords
from merge_jobs import extend_non_repeated
from metadata_utils import read_metadata, save_metadata
from pipeline_config import (
    KEYWORDS_REQUIREMENTS,
    JOBS_KEYWORD_MATCHED_CSV,
    JOBS_NEW_CSV,
    JOBS_SEEN_CSV,
    JOBS_SOURCE_FILENAME_BASE,
    JOBS_SOURCE_FILENAME_EXT,
    JOBS_RAW_CSV,
)
from merge_jobs import get_source_files_nums
from source_file_utils import (
    num_to_source_file_path,
)


def pipeline():
    """Main pipeline function."""
    sources_to_raw()
    raw_to_filtered_keywords()


def sources_to_raw() -> List[pd.DataFrame]:
    """Read the CSV files that have `jobs_{num}.csv` as name and combine them into jobs_raw"""
    jobs = get_jobs_raw()

    metadata = read_metadata()
    new_file_nums = get_unparsed_source_files_numbers(metadata)

    if not new_file_nums:
        print("No new files to parse")
        return

    for file_num in new_file_nums:
        file_path = num_to_source_file_path(file_num)
        # Read the CSV file and append it to the jobs dataframe
        jobs_from_source = read_from_csv(file_path)
        if len(jobs) == 0:
            jobs = jobs_from_source
        else:
            jobs = extend_non_repeated(jobs, jobs_from_source)
        print(f"Parsed {file_path}")
        print(f"Processed {len(jobs_from_source)} jobs")

    # Save the dataframe to a CSV file
    save_to_csv(jobs, JOBS_RAW_CSV)
    # Update the last parsed source in the metadata
    print(f"Saved {len(jobs)} jobs to {JOBS_RAW_CSV}")

    metadata["last_parsed_source_idx"] = max(new_file_nums)
    save_metadata(metadata)


def get_unparsed_source_files_numbers(metadata):
    last_parsed_source_idx = metadata["last_parsed_source_idx"]
    file_nums = get_source_files_nums()
    new_file_nums = [
        file_num for file_num in file_nums if file_num > last_parsed_source_idx
    ]

    return new_file_nums


def raw_to_filtered_keywords() -> pd.DataFrame:
    """Read the jobs_raw.csv file and filter the keywords"""
    df = filter_by_keywords(read_from_csv(JOBS_RAW_CSV), KEYWORDS_REQUIREMENTS)
    # Print the filtered dataframe
    print(f"Filter (keywords) passed by {len(df)} jobs")
    # Save the filtered dataframe to a new CSV file
    save_to_csv(df, JOBS_KEYWORD_MATCHED_CSV)


def get_jobs_raw():
    if pathlib.Path(JOBS_RAW_CSV).exists():
        jobs = read_from_csv(JOBS_RAW_CSV)
    else:
        jobs = pd.DataFrame()
    return jobs


def __main__():
    pipeline()


if __name__ == "__main__":
    __main__()
