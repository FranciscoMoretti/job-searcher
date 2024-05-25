# Define the keywords to search for
from typing import List


KEYWORDS_REQUIREMENTS: List[List[str]] = [
    ["react", "next.js", "nextjs", "reactjs", "React.js"],  # Frontend Framework
    ["js", "JavaScript", "TypeScript", "ts"],  # Language
    ["python", "python3", "py", "node", "nodejs", "node.js"],  # Backend
    ["AI", "A.I.", "artificial intelligence", "llm", "machine learning", "ML"],  # AI
]

DATA_PATH = "data/"

METADATA_JSON = DATA_PATH + "metadata.json"

JOBS_SOURCE_FILENAME_BASE = "jobs_"
JOBS_SOURCE_FILENAME_EXT = "csv"
JOBS_RAW_CSV = DATA_PATH + "jobs_raw.csv"
JOBS_KEYWORD_MATCHED_CSV = DATA_PATH + "jobs_keyword_matched.csv"
WEB_BROWSER = "wslview %s"
