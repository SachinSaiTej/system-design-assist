import os
from typing import List, Tuple
import chromadb
from chromadb.utils import embedding_functions
from rapidfuzz import fuzz
from models.llm import LocalLLM

SYSTEM_PROMPT = """You are a rigorous system design assistant.
Provide capacity estimates, trade-offs, architecture, APIs, scaling, failure modes, and SLOs.
Include a single Mermaid diagram if useful.
Cite sources as [LOCAL:filename] or [WEB:domain]."""

class SystemDesignRAG:
    def __init__(self, collection_name="sysdesign", embed_model="sentence-transformers/all-MiniLM-L6-v2",
                 llm_backend="ollama", llm_model="llama3.1:8b"):
        self.client = chromadb.PersistentClient(path=".chroma")
        self.embed = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model)
        self.col = self.client.get_or_create_collection(collection_name=collection_name, embedding_function=self.embed)
        self.llm = LocalLLM(backend=llm_backend, model=llm_model)

    def retrieve(self, query: str, k: int = 8) -> List[Tuple[str, str]]:
        results = self.col.query(query_texts=[query], n_results=k)
        chunks = [(m, t) for m, t in zip(results.get("metadatas", [[]])[0], results.get("documents", [[]])[0])]
        uniq = []
        for src, txt in chunks:
            if all(fuzz.token_set_ratio(txt, t2) < 90 for _, t2 in uniq):
                uniq.append((src, txt))
        return uniq

    def _build_prompt(self, user_q: str, passages: List[Tuple[str, str]], web_results: List[dict]):
        ctx = []
        for meta, txt in passages:
            label = meta.get("path") if isinstance(meta, dict) else str(meta)
            ctx.append(f"[LOCAL::{label}]\n{txt}")
        for w in web_results:
            ctx.append(f"[WEB::{w.get('title','')}] {w.get('url')}\n{w.get('snippet','')}")
        return f"{SYSTEM_PROMPT}\n\nContext:\n" + "\n\n".join(ctx) + f"\n\nUser Question:\n{user_q}"

    def answer(self, user_q: str, passages: List[Tuple[str,str]], web_results: List[dict]):
        prompt = self._build_prompt(user_q, passages, web_results)
        output = self.llm.complete(prompt)

        mermaid = None
        if "```mermaid" in output:
            try:
                mermaid = output.split("```mermaid")[1].split("```")[0].strip()
            except Exception:
                pass

        citations = [line.strip() for line in output.splitlines() if "[LOCAL:" in line or "[WEB:" in line]
        return output, mermaid, citations
    def generate(self, question: str) -> str:
        # Implement your RAG logic here
        # For now, returning a placeholder response
        return f"System design answer for: {question}"
