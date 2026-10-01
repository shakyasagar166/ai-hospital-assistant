import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.rag.ingestion import ingest_hospital_knowledge
from app.rag.retriever import retrieve_hospital_knowledge, format_clinical_context
from app.rag.vector_store import get_hospital_collection


def test_rag():
    print("\n--- 3. Testing ChromaDB Clinical Vector RAG Pipeline ---")
    ingest_hospital_knowledge(force_reindex=False)

    col = get_hospital_collection()
    count = col.count()
    print(f"[OK] ChromaDB hospital collection count: {count}")
    assert count > 0, "No clinical documents indexed in ChromaDB"

    # Test semantic retrieval
    results = retrieve_hospital_knowledge("emergency chest pain visiting hours insurance", top_k=2)
    print(f"[OK] Retrieved {len(results)} chunks.")
    assert len(results) > 0, "Failed to retrieve relevant chunks"
    for r in results:
        print(f"   - Score: {r['score']}, Category: {r['metadata'].get('category')}")

    context = format_clinical_context(results)
    assert len(context) > 20, "Formatted context empty"
    print("[OK] Formatted clinical prompt context successfully.")

    print(">>> ChromaDB Clinical Vector RAG Test Passed Successfully!\n")


if __name__ == "__main__":
    test_rag()
