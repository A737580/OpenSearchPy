from opensearchpy import OpenSearch, RequestsHttpConnection
from .config import settings
from typing import List, Dict
from typing import Optional
from core.models import ContentType

client = OpenSearch(
    hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
    http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    connection_class=RequestsHttpConnection
)

MAPPING = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "content_type": {"type": "text"}
        }
    }
}

def create_index():
    """Создает индекс с заданным маппингом."""
    if not client.indices.exists(index=settings.OPENSEARCH_INDEX_NAME):
        client.indices.create(index=settings.OPENSEARCH_INDEX_NAME, body=MAPPING)

def index_documents(documents: List[Dict]):
    """Загружает документы в индекс."""
    for doc in documents:
        client.index(
            index=settings.OPENSEARCH_INDEX_NAME,
            body=doc,
            refresh=True
        )
def search_documents(query: Optional[str] = None, content_type: Optional[ContentType] = None) -> List[Dict]:
    """Ищет документы по ключевому слову и фильтру."""
    body = {
        "query": {
            "bool": {
                "must": [],  
                "filter": []
            }
        }
    }

    if query:
        body["query"]["bool"]["must"].append(
            {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content"]
                }
            }
        )

    elif not query:
        body["query"]["bool"]["must"].append(
            {
                "match_all": {}
            }
        )
    
    if content_type:
        body["query"]["bool"]["filter"].append(
            {
                "term": {
                    "content_type": content_type.value
                }
            }
        )

    search_result = client.search(index=settings.OPENSEARCH_INDEX_NAME, body=body)
    
    results = []
    for hit in search_result['hits']['hits']:
        source = hit['_source']
        snippet = source['content'][:50] + "..." if len(source['content']) > 50 else source['content']
        results.append({
            "title": source['title'],
            "snippet": snippet
        })
    return results