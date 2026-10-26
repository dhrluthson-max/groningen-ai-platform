# src/gemeentecore/ui/pages/3_Admin.py
import streamlit as st

st.title("🛡️ AI-Governance & Compliance Center")
st.caption("Toetsing van AI-toepassingen aan de Baseline Informatiebeveiliging Overheid (BIO) en ethische kaders.")

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📊 Datamodel Architectuur Planner")
    systeem = st.selectbox("Selecteer registrasiesysteem:", ["BRP (Personen)", "BAG (Adressen)", "Zaaksysteem"])
    st.info(f"Geselecteerd model: {systeem}. Embedding mapping verloopt lokaal via multilingual-e5-large.")
    st.checkbox("Pseudonimisering & Maskering van BSN-nummers actief", value=True)
    st.checkbox("100% On-Premise (Geen data naar externe API's)", value=True)

with col_b:
    st.subheader("💡 Advieswijzer AI-Limieten")
    casus = st.selectbox("Toets een gemeentelijk AI-scenario:", [
        "Automatisch beoordelen van bijstandsaanvragen (Fraudedetectie)",
        "Automatisch samenvatten van raadsvergaderingen"
    ])
    st.write("---")
    if "Fraudedetectie" in casus:
        st.error("🔴 **Advies: Strikt Verboden.** AI mag nooit zelfstandig besluiten nemen over burgers wegens het risico op bias en uitsluiting (AVG/BIO restrictie).")
    else:
        st.success("🟢 **Advies: Veilig toepasbaar.** Betreft openbare raadsstukken. Versnelt de workflow van beleidsmakers zonder privacyrisico's.")
