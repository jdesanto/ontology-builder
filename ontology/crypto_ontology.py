#!/usr/bin/env python3
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib import URIRef, Literal

def get_github_org(url):
    """
    Extract the organization from a Guthub URL.

    Args:
        url (str): Github URL

    Returns:
        Github organization
    """
    if not url.startswith("https://github.com/"):
        return None
    
    org = url.split('/')[-1]
    return org

class CryptoOntology(Ontology):

    def __init__(self, metadata):
        super().__init__(metadata)
        
    def create_subject(self, item_data):
        """
        Create the primary entity.
        """
        ecosystem = self.ns[string_to_rdf_resource(item_data['title'])]
        self.add_triple(ecosystem, RDF.type, self.ns['Ecosystems'])
        #self.add_triple(ecosystem, self.metadata['filename'], Literal(filename, lang='en'))
        self.entity = ecosystem
  
    def handle_sub_ecosystems(self, item_data):
        sub_ecosystems = item_data.get('sub_ecosystems')
        ecosystem = self.entity
        if sub_ecosystems is not None:
            for se in sub_ecosystems:
                sub_ecosystem = self.ns[string_to_rdf_resource(se)]
                self.add_triple(sub_ecosystem, RDF.type, self.ns['Ecosystems'])
                self.add_triple(sub_ecosystem, self.ns['sub_ecosystem_of'], ecosystem)
                
    def handle_github_organizations(self, item_data):
        github_orgs = item_data.get('github_organizations')
        ecosystem = self.entity

        if github_orgs is not None:
            for org_url in github_orgs:
                org_name = get_github_org(org_url)
                organization = self.ns[string_to_rdf_resource(org_name)]

                self.add_triple(organization, RDF.type, self.ns['Organizations'])
                self.add_triple(ecosystem, self.ns['has_organization'], organization)
                self.add_triple(organization, self.ns['has_url'], URIRef(org_url))

    def handle_repo(self, item_data):
        repos = item_data.get('repo')
        ecosystem = self.entity

        if repos is not None:
            for repo in repos:
                repo_uri = URIRef(repo['url'])
                self.add_triple(repo_uri, RDF.type, self.ns['Repositories'])
                self.add_triple(ecosystem, self.ns['has_repository'], repo_uri)
        
    def handle_title(self, item_data):
        title = item_data.get('title')
        ecosystem = self.entity
        self.add_triple(ecosystem, self.ns['has_title'], Literal(title))
