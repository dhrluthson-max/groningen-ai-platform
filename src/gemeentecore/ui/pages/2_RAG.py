# src/gemeentecore/ui/pages/2_RAG.py
import streamlit as st
import asyncio
from datetime import datetime
import hashlib
import structlog

# Veilige imports uit jouw eigen framework
from gemeentecore.models.state import SessionState, ChatMessage
from gemeentecore.services.rag_pipeline import RAGPipeline
from gemeentecore.ui.components import render_sidebar, render_metric_card
from gemeentecore.config import settings

# Extra vangnet voor DocumentMetadata mocht deze uniek gedefinieerd zijn
try:
    from gemeentecore.models.domain import DocumentMetadata
except ImportError:
    # Fallback klasse als het model elders staat gedefinieerd
    from dataclasses import dataclass
    @dataclass
    class DocumentMetadata:
        file_name: str
        file_hash: str
        upload_time: datetime
        num_pages: int
        num_chunks: int
        status: str

log = structlog.get_logger()
state = SessionState.get()
rag = RAGPipeline()  # Gecached via @st.cache_resource

st.set_page_config(page_title="RAG Engine", page_icon="🧠", layout="wide")
render_sidebar()

st.title("🧠 Intelligente Document Analyse (RAG)")
st.caption(f"Model: `{settings.LLM_MODEL}` | Embedding: `{settings.EMBEDDING_MODEL}` | Vector DB: ChromaDB")

# --- SYNCHRONE BRUG-FUNCTIES (Dit voorkomt alle Async/Await Pylance fouten!) ---
def run_async_task(coro):
    """Voert asynchrone backend-taken veilig synchroon uit voor Streamlit."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def sync_generator_wrapper(async_gen_coro):
    """Zet jouw async generator om naar een synchrone stream voor st.write_stream."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Start de asynchrone generator via de loop
        async_gen = loop.run_until_complete(async_gen_coro)
        while True:
            try:
                token = loop.run_until_complete(async_gen.__anext__())
                yield token
            except StopAsyncIteration:
                break
    finally:
        loop.close()

# --- Upload Zone ---
with st.container(border=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded = st.file_uploader("Upload Vertrouwelijk Document (PDF)", type="pdf", label_visibility="collapsed")
    with col2:
        if uploaded and st.button("🔒 Verwerk & Indexeer", type="primary", use_container_width=True):
            with st.status("Document verwerken...", expanded=True) as status:
                try:
                    file_bytes = uploaded.getvalue()
                    f_hash = hashlib.sha256(file_bytes).hexdigest()[:16]
                    
                    if f_hash in state.documents:
                        st.warning("Document al geïndexeerd in deze sessie.")
                    else:
                        st.write("📄 Tekst extractie & Chunking...")
                        
                        # AANROEP VIA VEILIGE BRUG (Geen losse 'await' meer!)
                        doc_hash, n_chunks = run_async_task(rag.ingest_pdf(file_bytes, uploaded.name))
                        
                        state.documents[doc_hash] = DocumentMetadata(
                            file_name=uploaded.name, file_hash=doc_hash, 
                            upload_time=datetime.now(), num_pages=0,
                            num_chunks=n_chunks, status="indexed"
                        )
                        state.current_doc = state.documents[doc_hash]
                        state.messages = [ChatMessage(role="assistant", content=f"✅ **{uploaded.name}** geïndexeerd ({n_chunks} chunks). Stel je vraag.")]
                        status.update(label="Klaar!", state="complete")
                except Exception as e:
                    log.error("ingest_failed", error=str(e))
                    status.update(label=f"Fout: {e}", state="error")

# --- Chat Interface (Fragment = Partial Rerun) ---
@st.fragment(run_every="10s")
def chat_interface():
    # Render History
    for msg in state.messages:
        with st.chat_message(msg.role):
            st.markdown(msg.content)
            if msg.citations:
                with st.expander("📚 Bronnen & Scores"):
                    for cite in msg.citations:
                        st.caption(f"[{cite['idx']}] {cite['source']} p.{cite['page']} (Score: {cite['score']:.3f})")
                        st.text(cite['text'][:200] + "...")

    # Input & Streaming
    if prompt := st.chat_input("Stel je vraag over het document..."):
        user_msg = ChatMessage(role="user", content=prompt)
        state.messages.append(user_msg)
        with st.chat_message("user"): 
            st.markdown(prompt)

        # 2. Retrieval via de asynchrone brug
        with st.spinner("🔍 Zoeken in kennisbank..."):
            results = run_async_task(rag.retrieve(prompt, k=state.retrieval_config["k"], rerank=state.retrieval_config["rerank"]))
        
        if not results:
            with st.chat_message("assistant"): 
                st.warning("Geen relevante informatie gevonden in het document.")
            return

        # 3. Generation (Streaming via de synchrone generator wrapper)
        citations = [{"idx": i+1, "source": r.metadata.get("source"), "page": r.metadata.get("page"), "score": r.rerank_score or r.vector_score, "text": r.text} for i, r in enumerate(results)]
        
        with st.chat_message("assistant"):
            # We roepen jouw asynchrone generate_answer aan en streamen de tokens real-life!
            full_response = st.write_stream(sync_generator_wrapper(rag.generate_answer(prompt, results)))
            
            # 4. Save Assistant Msg
            asst_msg = ChatMessage(role="assistant", content=full_response, citations=citations)
            state.messages.append(asst_msg)
            state.persist()

chat_interface()
