#!/usr/bin/env python3

from http.client import HTTPConnection
from json import dumps

DEFAULT_OPENSEARCH_URL = "localhost"
DEFAULT_OPENSEARCH_PORT = 9200

INDEX_NAME = "store"
INDEX = {
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "fields": {
                    "autocomplete": {
                        "type": "text",
                        "analyzer": "autocomplete_indexing",
                        "search_analyzer": "autocomplete_search",
                    },
                },
            },
        },
    },
    "settings": {
        "index": {
            "number_of_shards": "1",
            "number_of_replicas": "0",
            "analysis": {
                "analyzer": {
                    "autocomplete_indexing": {
                        "type": "custom",
                        "char_filter": ["autocomplete_nfd", "autocomplete_mapping"],
                        "tokenizer": "icu_tokenizer",
                        "filter": ["autocomplete_shingle", "autocomplete_edge_ngram"],
                    },
                    "autocomplete_search": {
                        "type": "custom",
                        "char_filter": ["autocomplete_nfd", "autocomplete_mapping"],
                        "tokenizer": "icu_tokenizer",
                    },
                },
                "char_filter": {
                    "autocomplete_mapping": {
                        "type": "mapping",
                        "mappings": [
                            "ᆨ => ᄀ",
                            "ᆩ => ᄁ",
                            "ᆪ => ᄀᄉ",
                            "ᆫ => ᄂ",
                            "ᆬ => ᄂᄌ",
                            "ᆭ => ᄂᄒ",
                            "ᆮ => ᄃ",
                            "ᆯ => ᄅ",
                            "ᆰ => ᄅᄀ",
                            "ᆱ => ᄅᄆ",
                            "ᆲ => ᄅᄇ",
                            "ᆳ => ᄅᄉ",
                            "ᆴ => ᄅᄐ",
                            "ᆵ => ᄅᄑ",
                            "ᆶ => ᄅᄒ",
                            "ᆷ => ᄆ",
                            "ᆸ => ᄇ",
                            "ᆹ => ᄇᄉ",
                            "ᆺ => ᄉ",
                            "ᆻ => ᄊ",
                            "ᆼ => ᄋ",
                            "ᆽ => ᄌ",
                            "ᆾ => ᄎ",
                            "ᆿ => ᄏ",
                            "ᇀ => ᄐ",
                            "ᇁ => ᄑ",
                            "ᇂ => ᄒ",
                        ],
                    },
                    "autocomplete_nfd": {"mode": "decompose", "type": "icu_normalizer"},
                },
                "filter": {
                    "autocomplete_edge_ngram": {
                        "type": "edge_ngram",
                        "min_gram": "1",
                        "max_gram": "100",
                    },
                    "autocomplete_shingle": {
                        "type": "shingle",
                        "min_shingle_size": "2",
                        "max_shingle_size": "2",
                        "token_separator": "",
                    },
                },
            },
        },
    },
}


def create_index():
    body = dumps(INDEX)
    headers = {"Content-Type": "application/json"}

    connection = HTTPConnection(DEFAULT_OPENSEARCH_URL, DEFAULT_OPENSEARCH_PORT)
    connection.request("PUT", f"/{INDEX_NAME}", body, headers)

    response = connection.getresponse()

    if response.status != 200:
        connection.close()
        raise Exception(f"failed to create index: {response.status} {response.reason}")


if __name__ == "__main__":
    create_index()
