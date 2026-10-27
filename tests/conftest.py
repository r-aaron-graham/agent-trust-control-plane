import os
import shutil
import tempfile
from pathlib import Path

# Tests must never write to the tracked sample corpus. Point the retriever at a
# throwaway copy before any app module (and its singletons) is imported.
_ROOT = Path(__file__).resolve().parents[1]
_TMP = Path(tempfile.mkdtemp(prefix="atcp-tests-")) / "documents.json"
shutil.copy(_ROOT / "app" / "data" / "sample_documents.json", _TMP)
os.environ.setdefault("RETRIEVAL_DATA_PATH", str(_TMP))
