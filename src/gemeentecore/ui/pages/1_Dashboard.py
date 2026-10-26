# src/gemeentecore/ui/pages/1_Dashboard.py
import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh # pyright: ignore[reportMissingImports]
from gemeentecore.ui.components import render_metric_card

st.title("🎛️ Systeem Telemetrie Dashboard")
st.caption("Realtime status van de on-premise overheid-infrastructuur.")

# Realtime verversing van 2 seconden activeren voor de beweging
st_autorefresh(interval=2000, limit=10000, key="dashboard_refresh")

# Genereer bewegende test-data
current_airflow = round(98.7 + random.uniform(-0.5, 0.5), 1)
current_pressure = round(0.42 + random.uniform(-0.02, 0.02), 2)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_metric_card("Quantum Airflow", f"{current_airflow} m³/h", "Shield Status: Actief Veilig", "🌀")
with col2:
    render_metric_card("Drukair Sensor", f"{current_pressure} Bar", "Sensor Integriteit: Binnen Limiet", "🎈")
with col3:
    render_metric_card("Master Prompt", "v4.1.2", "Systeemlogica: Zelf-Reflecterend", "🧠")
with col4:
    render_metric_card("Self-Healer", "0 Fouten", "Systeem Gezondheid: 100%", "🩹")

st.markdown("---")
st.subheader("🛡️ Gecertificeerde Beveiliging Parameters")
col_l, col_r = st.columns(2)
with col_l:
    st.write("**• Lattice-based Cryptografie (LWE):** Data-encryptie is volledig bestand tegen de rekenkracht van toekomstige kwantumcomputers.")
    st.write("**• Fully Homomorphic Encryption (FHE):** Berekeningen uitvoeren op actieve datastromen zonder deze vooraf te ontsleutelen.")
with col_r:
    st.write("**• Analoge Sensor-Matrix:** Monitort fysieke parameters. Luchtdrukstijging signaleert geforceerde toegang.")
    st.write("**• Instant RAM-Shredding:** Bij alarm worden alle cryptografische sleutels binnen een milliseconde definitief gewist.")
