import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="ERUPLAN FIA - Dashboard", layout="wide")
st.title("ERUPLAN - Piano di Evacuazione Intelligente")
st.markdown("Confronto algoritmi di ricerca per l'assegnazione dei rifugi sicuri.")

API_URL = "https://eruplan-fia-api-a4c6dkd0hvetgse9.italynorth-01.azurewebsites.net/calcola-percorso"

with st.sidebar:
    st.header("Parametri di Ricerca")
    algoritmo = st.selectbox("Scegli l'algoritmo", ["A*", "Greedy", "Costo Uniforme"])
    
    # NUOVO BLOCCO EURISTICA
    # Mostriamo il selettore SOLO per gli algoritmi informati
    if algoritmo in ["A*", "Greedy"]:
        euristica_scelta = st.selectbox(
            "Scegli l'euristica", 
            ["Euclidea", "Manhattan", "Chebyshev"],
            help="Determina come l'algoritmo stima la distanza rimanente verso il rifugio."
        )
    else:
        euristica_scelta = "euclidea" 
        st.info("Il Costo Uniforme non usa euristiche (Ricerca Non Informata).")
    mezzo = st.radio("Mezzo di trasporto", ["A Piedi", "In Auto"])
    fragili = st.checkbox("Presenza di soggetti fragili")
    
    st.markdown("---")
    calcola_btn = st.button("Calcola Percorso Ottimale", type="primary")

if "dati_api" not in st.session_state:
    st.session_state.dati_api = None
    st.session_state.payload_usato = None

if calcola_btn:
    with st.spinner(f"Calcolo in corso con {algoritmo}..."):
        payload = {
            "famiglia": {
                "nome": "Famiglia Esposito",
                "lat": 40.8431,
                "lon": 14.2483,
                "in_auto": True if mezzo == "In Auto" else False,
                "con_fragili": fragili
            },
            "rifugi": [
                {"nome": "Piazza del Plebiscito", "lat": 40.8359, "lon": 14.2487},
                {"nome": "Stadio Diego Armando Maradona", "lat": 40.8279, "lon": 14.1930},
                {"nome": "Bosco di Capodimonte", "lat": 40.8672, "lon": 14.2504}
            ],
            "algoritmo": algoritmo,
            "euristica": euristica_scelta.lower()
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code != 200:
                st.error(f"Errore dal server Azure (Codice {response.status_code})")
                st.code(response.text)
                st.stop() # Fermo tutto per non far crashare Streamlit

            data = response.json()
            
            if data.get("status") == "success":
                st.session_state.dati_api = data
                st.session_state.payload_usato = payload
            else:
                st.error("Errore dall'API: " + data.get("message", "Sconosciuto"))
                
        except requests.exceptions.ConnectionError:
            st.error("Impossibile connettersi all'API. Assicurati che il server FastAPI sia acceso!")

# DISEGNO INTERFACCIA
if st.session_state.dati_api:
    data = st.session_state.dati_api
    payload = st.session_state.payload_usato
    
    st.success(f"Percorso trovato verso: **{data['rifugio_assegnato']}**")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Tempo di Viaggio", f"{data['tempo_stimato_minuti']} min")
    col2.metric("Nodi Esplorati", f"{data['nodi_esplorati']:,}".replace(",", "."))
    col3.metric("Tempo AI (sec)", f"{data['tempo_esecuzione_ai_sec']} s")

    st.subheader("🗺️ Mappa del Percorso")
    
    m = folium.Map(location=[payload["famiglia"]["lat"], payload["famiglia"]["lon"]], zoom_start=13)
    
    folium.Marker(
        [payload["famiglia"]["lat"], payload["famiglia"]["lon"]],
        popup="Partenza",
        icon=folium.Icon(color="red", icon="home")
    ).add_to(m)

    coords = [(punto["lat"], punto["lon"]) for punto in data["percorso_coordinate"]]
    
    folium.Marker(
        coords[-1],
        popup=data['rifugio_assegnato'],
        icon=folium.Icon(color="green", icon="shield")
    ).add_to(m)

    folium.PolyLine(
        coords,
        color="blue" if payload["algoritmo"] == "A*" else ("red" if payload["algoritmo"] == "Dijkstra" else "orange"),
        weight=5,
        opacity=0.8
    ).add_to(m)

    # Per evitare che cliccando sulla mappa la pagina venga ricaricata
    st_folium(m, width=800, height=500, returned_objects=[])

else:
    st.info("Imposta i parametri a sinistra e clicca su 'Calcola Percorso Ottimale'")