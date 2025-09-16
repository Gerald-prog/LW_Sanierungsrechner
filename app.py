import streamlit as st
import streamlit.components.v1 as components
import datetime

# -------------------------------------------------
#   Layout & Styles (wie gehabt)
# -------------------------------------------------
st.set_page_config(page_title="LW_Sanierungsrechner", page_icon="📊", layout="centered")

st.markdown(
    """
    <style>
        .stApp {background-color:#2c3e50;color:#ffb90f;}
        h1,h2,h3,h4,h5,h6,p,label,.markdown-text-container {color:#ffb90f !important;}
        .stTextInput > div > input {background-color:#ecf0.1f1;color:#2c3e50;font-weight:bold;}
        .stButton > button {background-color:#34495e;color:white;font-weight:bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
#   Konstanten & Hilfsfunktionen
# -------------------------------------------------
VERS_DEFAULT = 3.0


def parse_float(value: str):
    try:
        return float(value.replace(",", "."))
    except:
        return None


def berechnen(abgerechnet, mengeneinheit, versichert):
    if abgerechnet and mengeneinheit and versichert:
        return (versichert / abgerechnet) * mengeneinheit
    return None


# -------------------------------------------------
#   UI – Eingaben
# -------------------------------------------------
st.markdown("## 📊 Reparaturanteil Rechner")

vers_input = st.text_input("Versichert (Standard = 3 lfm.):", value=str(VERS_DEFAULT))
abgerechnet_input = st.text_input("Abgerechnet:")
mengeneinheit_input = st.text_input("Mengeneinheit:")

vers = parse_float(vers_input)
abgerechnet = parse_float(abgerechnet_input)
mengeneinheit = parse_float(mengeneinheit_input)

# -------------------------------------------------
#   (Berechnung)
# -------------------------------------------------
ergebnis = berechnen(abgerechnet, mengeneinheit, vers)

# -------------------------------------------------
#   Ausgabe + Kopier‑Buttons
# -------------------------------------------------
if ergebnis is not None:
    st.markdown("### Reparaturanteil:")

    # Dezimalwert
    st.text_input("Ergebnis", value=f"{ergebnis:.3f}", key="ergebnisfeld")

    # Gerundeter Integer
    gerundet = round(ergebnis)
    st.text_input("Gerundet (Integer)", value=str(gerundet), key="gerundetfeld")

    # ---- Kopier‑Button für Dezimalwert ----
    if st.button("📋 Kopieren (Dezimal)"):
        st.copy_to_clipboard(f"{ergebnis:.3f}")
        st.success("✔ Ergebnis wurde in die Zwischenablage kopiert.")

    # ---- Kopier‑Button für Integer‑Wert ----
    if st.button("📋 Kopieren (Integer)"):
        st.copy_to_clipboard(str(gerundet))
        st.success("✔ Integer‑Wert wurde in die Zwischenablage kopiert.")
else:
    st.markdown("📝 Bitte gültige Werte eingeben.")

# -------------------------------------------------
jahr = datetime.datetime.now().year
st.markdown(
    f"<hr><center style='color:#aaaaaa;'>© {jahr} | Gerald Günther</center>",
    unsafe_allow_html=True,
)
