# src/main.py
import os
import sys

# --- 1. BOOTSTRAP ENVIRONMENT PATHS (Dit MOET bovenaan staan) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

paths_to_inject = [project_root, current_dir, os.path.join(project_root, "src")]
for p in paths_to_inject:
    if p not in sys.path:
        sys.path.insert(0, p)

# --- 2. CORE IMPORTS ---
import streamlit as st
from gemeentecore.config import settings
from gemeentecore.logging_config import setup_logging
from gemeentecore.ui.styles import inject_global_css

# --- 3. PAGE CONFIG (Eerste harde Streamlit-commando na imports) ---
st.set_page_config(
    page_title="Gemeente AI Control Center",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/jouw-org/gemeente-ai-core',
        'Report a bug': 'https://github.com/jouw-org/gemeente-ai-core/issues',
        'About': "Sovereign AI Platform v3.0"
    }
)

# --- 4. INITIALIZE BOOTSTRAP SERVICES ---
setup_logging(settings.LOG_LEVEL, settings.SERVICE_NAME)
inject_global_css()

# --- 5. NATIVE MULTI-PAGE NAVIGATION (Unieke Master Prompt Fix) ---
dashboard_path = os.path.join(current_dir, "gemeentecore", "ui", "pages", "1_Dashboard.py")
rag_path = os.path.join(current_dir, "gemeentecore", "ui", "pages", "2_RAG.py")
admin_path = os.path.join(current_dir, "gemeentecore", "ui", "pages", "3_Admin.py")

pg = st.navigation([
    st.Page(dashboard_path, title="Dashboard", icon="🎛️"),
    st.Page(rag_path, title="RAG Engine", icon="🧠"),
    st.Page(admin_path, title="Governance", icon="🛡️"),
])

# --- 6. RUN ENGINE ---
pg.run()
