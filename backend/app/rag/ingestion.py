import json
import logging
import os
from app.rag.vector_store import get_hospital_collection
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)


def ingest_hospital_knowledge(force_reindex: bool = False):
    """
    Ingests hospital clinical guides, department overviews, lab preparations,
    and emergency protocols into ChromaDB.
    """
    collection = get_hospital_collection()
    count = collection.count()

    if count > 0 and not force_reindex:
        logger.info(f"ChromaDB hospital collection already contains {count} knowledge chunks. Skipping reindex.")
        return

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_dir = os.path.dirname(backend_dir)
    possible_paths = [
        os.path.join(root_dir, "data", "hospital_data.json"),
        os.path.join(backend_dir, "data", "hospital_data.json"),
        os.path.join(os.getcwd(), "data", "hospital_data.json"),
    ]
    json_path = None
    for p in possible_paths:
        if os.path.exists(p):
            json_path = p
            break

    if not json_path:
        logger.warning(f"Hospital data file not found in possible locations: {possible_paths}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    embedder = get_embeddings_model()
    docs = []
    metadatas = []
    ids = []

    # 1. Department Chunks
    for d in data.get("departments", []):
        dept_text = (
            f"Department: {d['name']}. Location: {d['floor_location']}. "
            f"Head of Department: {d.get('head_doctor')}. Contact Ext: {d.get('contact_ext')}. "
            f"Clinical Scope & Care: {d['description']}"
        )
        docs.append(dept_text)
        metadatas.append({"category": "department", "name": d["name"]})
        ids.append(f"dept_{d['id']}_{d['name'].lower().replace(' ', '_')[:20]}")

    # 2. Lab Test Chunks
    for test in data.get("lab_tests", []):
        fasting_str = "Yes, 10-12 hours overnight fasting mandatory" if test.get("fasting_required") else "No fasting required"
        test_text = (
            f"Diagnostic Lab Test: {test['name']} ({test['sample_type']}). "
            f"Department: {test.get('department')}. Fasting Required: {fasting_str}. "
            f"Result Turnaround: {test.get('turnaround_hours')} hours. Fee: ₹{test['price_inr']}. "
            f"Clinical Purpose: {test.get('description')}"
        )
        docs.append(test_text)
        metadatas.append({"category": "lab_test", "name": test["name"]})
        ids.append(f"lab_{test['name'].lower().replace(' ', '_')[:25]}")

    # 3. Hospital Protocol Chunks
    for idx, proto in enumerate(data.get("hospital_protocols", []), 1):
        docs.append(f"Hospital Policy & Protocol: {proto}")
        metadatas.append({"category": "protocol", "id": idx})
        ids.append(f"protocol_{idx}")

    logger.info(f"Computing embeddings for {len(docs)} clinical documents...")
    embeddings = embedder.embed_documents(docs)

    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Successfully indexed {len(docs)} clinical knowledge chunks into ChromaDB!")
