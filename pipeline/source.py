import ollama as llm
from wikipedia import page
from SPARQLWrapper import SPARQLWrapper, JSON

# Text Based

def wikipedia(query: str) -> str:
    """Return the wikipedia content of the query"""
    return page(query).content

def ollama(query: str, model: str = 'llama3', prompt: str = '{}') -> str:
    """Return the response of a query from a ollama model"""
    response = llm.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt.format(query),
    }])

    return response['message']['content']

# SPARQLWRAPPER based

SPARPQLWrapperGraph = dict

def sparqlwrapper(query: str) -> SPARPQLWrapperGraph:
    """Return the results of a SPARQL query"""
    DESCRIBE_QUERY = f"""
    PREFIX dbres: <http://dbpedia.org/resource/>

    DESCRIBE dbres:{query}
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(DESCRIBE_QUERY)  # the previous query as a literal string
    return sparql.query().convert()

# Graph Based