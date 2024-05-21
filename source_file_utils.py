import pathlib
import re
from typing import Optional

from pipeline_config import (
    DATA_PATH,
    JOBS_SOURCE_FILENAME_BASE,
    JOBS_SOURCE_FILENAME_EXT,
)


def num_to_source_file_path(num: int) -> pathlib.Path:
    """Convert a number to a pathlib.Path object representing a file with the given number."""
    return pathlib.Path(
        DATA_PATH, f"{JOBS_SOURCE_FILENAME_BASE}{num}.{JOBS_SOURCE_FILENAME_EXT}"
    )


def source_file_path_to_num(file: pathlib.Path) -> Optional[int]:
    """Convert a pathlib.Path object representing a file with the given number to an integer."""
    # TODO Extract `jobs_` into a reusable pipeline variable
    file_search = re.search(r"jobs_(\d+).csv", file.name)
    if file_search is None:
        return None
    return int(file_search.group(1))
