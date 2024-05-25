"""Main pipeline definition for the job-search project."""

import os
import pathlib
from typing import List, Optional

import pandas as pd

from csv_utils import read_from_csv, save_to_csv
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


def sources_to_raw() -> List[pd.DataFrame]:
    """Read the CSV files that have `jobs_{num}.csv` as name and combine them into jobs_raw"""
    jobs = get_jobs_raw()

    metadata = read_metadata()
    last_parsed_source_idx = metadata["last_parsed_source_idx"]
    file_nums = get_source_files_nums()
    new_file_nums = [
        file_num for file_num in file_nums if file_num > last_parsed_source_idx
    ]
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

    if new_file_nums:
        metadata["last_parsed_source_idx"] = max(new_file_nums)
    save_metadata(metadata)


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
