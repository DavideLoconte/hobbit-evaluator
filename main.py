import os
import csv
import sys
import tqdm
import typing as T

from config import *
from pipeline.metric import set_corpus

def main() -> int:
    queries = sys.argv[1:] if len(sys.argv) > 1 else QUERIES
    header = table_header(SOURCES, SOURCE_TYPE, METRICS)
    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(os.path.join(RESULT_DIR, 'results.csv'), 'w') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        rows = table_rows(queries, SOURCES, SOURCE_TYPE, METRICS, WRITERS)
        writer.writerows(rows)
    return 0

def table_header(sources: SourceDictType,
                 source_type: SourceTypeType,
                 metrics: Metrics) -> T.List[T.List[str]]:
    header = ['query']
    for source_name, source in sources.items():
        source_output_type = source_type[source_name]

        for metric in metrics[source_output_type]:
            header.append(f'{source_name}_{metric}')

    return header

def table_rows(queries: T.List[str],
               sources: SourceDictType,
               source_type: SourceTypeType,
               metrics: Metrics,
               writers: WriterTypes) -> T.List[T.List[str]]:
    rows = {}
    for query in queries:
        rows[query] = {'query': query}

    for source_name, source in sources.items():
        os.makedirs(os.path.join(CORPUS_DIR, source_name), exist_ok=True)
        source_output_type = source_type[source_name]
        writer = writers[source_output_type]
        print("Building corpus from source {}".format(source_name))
        corpus = [source(query) for query in tqdm.tqdm(queries)]
        set_corpus(corpus)

        for query, response in zip(queries, corpus):
            writer(response, os.path.join(CORPUS_DIR, source_name, f'{query}'))
            for metric_name, metric in metrics[source_output_type].items():
                rows[query][f'{source_name}_{metric_name}'] = metric(response)

    return list(rows.values())

if __name__ == "__main__":
    sys.exit(main())