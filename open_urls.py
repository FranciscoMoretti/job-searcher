"""Reads from a file that contains a jobs DF and open all the URLs in a browser."""

import webbrowser

from csv_utils import read_from_csv
from pipeline_config import JOBS_KEYWORD_MATCHED_CSV, WEB_BROWSER

df = read_from_csv(JOBS_KEYWORD_MATCHED_CSV)
for url in df["job_url"]:
    print(f"Opening {url}")
    webbrowser.get(WEB_BROWSER).open(url)
