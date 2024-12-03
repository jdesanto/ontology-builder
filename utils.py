#!/usr/bin/env python3

import os
import toml, json
import re
from urllib.parse import quote


def string_to_rdf_resource(string):
    """
    Converts a string into a valid RDF resource name.

    Args:
        base_uri (str): The base URI for the RDF resource (e.g., "http://example.org/").
        string (str): The input string to convert into a valid resource name.

    Returns:
        str: A valid RDF resource URI.
    """

    # Remove leading and trailing whitespace
    string = string.strip()

    # Replace spaces and special characters with valid alternatives
    # Convert to lowercase, replace spaces with underscores
    string = re.sub(r"\s+", "_", string)

    # Remove invalid characters (retain alphanumeric, _, -, ., ~)
    string = re.sub(r"[^\w\-\.~]", "", string)

    # Percent-encode remaining characters if necessary (for reserved URI components)
    string = quote(string)

    return string


def walk_file_tree(root_path, extension=None):
    """
    Traverse a directory tree starting with `root_path` and process each file with
    `extension`. Yields the contents of each file as a dictionary. Raise errors
    if the `root_path` does not exist or if the file extension is not supported.

    Args:
        root_path (str): the root path to start walking
        extension (str): the file extension for processed files

    Returns:
        file_path, file_content (str, dict)
    """

    loader_functions = {".toml": toml.load, ".json": json.load}

    if extension not in loader_functions:
        raise ValueError(f"{extension} is not supported.")

    loader_function = loader_functions[extension]

    if not os.path.exists(root_path):
        raise ValueError(f"{root_path} does not exist.")

    for dir_path, _, filenames in os.walk(
        root_path,
    ):
        for filename in filenames:
            if filename.endswith(extension):
                file_path = os.path.join(dir_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_content = loader_function(file)
                        yield file_path, file_content
                except Exception as e:
                    yield file_path, {"error": str(e)}


if __name__ == "__main__":
    p = "/Users/john/Documents/code/github/crypto-ecosystems/data/ecosystems"
    for f, data in walk_file_tree(p, ".toml"):
        print(f)
        print(data)
        break
