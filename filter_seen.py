"""Checks if the jobs are seen in the database and filters them out."""

import pandas as pd

from csv_utils import read_from_csv, save_to_csv
from pipeline_config import JOBS_NEW_CSV, JOBS_SEEN_CSV


def filter_seen_jobs(
    seen_jobs: pd.DataFrame, candidate_jobs: pd.DataFrame
) -> pd.DataFrame:
    """Filters out jobs that are already seen in the database."""
    seen_jobs = seen_jobs.set_index("job_url")
    candidate_jobs = candidate_jobs.set_index("job_url")
    return candidate_jobs[~candidate_jobs.index.isin(seen_jobs.index)]
