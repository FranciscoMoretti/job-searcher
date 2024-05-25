import pandas as pd
import pathlib

from filter_seen import filter_seen_jobs
from source_file_utils import source_file_path_to_num


def extend_non_repeated(
    seen_jobs: pd.DataFrame, candidate_jobs: pd.DataFrame
) -> pd.DataFrame:
    """Extend the first dataframe with the second dataframe without repeating jobs."""
    jobs_new = filter_seen_jobs(seen_jobs=seen_jobs, candidate_jobs=candidate_jobs)
    return pd.concat([seen_jobs, jobs_new], ignore_index=True)


def get_source_files_nums() -> list[int]:
    # Find jobs_{num}.csv files in the data/ directory with pathlib
    glob_pattern = "jobs_*.csv"
    source_indexes = []
    for file in pathlib.Path("data").glob(glob_pattern):
        file_num = source_file_path_to_num(file)
        if file_num is not None:
            source_indexes.append(file_num)
    return sorted(source_indexes)
