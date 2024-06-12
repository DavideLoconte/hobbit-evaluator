import typing as T
import json

import owlready2 as owl

SPARQLWrapperGraph = T.Dict

def write_text(response: str, filename: str) -> None:
    with open(filename, 'w') as f:
        f.write(response)

def write_dbpedia(response: SPARQLWrapperGraph, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(response, f)

def write_ontology(response: owl.Ontology, filename: str) -> None:
    response.save(filename)