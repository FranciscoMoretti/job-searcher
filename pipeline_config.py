# Define the keywords to search for
from typing import List


KEYWORDS_REQUIREMENTS: List[List[str]] = [
    ["react", "next.js", "nextjs", "reactjs", "React.js"],  # Frontend Framework
    ["js", "JavaScript", "TypeScript", "ts"],  # Language
    ["python", "python3", "py", "node", "nodejs", "node.js"],  # Backend
    ["AI", "A.I.", "artificial intelligence", "llm", "machine learning", "ML"],  # AI
]

DATA_PATH = "data/"

JOBS_SEEN_CSV = DATA_PATH + "jobs_seen.csv"
# TODO: Not sure if new should be in memory / queue or in a CSV db
JOBS_NEW_CSV = DATA_PATH + "jobs_new.csv"
JOBS_KEYWORD_MATCHED_CSV = DATA_PATH + "jobs_keyword_matched.csv"
