from chat_api.settings import chat_settings
from elasticsearch import Elasticsearch


def init_connection(create_index=False):
    connection = Elasticsearch(chat_settings.ELASTICSEARCH_URL)
    index_name = "chat_api-messages-{prefix}".format(prefix=chat_settings.ELASTICSEARCH_PREFIX)

    if create_index:
        # create an index in elasticsearch, ignore status code 400 (index already exists)
        body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "autocomplete": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "template": {
                    "properties": {
                        "text": {"type": "string", "analyzer": "autocomplete"},
                        "thread_user_full_name": {"type": "string"}
                    }
                }
            }
        }
        connection.indices.create(index=index_name, ignore=400, body=body)
    return connection, index_name


def index(message):
    if not chat_settings.ELASTICSEARCH_URL:
        return

    connection, index_name = init_connection(True)
    data = {
        "index": index_name,
        "id": message.id,
        "doc_type": "message",
        "body": {
            "created": message.created,
            "text": message.text,
            "thread_id": message.thread_id,
            "thread_user_full_name": message.sender.get_full_name() if message.sender else ""
        },
    }
    connection.index(**data)


def find_messages(queryset, search_term):
    if not chat_settings.ELASTICSEARCH_URL:
        return queryset.none()

    results = find(search_term)
    return queryset.filter(id__in=[obj["_id"] for obj in results])


def find_threads_with_messages(search_term):
    if not chat_settings.ELASTICSEARCH_URL:
        return {}

    results = find(search_term)
    return {obj["_source"]["thread_id"]: obj["_id"] for obj in reversed(results)}


def find(search_term):
    if not chat_settings.ELASTICSEARCH_URL:
        return []

    connection, index_name = init_connection()

    body = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase_prefix": {"_all": search_term}},
                ]
            }
        }
    }
    size = 10000  # Pagination will be handled by Django
    fields = ["hits.hits._id", "hits.hits._source.thread_id"]
    results = connection.search(index=index_name, body=body, size=size, from_=0, filter_path=fields,
                                sort="created:desc")
    if "hits" not in results:
        return []

    return [obj for obj in results["hits"]["hits"]]
