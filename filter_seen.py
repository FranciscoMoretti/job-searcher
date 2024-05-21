"""Checks if the jobs are seen in the database and filters them out."""

import pandas as pd

from csv_utils import read_from_csv, save_to_csv
from pipeline_config import JOBS_NEW_CSV, JOBS_SEEN_CSV


def filter_seen(seen_jobs: pd.DataFrame, candidate_jobs: pd.DataFrame) -> pd.DataFrame:
    """Filters out jobs that are already seen in the database."""
    seen_jobs = seen_jobs.set_index("job_url")
    candidate_jobs = candidate_jobs.set_index("job_url")
    return candidate_jobs[~candidate_jobs.index.isin(seen_jobs.index)]


if __name__ == "__main__":
    # Read the CSV file
    seen_jobs = read_from_csv(JOBS_SEEN_CSV)
    candidate_jobs = read_from_csv("data/jobs_1.csv")
    filtered_jobs = filter_seen(seen_jobs, candidate_jobs)
    # Print the filtered dataframe
    print(filtered_jobs)
    # Save the filtered dataframe to a new CSV file
    save_to_csv(filtered_jobs, JOBS_NEW_CSV)
