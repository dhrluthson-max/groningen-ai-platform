# src/gemeentecore/ui/components.py
import streamlit as st

def render_sidebar():
    """Renders the sovereign enterprise sidebar."""
    with st.sidebar:
        st.markdown("### 🏛️ Gemeente AI Core")
        st.caption("Quantum Guard & Modulaire Architectuur")
        st.markdown("---")
        st.markdown("🛡️ **Quantum Cyber Status:**")
        st.markdown("- *Airflow Shield: On-Premise*")
        st.markdown("- *Lattice Crypto: Gecertificeerd (LWE)*")
        st.markdown("- *Homomorphic Logic: Actief (FHE)*")

def render_metric_card(title: str, value: str, subtext: str, icon: str):
    """Renders a beautiful, cyber-style metric card based on your telemetry design."""
    st.markdown(f"""
    <div style="
        background-color: #030712;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        min-height: 140px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    ">
        <div style="
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #06b6d4;
            font-size: 14px;
        ">{icon}</div>
        <p style="
            color: #9ca3af;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 0;
        ">{title}</p>
        <h2 style="
            color: #ffffff;
            font-size: 28px;
            font-weight: 600;
            margin-top: 15px;
            margin-bottom: 5px;
            font-family: monospace;
        ">{value}</h2>
        <p style="
            color: #6b7280;
            font-size: 12px;
            margin: 0;
        ">{subtext}</p>
    </div>
    """, unsafe_allow_html=True)
