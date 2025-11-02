import streamlit as st
from rag_pipeline import SystemDesignRAG
from tools.research import ResearchTool

st.set_page_config(page_title="System Design Assistant", layout="wide")

st.title("🧠 System Design Assistant (Local)")
st.caption("Local RAG + LLM + optional web research + Mermaid diagrams")

with st.sidebar:
    st.header("Settings")
    llm_backend = st.selectbox("LLM backend", ["ollama", "llama.cpp"], index=0)
    llm_model = st.text_input("Model name", "llama3.1:8b")
    do_research = st.checkbox("Enable web research", value=False)
    num_results = st.slider("RAG results", 1, 20, 8)
    st.markdown("---")
    if st.button("Rebuild Index"):
        from build_index import build_index
        with st.spinner("Rebuilding index..."):
            build_index()
        st.success("Index rebuilt!")

rag = SystemDesignRAG(collection_name="sysdesign", embed_model="sentence-transformers/all-MiniLM-L6-v2",
                      llm_backend=llm_backend, llm_model=llm_model)

research = ResearchTool()

prompt = st.text_area("Enter your system design problem:", height=180,
                      placeholder="e.g., Design a global rate limiter for 100k RPS...")

if st.button("Generate Design"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    web_results = []
    if do_research:
        with st.spinner("Running web research..."):
            web_results = research.search(prompt, k=5)

    with st.spinner("Retrieving local context..."):
        passages = rag.retrieve(prompt, k=num_results)

    with st.spinner("Synthesizing answer..."):
        answer, mermaid_code, citations = rag.answer(prompt, passages, web_results)

    st.markdown("## 📘 Answer")
    st.markdown(answer)

    if mermaid_code:
        st.markdown("## 🪄 Diagram")
        st.markdown(f"```mermaid\n{mermaid_code}\n```")

    if citations:
        st.markdown("## 🔗 Citations")
        for c in citations:
            st.markdown(f"- {c}")

st.caption("Tip: Put PDFs/MD in `data/` and rebuild the index.")


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from rag_pipeline import SystemDesignRAG

# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods
#     allow_headers=["*"],  # Allow all headers
# )
# rag = SystemDesignRAG()

# class Query(BaseModel):
#     question: str

# @app.post("/design")
# async def design(q: Query):
#     answer = rag.generate(q.question)
#     return {"answer": answer}
