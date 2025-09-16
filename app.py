import streamlit as st
import streamlit.components.v1 as components
import datetime

# -------------------------------------------------
# Layout & Styles (wie gehabt)
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
# Konstanten & Hilfsfunktionen
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
# UI – Eingaben
# -------------------------------------------------
st.markdown("## 📊 Reparaturanteil Rechner")

vers = parse_float(
    st.text_input("Versichert (Standard = 3 lfm.):", value=str(VERS_DEFAULT))
)
abgerechnet = parse_float(st.text_input("Abgerechnet:"))
mengeneinheit = parse_float(st.text_input("Mengeneinheit:"))

ergebnis = berechnen(abgerechnet, mengeneinheit, vers)

# -------------------------------------------------
# Ausgabe + Kopier‑Buttons
# -------------------------------------------------
if ergebnis is not None:
    st.markdown("### Reparaturanteil:")

    # Dezimalwert
    st.text_input("Ergebnis", value=f"{ergebnis:.3f}", key="ergebnisfeld")

    # Gerundeter Integer
    gerundet = round(ergebnis)
    st.text_input("Gerundet (Integer)", value=str(gerundet), key="gerundetfeld")

    # -------------------------------------------------
    # 1️⃣ Button für Dezimalwert
    # -------------------------------------------------
    dec_btn_id = "copy-dec-btn"
    st.markdown(
        f"""
        <button id="{dec_btn_id}"
                style="
                    background-color:#34495e;
                    color:white;
                    font-weight:bold;
                    border:none;
                    padding:8px 16px;
                    border-radius:4px;
                    cursor:pointer;
                ">
            📋 Kopieren (Dezimal)
        </button>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # 2️⃣ Button für Integer‑Wert
    # -------------------------------------------------
    int_btn_id = "copy-int-btn"
    st.markdown(
        f"""
        <button id="{int_btn_id}"
                style="
                    background-color:#34495e;
                    color:white;
                    font-weight:bold;
                    border:none;
                    padding:8px 16px;
                    border-radius:4px;
                    margin-left:8px;
                    cursor:pointer;
                ">
            📋 Kopieren (Integer)
        </button>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------
    # JavaScript‑Listener (einmalig einbinden)
    # -------------------------------------------------
    js = f"""
    <script>
    // Funktion, die den Text in die Zwischenablage schreibt
    function copyText(text) {{
        // Moderne API, fallback zu execCommand
        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(() => {{
                alert('✔ ' + text + ' kopiert.');
            }}).catch(err => {{
                alert('⚠️ Kopieren fehlgeschlagen: ' + err);
            }});
        }} else {{
            const ta = document.createElement('textarea');
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            try {{
                document.execCommand('copy');
                alert('✔ ' + text + ' kopiert.');
            }} catch (e) {{
                alert('⚠️ Kopieren fehlgeschlagen: ' + e);
            }}
            document.body.removeChild(ta);
        }}
    }}

    // Listener für den Dezimal‑Button
    document.getElementById('{dec_btn_id}').addEventListener('click', function() {{
        copyText("{ergebnis:.3f}");
    }});

    // Listener für den Integer‑Button
    document.getElementById('{int_btn_id}').addEventListener('click', function() {{
        copyText("{gerundet}");
    }});
    </script>
    """
    # Das HTML‑Fragment wird ohne sichtbaren Platz gerendert
    components.html(js, height=0)

else:
    st.markdown("📝 Bitte gültige Werte eingeben.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
jahr = datetime.datetime.now().year
st.markdown(
    f"<hr><center style='color:#aaaaaa;'>© {jahr} | Gerald Günther</center>",
    unsafe_allow_html=True,
)
