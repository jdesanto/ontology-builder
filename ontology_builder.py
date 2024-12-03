#!/usr/bin/env python

# Standard imports
import importlib.util
import sys
from pathlib import Path
import yaml
import os

# Local imports
from utils import string_to_rdf_resource, walk_file_tree
from ontology.ontology import Ontology


def load_class_from_file(file_path, class_name, global_context=None):
    """
    Dynamically load a class from a file. This allows subclasses
    to reference the main Ontology class without importing it.

    Args:
        file_path (str): path to the metadata yaml file
        class_name (str): the name of the class to load

    Return:
        The class object
    """
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"Class file not found: {file_path}")

    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    if global_context is not None:
        module.__dict__.update(global_context)

    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def build_ontology(metadata):
    """
    Build and save the ontology according to the metadata. The ontology is
    created using the class name and definition included in the metadata.
    Once the ontology is created the steps are as follows:
    - Create the supporting classes/predicates from the metadata file
    - Loop through the file tree and process each file as follows:
      - Generate the underlying object.
      - Call each handler function. These functions serve to process the
        file payloads.
    - Save the ontology to a file
    """

    ontology_class_name = metadata["ontology"]
    class_definition_path = metadata["class_definition"]

    # Construct the subclass of Ontology that will hold this data.
    ontology_class = load_class_from_file(
        class_definition_path,
        ontology_class_name,
        global_context={
            "Ontology": Ontology,
            "string_to_rdf_resource": string_to_rdf_resource,
        },
    )

    # Instantiate the ontology class, bind the namespace, and create the initial
    # classes and predicates
    o = ontology_class(metadata)
    o.bind_namespace()
    o.initialize()

    # Walk the file tree and process each file
    source_directory = metadata["source_directory"]
    file_extension = metadata["file_extension"]
    for file_path, file_content in walk_file_tree(source_directory, file_extension):
        o.create_subject(file_content)
        for item in metadata["handlers"]:
            fn = getattr(o, "handle_" + item)
            fn(file_content)

    # Save the ontology
    o.export_to_file(metadata["output_file"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ontology builder.")
    parser.add_argument(
        "-m",
        "--metadata",
        type=str,
        help="Path to the yaml file defining the ontology.",
    )
    args = parser.parse_args()

    with open(args.metadata, "r") as fh:
        metadata = yaml.load(fh, Loader=yaml.SafeLoader)

    build_ontology(metadata)
