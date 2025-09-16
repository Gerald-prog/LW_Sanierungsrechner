import streamlit as st
import streamlit.components.v1 as components  # <- wichtig für streamlit
import datetime

# --- Konfiguration ---
st.set_page_config(page_title="LW_Sanierungsrechner", page_icon="📊", layout="centered")

# --- Farben und Styles ---
st.markdown(
    """
    <style>
        .stApp {
            background-color: #2c3e50;
            color: #ffb90f;
        }
        h1, h2, h3, h4, h5, h6, p, label, .markdown-text-container {
            color: #ffb90f !important;
        }
        .stTextInput > div > input {
            background-color: #ecf0f1;
            color: #2c3e50;
            font-weight: bold;
        }
        .stButton > button {
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Konstanten ---
VERS_DEFAULT = 3.0


# --- Hilfsfunktionen ---
def parse_float(value: str):
    try:
        return float(value.replace(",", "."))
    except:
        return None


def berechnen(abgerechnet, mengeneinheit, versichert):
    if abgerechnet is not None and mengeneinheit is not None and versichert is not None:
        return (versichert / abgerechnet) * mengeneinheit
    return None


# --- UI ---
st.markdown("## 📊 Reparaturanteil Rechner")

# Eingabefelder
vers_input = st.text_input("Versichert (Standard = 3lfm.):", value=str(VERS_DEFAULT))
abgerechnet_input = st.text_input("Abgerechnet:")
mengeneinheit_input = st.text_input("Mengeneinheit:")

# Umwandlung der Eingaben
vers = parse_float(vers_input)
abgerechnet = parse_float(abgerechnet_input)
mengeneinheit = parse_float(mengeneinheit_input)

# Berechnung
ergebnis = berechnen(abgerechnet, mengeneinheit, vers)

# Anzeige des Ergebnisses
if ergebnis is not None:
    st.markdown("### Reparaturanteil:")

    # Dezimalwert
    st.text_input("Ergebnis", value=f"{ergebnis:.3f}", key="ergebnisfeld")

    # Gerundeter Integer
    gerundet = round(ergebnis)

    # oder int(ergebnis) für Abrunden
    st.text_input("Gerundet (Integer)", value=str(gerundet), key="gerundetfeld")

    # -------------------------------------------------
    # 1️⃣ Kopier‑Button für den Dezimalwert
    # -------------------------------------------------
    if st.button("📋 Kopieren (Dezimal)"):
        # JavaScript‑Snippet, das den Text in die Zwischenablage schreibt
        js = f"""
        <script>
        navigator.clipboard.writeText("{ergebnis:.3f}")
            .then(() => alert("✔ Ergebnis wurde kopiert."))
            .catch(err => alert("⚠️ Kopieren fehlgeschlagen: " + err));
        </script>
        """
        components.html(js, height=0)  # rendert das Skript, führt es sofort aus

    # -------------------------------------------------
    # 2️⃣ Kopier‑Button für den Integer‑Wert
    # -------------------------------------------------
    if st.button("📋 Kopieren (Integer)"):
        js = f"""
        <script>
        navigator.clipboard.writeText("{gerundet}")
            .then(() => alert("✔ Integer‑Wert wurde kopiert."))
            .catch(err => alert("⚠️ Kopieren fehlgeschlagen: " + err));
        </script>
        """
        components.html(js, height=0)

else:
    st.markdown("📝 Bitte gültige Werte eingeben.")

# Footer
jahr = datetime.datetime.now().year
st.markdown(
    f"<hr><center style='color:#aaaaaa;'>© {jahr} | Gerald Günther</center>",
    unsafe_allow_html=True,
)
# Minimaler Kommentar hinzugefügt, um eine Änderung für Git zu erzwingen
