# src/gemeentecore/models/state.py
from pydantic import BaseModel, Field, PrivateAttr
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
import streamlit as st
import uuid

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    citations: List[Dict[str, Any]] = Field(default_factory=list) # {doc_id, page, score, text}
    metadata: Dict[str, Any] = Field(default_factory=dict) # tokens, latency, model

class DocumentMetadata(BaseModel):
    file_name: str
    file_hash: str
    upload_time: datetime
    num_pages: int
    num_chunks: int
    status: Literal["processing", "indexed", "failed"] = "processing"

class SessionState(BaseModel):
    # UI State
    active_module: str = "dashboard"
    sidebar_collapsed: bool = False
    
    # RAG State
    current_doc: Optional[DocumentMetadata] = None
    documents: Dict[str, DocumentMetadata] = Field(default_factory=dict)
    messages: List[ChatMessage] = Field(default_factory=list)
    retrieval_config: Dict[str, Any] = Field(default_factory=lambda: {"k": 5, "rerank": True})
    
    # System State
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    _initialized: bool = PrivateAttr(default=False)

    # --- Singleton Pattern voor Streamlit ---
    @classmethod
    def get(cls) -> "SessionState":
        if "typed_state" not in st.session_state:
            st.session_state.typed_state = cls()
            st.session_state.typed_state._initialized = True
        return st.session_state.typed_state

    def persist(self):
        """Forceer sync naar Streamlit (meestal niet nodig, Pydantic mutatie werkt direct)."""
        st.session_state.typed_state = self

    def clear_chat(self):
        self.messages = []
        self.persist()
