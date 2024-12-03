#!/usr/bin/env python3
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib import URIRef, Literal

class PetOntology(Ontology):

    def __init__(self, metadata):
        super().__init__(metadata)
        
    def create_subject(self, item_data):
        """
        Create the primary entity.
        """
        item = self.ns[string_to_rdf_resource(item_data['name'])]
        item_type = self.ns[string_to_rdf_resource(item_data['type'])]
        self.add_triple(item, RDF.type, item_type)
        self.entity = item
  
    def handle_name(self, item_data):
        item_name = item_data.get('name')
        if item_name is not None:
            self.add_triple(self.entity, self.ns['name'], Literal(item_name))
                
    def handle_siblings(self, item_data):
        siblings = item_data.get('siblings')

        if siblings is not None:
            for sibling in siblings:
                self.add_triple(self.entity, self.ns['has_sibling'], self.ns[sibling])

    def handle_caregiver_for(self, item_data):
        caregiver_for = item_data.get('caregiver_for')
        if caregiver_for is not None:
            for care_target in caregiver_for:
                self.add_triple(self.entity, self.ns['caregiver_for'], self.ns[care_target])

