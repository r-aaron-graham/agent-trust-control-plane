import json
from pathlib import Path

data_path = Path("app/data/sample_documents.json")
docs = json.loads(data_path.read_text(encoding="utf-8"))
print(f"Loaded {len(docs)} sample documents from {data_path}")
for doc in docs:
    print(f"- {doc['doc_id']}: {doc['title']} [{doc['classification']}]")
