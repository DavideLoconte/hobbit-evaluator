import typing as T
import os
# User libs

from pipeline.source import wikipedia, ollama, sparqlwrapper
from pipeline.metric import words, entities, class_count, entity_count, edges, distinct_edges, nodes, set_corpus
from pipeline.writer import write_text, write_dbpedia, write_ontology

# Schema definition for configuration file

ModelIdentifier = str
Query = str
Response = T.Any

SourceDictType = T.Dict[
    ModelIdentifier,
    T.Callable[[Query], Response]
]

TypeSpec = Response
SourceTypeType = T.Dict[TypeSpec, TypeSpec]
Metrics = T.Dict[
    TypeSpec,
    T.Dict[str, T.Callable[[Response], float]]
]

WriterTypes = T.Dict[TypeSpec, T.Callable[[Response, str], None]]

# == Configs

PROMPT: str = 'I am knowledgeable about pharmacy. Please provide all information about {}'
RESULT_DIR = 'results'
CORPUS_DIR = os.path.join(RESULT_DIR, 'corpus')

SOURCES: SourceDictType = {
    'wikipedia': wikipedia,
    'ollama-llama3': lambda query: ollama(query, model='llama3', prompt=PROMPT),
    # 'ollama-phi3': lambda query: ollama(query, model='phi3', prompt=PROMPT),
    # 'ollama-mistral': lambda query: ollama(query, model='mistral', prompt=PROMPT),
    'dbpedia': sparqlwrapper,
}

SOURCE_TYPE: SourceTypeType = {
    'wikipedia': 'text',
    'ollama-llama3': 'text',
    'ollama-phi3': 'text',
    'ollama-mistral': 'text',
    'dbpedia': 'dbpedia'
}

METRICS: Metrics = {
    'text': {
        'words': words,
        'entities': entities
    },
    'dbpedia': {
        'nodes': nodes,
        'edges': edges,
        'distinct_edges': distinct_edges
    },
    'ontology': {
        'class_count': class_count,
        'entity_count': entity_count
    }
}

WRITERS: WriterTypes = {
    'text': write_text,
    'dbpedia': write_dbpedia,
    'ontology': write_ontology
}

QUERIES = [
    'Aspirin'
]