import streamlit as st
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
    st.text_input("Ergebnis", value=f"{ergebnis:.3f}", key="ergebnisfeld")

    # Kopieren per JavaScript
    st.markdown(
        """
        <script>
        function copyToClipboard(text) {
          navigator.clipboard.writeText(text).then(function() {
            alert('✔ Ergebnis wurde in die Zwischenablage kopiert.');
          }, function(err) {
            alert('⚠️ Kopieren fehlgeschlagen: ' + err);
          });
        }
        </script>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <button onclick="copyToClipboard('{ergebnis:.3f}')" style="
            background-color: #34495e;
            color: white;
            font-weight: bold;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        ">📋 Kopieren</button>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown("📝 Bitte gültige Werte eingeben.")

# Footer
jahr = datetime.datetime.now().year
st.markdown(
    f"<hr><center style='color:#aaaaaa;'>© {jahr} | Gerald Günther</center>",
    unsafe_allow_html=True,
)
