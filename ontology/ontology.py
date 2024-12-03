#!/usr/bin/env python3

# Standard library
import os
import logging

# Third party imports
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import OWL, RDF, RDFS, XSD

# Local imports
import utils

# Defaults
NAMESPACE = "http://example.org/"

log_level = "INFO" or os.env.get('LOG_LEVEL', None)
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

class Ontology:
    
    def __init__(self, metadata):
        """
        Establish the empty graph and metadata defining the ontology
        
        Args:
            metadata (dict): Dictionary representation of the yaml file that defines the ontologyt
            
        Returns:
            An instance of the class
        """
        self.G = Graph()
        self.metadata = metadata

    def add_triple(self, s, p, o):
        """
        Wrapper for Graph.add method.
        
        Args:
            s, o, p: RDF resource URIs used to form the triple
            
        Returns:
            Nothing
        """
        self.G.add((s,p,o))

    def bind_namespace(self):
        """
        Bind the namespace referenced in the ontology metadata. Use NAMESPACE if the former is empty.
        This function takes no arguments and returns no value
        """
        self.ns = Namespace(self.metadata.get("namespace", NAMESPACE))
        self.G.bind("ns", self.ns)
    
    def export_to_file(self, destination):
        """
        Serialize and save the ontology to `destination`.
        
        Args:
            destination (str): path to save the ontology
            
        Returns:
            Nothing
        """
        self.G.serialize(destination=destination)

    def initialize(self):
        """
        Creates classes and predicates used by the ontology. These are defined in the ontology yaml file.
        Takes no arguments and returns no value
        """
        
        # Create triples for classes referenced in the metadata yaml
        classes = self.metadata.get("classes")
        if classes is not None:
            for c in classes:
                self.add_triple(self.ns[c], RDF.type, RDFS.Class)
                
        # Create predicates referenced in the metadata yaml
        predicates = self.metadata.get("predicates")
        if predicates is not None:
            for p_dict in predicates:
                for p_name, p_type in p_dict.items():
                    self.add_triple(self.ns[p_name], RDF.type, eval(p_type))


if __name__ == "__main__":
    o = CryptoOntology("http://aevea.com/ontologies/crypto#")
    o.initialize()
    o.process_source("/Users/john/Documents/code/github/crypto-ecosystems/data/ecosystems", ".toml")
    o.export_to_file("onto.ttl")
    
