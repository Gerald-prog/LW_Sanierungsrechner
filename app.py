import streamlit as st
import streamlit.components.v1 as components
import datetime
import math


import streamlit as st
import streamlit.components.v1 as components
import datetime
import math


# Debug-Hilfsfunktion
def debug_print(label, value, value_type=None):
    st.sidebar.write(f"🔍 {label}:")
    st.sidebar.write(f"Wert: {value}")
    if value_type:
        st.sidebar.write(f"Typ: {type(value)}")
    st.sidebar.write("---")


# -------------------------------------------------
# Layout & Styles
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


def reparatur_faktor(ab, ve):
    if ab and ve:
        return ve / ab
    return None


def stk_setzen(wert, ergebnis):

    # 1. Bedingung: Wenn der Wert kleiner als 1 ist, setze ihn auf 1
    if wert < 1:
        wert = 1

    # 2. Bedingung: Wenn der Wert größer als
    # floor(ergebnis) + (VERS_DEFAULT/ abgerechnet) ist,
    # dann verwende ceil, sonst floor
    floor_ergebnis = math.floor(ergebnis)
    if wert > (floor_ergebnis + 0.2):
        return math.ceil(wert)
    else:
        return math.floor(wert)


# Pfad zur Textdatei
text_file_path = "lw_text.txt"


def lese_text_datei(file_path):
    with open(file_path, "r") as file:
        return file.read()


# -------------------------------------------------
# UI – Eingaben
# -------------------------------------------------
st.markdown("## 📊 Reparaturanteil Rechner")

col1, col2 = st.columns([1, 2])

with col1:
    # Debug-Ausgabe für Versichert
    debug_print("Versichert (Eingabe)", str(VERS_DEFAULT))

    # Eingabefelder mit Session State (dynamische Berechnung)
    vers = parse_float(
        st.text_input("Versichert (Standard = 3 lfm.):", value=str(VERS_DEFAULT))
    )
    # Debug-Ausgabe für Abgerechnet
    # debug_print("Abgerechnet (Session State)", st.text_input("Abgerechnet:", value=""))

    abgerechnet = parse_float(st.text_input("Abgerechnet:", value=""))

    debug_print("Abgerechnet (Nach parse_float)", abgerechnet)

    # Debug-Ausgabe für Mengeneinheit
    # debug_print("Mengeneinheit (Session State)", st.session_state.mengeneinheit_input)

    mengeneinheit = parse_float(st.text_input("Mengeneinheit:", value=""))

    debug_print("Mengeneinheit (Nach parse_float)", mengeneinheit)

    # Debug-Ausgabe für Berechnung
    debug_print(
        "Berechnungs-Parameter",
        {
            "Abgerechnet": abgerechnet,
            "Mengeneinheit": mengeneinheit,
            "Versichert": vers,
        },
    )

    # Berechnung des Ergebnisses
    ergebnis = (
        round(berechnen(abgerechnet, mengeneinheit, vers), 3)
        if all([abgerechnet, mengeneinheit, vers])
        else None
    )

    debug_print("Ergebnis", ergebnis)


with col2:

    debug_print(
        "Faktor-Berechnung (Parameter)",
        {"Abgerechnet": abgerechnet, "Versichert": vers},
    )

    faktor = (
        round(reparatur_faktor(abgerechnet, vers), 3)
        if all([abgerechnet, vers])
        else None
    )

    debug_print("Faktor", faktor)

    st.markdown(
        f"**Reparatur-Faktor (für Eintrag im Bemerkungstext):**   {faktor:.3f}"
        if faktor is not None
        else ""
    )

# -------------------------------------------------
# Ausgabe & Kopier‑Buttons
# -------------------------------------------------
if ergebnis is not None:

    st.markdown("### Reparaturanteil:")

    st.markdown(f"**Ergebnis:** {ergebnis:.3f}")

    # Sicherheitsprüfung das ergebnis nicht None ist
    gerundet = stk_setzen(ergebnis, ergebnis) if ergebnis is not None else None

    if gerundet is not None:
        st.markdown(f"**Menge in Stück:** {gerundet}")
    else:
        pass

    debug_print("Menge in Stueck", gerundet)


# -------------------------------------------------
# Ausgabe & Kopier‑Buttons
# -------------------------------------------------
if ergebnis is not None:
    # ---------- Button Dezimal ----------
    if st.button("📋 Kopieren (Dezimal)"):
        st.session_state["copy_text"] = f"{ergebnis:.3f}"

    # ---------- Button Integer ----------
    if st.button("📋 Kopieren (Stück)"):
        st.session_state["copy_text"] = str(gerundet)

    with col2:
        if st.button("📋 Kopieren"):
            st.session_state["copy_text"] = str(faktor)

if ergebnis is not None:

    # Lesen der Textdatei
    text = lese_text_datei(text_file_path)

    # Ersetzen der Platzhalter durch die aktuellen Werte
    text = text.replace("{vers}", str(vers))
    text = text.replace("{abgerechnet}", str(abgerechnet))
    text = text.replace("{faktor}", str(f"{faktor:.3f}" if faktor is not None else ""))

    # Ausgabe des formatierten Textes
    with col2:
        st.markdown("### Text mit Werten:")
        st.text_area(
            "Text für Bearbeitungshinweise", value=text, height=20, key="bemerkungsfeld"
        )

    # ---------- JavaScript‑Snippet ----------
    # Wird nur gerendert, wenn ein Kopier‑Flag existiert
    if "copy_text" in st.session_state:
        text = st.session_state["copy_text"]
        # Flag wieder entfernen, damit ein neuer Klick erneut funktioniert
        del st.session_state["copy_text"]

        js = f"""
        <script>
        // 1️⃣ Fokus sicherstellen
        if (document.hasFocus && !document.hasFocus()) {{
            window.focus();
        }}

        // 2️⃣ Kopier‑Funktion (moderne API + Fallback)
        function copyNow(txt) {{
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(txt)
                    .then(() => alert('✔ ' + txt + ' kopiert.'))
                    .catch(err => alert('⚠️ Kopieren fehlgeschlagen: ' + err));
            }} else {{
                const ta = document.createElement('textarea');
                ta.value = txt;
                document.body.appendChild(ta);
                ta.select();
                try {{
                    document.execCommand('copy');
                    alert('✔ ' + txt + ' kopiert.');
                }} catch (e) {{
                    alert('⚠️ Kopieren fehlgeschlagen: ' + e);
                }}
                document.body.removeChild(ta);
            }}
        }}

        // 3️⃣ sofort ausführen
        copyNow("{text}");
        </script>
        """
        # height=0 → kein sichtbarer Platz
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
