import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, TOP_K
from ingest import chunk_documents, load_documents

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        print(f"[retriever] Loading embedding model '{EMBEDDING_MODEL}'...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(
            CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def _clean_metadata(meta):
    """Replace None values with '' — ChromaDB only accepts str/int/float/bool."""
    return {k: (v if v is not None else "") for k, v in meta.items()}


def embed_and_store(chunks=None):
    """Embed all chunks and upsert into ChromaDB. Safe to re-run."""
    if chunks is None:
        docs = load_documents()
        chunks = chunk_documents(docs)

    model = _get_model()
    collection = _get_collection()

    texts = [c["text"] for c in chunks]
    metadatas = [_clean_metadata(c["metadata"]) for c in chunks]
    ids = [
        f"{c['metadata']['source_file']}_{c['metadata']['chunk_index']}"
        for c in chunks
    ]

    print(f"[embed_and_store] Embedding {len(chunks)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    print(f"[embed_and_store] Stored {len(chunks)} chunks in '{CHROMA_COLLECTION}' at {CHROMA_PATH}")


def retrieve(query, filters=None, top_k=TOP_K):
    """Return the top_k most similar chunks to query.

    Args:
        query:   natural-language question
        filters: optional ChromaDB `where` dict, e.g. {"professor_name": "John-Paul Ore"}
        top_k:   number of results (default TOP_K from config)

    Returns:
        list of dicts — {text, metadata, distance}
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode([query]).tolist()
    kwargs = dict(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    if filters:
        kwargs["where"] = filters

    results = collection.query(**kwargs)

    return [
        {"text": text, "metadata": meta, "distance": dist}
        for text, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


# ── smoke-test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    embed_and_store()

    test_queries = [
        "Who is a better professor for CSC 326 — Sarah Heckman or John-Paul Ore?",
        "How is Professor Kemafor Ogan?",
        "Tips for CSC 116 with Dr. Schmidt?",
        "good professor for CSC 326",
        "pineapple pizza",
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        results = retrieve(query)
        for i, r in enumerate(results, 1):
            m = r["metadata"]
            print(
                f"  [{i}] dist={r['distance']:.4f} | "
                f"{m['source_file']} #{m['chunk_index']} | "
                f"prof={m['professor_name']} course={m['course_name']}"
            )
            print(f"      {r['text'][:120]}...")
