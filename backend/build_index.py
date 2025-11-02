import os, glob, uuid
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from markdown_it import MarkdownIt

def _chunk_text(text, chunk_size=1200, overlap=200):
    i = 0
    while i < len(text):
        yield text[i:i+chunk_size]
        i += chunk_size - overlap

def _read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def _read_md(path):
    md = open(path, "r", encoding="utf-8").read()
    parsed = MarkdownIt().render(md)
    return md + "\n" + parsed

def build_index():
    client = chromadb.PersistentClient(path=".chroma")
    embed = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ✅ recreate collection safely
    collection_name = "sysdesign"
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    col = client.create_collection(name=collection_name, embedding_function=embed)

    docs, metas, ids = [], [], []
    for ext in ("*.pdf", "*.md", "*.txt"):
        for path in glob.glob(os.path.join("data", ext)):
            try:
                if path.endswith(".pdf"):
                    text = _read_pdf(path)
                elif path.endswith(".md"):
                    text = _read_md(path)
                else:
                    text = open(path, "r", encoding="utf-8").read()
            except Exception as e:
                print("Skip:", path, e)
                continue
            for chunk in _chunk_text(text):
                docs.append(chunk)
                metas.append({"path": path})
                ids.append(str(uuid.uuid4()))

    if docs:
        col.add(documents=docs, metadatas=metas, ids=ids)
        print(f"✅ Indexed {len(docs)} chunks from {len(set(m['path'] for m in metas))} files.")
    else:
        print("⚠️ No documents found in ./data")

if __name__ == "__main__":
    build_index()
