""" Tests for the filter_by_keywords file """

import pytest
import pandas as pd
from io import StringIO
from .filter_by_keywords import (
    tokenize,
    filter_by_keywords,
    df_filtering_function,
    single_requirement_description_filter,
)

# Mock CSV content
CSV_CONTENT = """description
React is a great frontend framework.
We use JavaScript and TypeScript for development.
Python and Node are backend technologies.
Our project involves AI and machine learning.
We do AI with React JS and Python.
"""


@pytest.fixture
def mock_csv_file():
    return StringIO(CSV_CONTENT)


@pytest.fixture
def mock_df(mock_csv_file):
    return pd.read_csv(mock_csv_file)


@pytest.fixture
def keyword_requirements():
    return [
        ["react", "next.js", "nextjs"],  # Frontend Framework
        ["js", "JavaScript", "TypeScript", "ts"],  # Language
        ["python", "py", "node"],  # Backend
        ["AI", "artificial intelligence", "llm", "machine learning", "ML"],  # AI
    ]


# Parametrized with strings that have ',' '.' and ' ' in them
@pytest.mark.parametrize(
    "source, tokenized",
    [
        (
            "React is a great frontend framework.",
            ["React", "is", "a", "great", "frontend", "framework"],
        ),
        (
            "We use JavaScript, and TypeScript for development.",
            ["We", "use", "JavaScript", "and", "TypeScript", "for", "development"],
        ),
        (
            'Python, and Node are "backend" technologies.',
            ["Python", "and", "Node", "are", "backend", "technologies"],
        ),
        (
            "Our project involves Next.js and AI.",
            ["Our", "project", "involves", "Next.js", "and", "AI"],
        ),
    ],
)
def test_tokenize(source, tokenized):
    assert tokenize(source) == [token.lower() for token in tokenized]


def test_description_filtering_function():
    description = "We use JavaScript and TypeScript for development."
    keywords = ["js", "JavaScript", "TypeScript", "ts"]
    assert single_requirement_description_filter(description, keywords) == True


def test_df_filtering_function(mock_df):
    keywords = ["js", "JavaScript", "TypeScript", "ts"]
    result_series = df_filtering_function(mock_df["description"], keywords)
    assert result_series.sum() == 1  # Only one row should match


def test_filter_by_keywords(mock_df, keyword_requirements):
    filtered_df = filter_by_keywords(mock_df, keyword_requirements)
    assert not filtered_df.empty
    assert len(filtered_df) == 1  # All descriptions match at least one keyword group
