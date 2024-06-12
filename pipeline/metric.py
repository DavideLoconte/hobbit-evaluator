import typing as T
import io
import owlready2 as owl
import spacy

# Globals
_nlp = spacy.load("en_core_web_sm")

# Corpus
_corpus = None
_context = None

def set_corpus(corpus: T.List[str]) -> None:
    global _corpus
    global _context
    _corpus = corpus
    _context = None

# Ontology Based

def class_count(ontology: owl.Ontology) -> int:
    """
    Count the number of classes in an ontology
    """
    return len(list(ontology.classes()))

def entity_count(ontology: owl.Ontology) -> int:
    """
    Count the number of entities in an ontology
    """
    return len(list(ontology.individuals()))

# Text Based

def words(string: str) -> float:
    """
    This metric return the number of unique words normalized
    by the length of the document
    """
    doc = _nlp(string)
    filtered_words = set([token.text.lower().strip() for token in doc if not token.is_stop])
    return len(filtered_words)

def entities(string: str) -> float:
    """
    This metric return the number of unique entities normalized
    by the length of the document
    """
    doc = _nlp(string)
    return len(set([ent.label_ for ent in doc.ents]))

# SPARQLWRAPPER based

SPARPQLWrapperGraph = dict

def __get_bindings(graph: SPARPQLWrapperGraph) -> dict:
    """
    Extract the list of triples from the graph object
    returned by SPARQLWrapper library
    """
    return graph['results']['bindings']

def nodes(graph: SPARPQLWrapperGraph) -> int:
    """
    Return the number of unique nodes in the graph
    """
    nodes = []
    for binding in __get_bindings(graph):
        for node_type in ['s', 'o']:
            node = binding.get(node_type)
            if node is not None:
                nodes.append(node['value'])
    return len(set(nodes))

def edges(graph: SPARPQLWrapperGraph) -> int:
    """
    Return the absolute number of edges
    """
    return len(__get_bindings(graph))

def distinct_edges(graph: SPARPQLWrapperGraph) -> int:
    """
    Return the number of uniques edges
    """
    edges = []
    for binding in __get_bindings(graph):
        edge = binding.get('p')
        if edge is not None:
            edges.append(edge['value'])
    return len(set(edges))

# Graph Based
