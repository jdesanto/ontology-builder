# Ontology Builder

Ontology Builder is a low-code library to build ontologies from source data holding explicit semantic relationships. 
Once exported to a standard semantic web format, it is easier to view and manipulate semantic content than in the 
original .toml, .json, or spreadsheet.

## Quick Start

### Building the Pet Ontology

Components:
- Source data in `./samples/pets` (toml files)
- Ontology metadata in `./templates/simple_pet_ontology.yaml`
- `PetOntology` class in `./ontology/pet_ontology.py`

To run

```
pip install -e requirements.txt

python ontology_builder.py -m templates/simple_pet_ontology.yaml
```

The output is a file as listed in the metadata. It can be imported by [Protégé](https://protege.stanford.edu)

## Prerequisites

There are two components, a metadata file describing the ontology and an ontology class where the semantic relations are 
converted to RDF triples

### Metadata

The build engine needs to know how to process the source. This is a sample metadata yaml (see `./templates`).

```yaml
name: Pet Ontology
ontology: PetOntology
class_definition: ./ontology/pet_ontology.py
namespace: http://aevea.com/ontologies/pets#
source_directory: ./samples/pets
file_extension: .toml
output_file: pets.ttl
classes:
  - Human
  - Animal
predicates:
  - caregiver_for: OWL.ObjectProperty
  - sibling_of: OWL.ObjectProperty
  - name: OWL.DatatypeProperty
entity_name_field: name
handlers:
  - name
  - type
  - has_sibling
  - caregiver_for
```

These are used as follows:

- name - The name of the ontology.
- ontology - The class that creates triples from the source
- class_definition - The Python file where the ontology class is defined
- namespace - Default namespace for the ontology (defaults to "http://example.org/")
- source_directory - The root folder for source files
- file_extension - The file extension for source files that are processed
- output_file - The serialized ontology outputted to a file
- classes - Classes required for the ontology
- predicates - Predicates and corresponding types required for the ontology
- entity_name_field - The source data field used to create the ontology entty
- handlers - custom functions that create the ontology triples

### Ontology Class

For the main ontology class to know how to build the ontology it needs a way to create triples from the source content. This is done in the `PetOntology` class as follows

#### Create primary entity

`lucy.toml` consists of 

```toml
name = "Lucy"
type = "Cat"

siblings = ["Shadow"]
```  

This file is about Lucy. The build function calls the `create_subject` method to create the triple `("Lucy" RDF.type "Cat")` where "Cat" was already created as a class declared in the metadata. "Lucy" and "Cat" both use the namespace defined in the metadata.

#### Predicate Handlers

Relationships correspond to the handlers listed in the metadata. For example, the builder knows how to create a triple from the "siblings" key in the toml

```python
def handle_siblings(self, item_data):
    siblings = item_data.get('siblings')

    if siblings is not None:
        for sibling in siblings:
            self.add_triple(self.entity, self.ns['has_sibling'], self.ns[sibling])
```

Every key used to generate triples must be included in the metadata handlers section, and every such key corresponds to a method named `handle_<key>` that takes the file payload and creates triples.

## Detailed Usage

This is a full end-to-end explanation using the pets data set.

The metadata file is already defined. See `templates/simple_pet_ontology.yaml` (see above).

The ontology is built off `.toml` files. For example, `shadow.toml` consists of

```toml
name = "Shadow"
type = "Cat"

siblings = ["Lucy"]
```

This becomes triples as follows:
- The `PetOntology` method `create_subject` creates the triple ("Shadow" RDF.type "Cat").
- The `handle_siblings` method creates the triple ("Shadow" "has_sibling" "Lucy"). Note that `has_sibling` was included in the metadata a predicate with type OWL.ObjectTypeProperty whereas `siblings` is a field in the toml. 




