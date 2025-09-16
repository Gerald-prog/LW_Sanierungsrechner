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
        .stTextInput > div > input {background-color:#ecf0f1;color:#2c3e50;font-weight:bold;}
        .stButton > button {background-color:#34495e;color:white;font-weight:bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
#   Konstanten & Hilfsfunktionen
# -------------------------------------------------
VERS_DEFAULT = 3.0


def parse_float(v: str):
    try:
        return float(v.replace(",", "."))
    except:
        return None


def berechnen(ab, me, ve):
    if ab and me and ve:
        return (ve / ab) * me
    return None


# -------------------------------------------------
#   UI – Eingaben
# -------------------------------------------------
st.markdown("## 📊 Reparaturanteil Rechner")

vers = parse_float(
    st.text_input("Versichert (Standard = 3 lfm.):", value=str(VERS_DEFAULT))
)
abgerechnet = parse_float(st.text_input("Abgerechnet:"))
mengeneinheit = parse_float(st.text_input("Mengeneinheit:"))

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
        js = f"""
        <script>
        const ta = document.createElement('textarea');
        ta.value = "{ergebnis:.3f}";
        document.body.appendChild(ta);
        ta.select();
        try {{
            document.execCommand('copy');
            alert('✔ Ergebnis wurde kopiert.');
        }} catch (e) {{
            alert('⚠️ Kopieren fehlgeschlagen: ' + e);
        }}
        document.body.removeChild(ta);
        </script>
        """
        components.html(js, height=0)

    # ---- Kopier‑Button für Integer‑Wert ----
    if st.button("📋 Kopieren (Integer)"):
        js = f"""
        <script>
        const ta = document.createElement('textarea');
        ta.value = "{gerundet}";
        document.body.appendChild(ta);
        ta.select();
        try {{
            document.execCommand('copy');
            alert('✔ Integer‑Wert wurde kopiert.');
        }} catch (e) {{
            alert('⚠️ Kopieren fehlgeschlagen: ' + e);
        }}
        document.body.removeChild(ta);
        </script>
        """
        components.html(js, height=0)

else:
    st.markdown("📝 Bitte gültige Werte eingeben.")

# -------------------------------------------------
#   Footer
# -------------------------------------------------
jahr = datetime.datetime.now().year
st.markdown(
    f"<hr><center style='color:#aaaaaa;'>© {jahr} | Gerald Günther</center>",
    unsafe_allow_html=True,
)
