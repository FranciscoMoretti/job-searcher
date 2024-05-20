# A script that reads a CSV file and filters it by keywords in the description column

import re
from typing import List
import pandas as pd
from textblob import TextBlob

from csv_utils import read_from_csv, save_to_csv
from pipeline_config import (
    JOBS_KEYWORD_MATCHED_CSV,
    JOBS_NEW,
    JOBS_SCRAPPED_CSV,
    KEYWORDS_REQUIREMENTS,
)


def tokenize(text: str) -> List[str]:
    """Tokenize a text into a list of words."""
    blob = TextBlob(text)
    return [token.lower() for token in blob.words]


def filter_by_keywords(df, keywords_requirements):
    filtered_df = df.copy()
    # Filter the dataframe by the keywords
    filtered_df = filtered_df[
        df_filtering_function(filtered_df["description"], keywords_requirements)
    ]
    return filtered_df


def df_filtering_function(
    df_description_column: pd.Series, keyword_requirements: List[List[str]]
):
    # Transform df column with description string to a boolean indicating whether the description contains one of the keywords
    df_description_column = df_description_column.copy()
    return df_description_column.apply(
        lambda description: all(
            single_requirement_description_filter(description, keyword_alternatives)
            for keyword_alternatives in keyword_requirements
        )
    )


def single_requirement_description_filter(
    description: str, keyword_alternatives: List[str]
) -> bool:
    for keyword in keyword_alternatives:
        # Check if the description contains the keyword literally

        # Similar to this but with regex
        literal_match = re.search(keyword, description, re.IGNORECASE) is not None
        if not literal_match:
            continue
        # Check if the description contains a word that is a match to the keyword
        word_match = keyword.lower() in tokenize(description)
        # If both conditions are true, return True
        if literal_match and word_match:
            return True
    return False


if __name__ == "__main__":
    # Read the CSV file
    df = filter_by_keywords(read_from_csv(JOBS_NEW), KEYWORDS_REQUIREMENTS)
    # Print the filtered dataframe
    print(df)
    # Save the filtered dataframe to a new CSV file
    save_to_csv(df, JOBS_KEYWORD_MATCHED_CSV)
