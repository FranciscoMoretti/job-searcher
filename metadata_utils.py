import json

from pipeline_config import METADATA_JSON
from typing import TypedDict


class Metadata(TypedDict):
    last_parsed_source_idx: int
    last_processed_job_idx: int


def read_metadata() -> Metadata:
    # Read the metadata from the metadata.json file
    metadata = read_from_json(METADATA_JSON)
    return metadata


def save_metadata(metadata: Metadata):
    # Save the metadata to the metadata.json file
    save_to_json(metadata, METADATA_JSON)


def read_from_json(file_name):
    # Open the JSON file
    with open(file_name, "r") as file:
        # Read from json with a dict
        data = json.load(file)
        return data


def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
