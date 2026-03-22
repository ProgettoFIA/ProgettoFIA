import os
from dotenv import load_dotenv
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

load_dotenv()

st.set_page_config(page_title="ERUPLAN FIA - Dashboard", layout="wide")

col1, col2 = st.columns([1, 6.25])
with col1:
    st.markdown('<div class="logo-img">', unsafe_allow_html=True)
    st.image("eruplanlogo.png")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.title("ERUPLAN - Piano di Evacuazione Intelligente")
    st.markdown("Confronto algoritmi di ricerca per l'assegnazione dei rifugi sicuri.")

    st.divider()

API_URL = os.getenv(
    "API_URL",
    "https://eruplan-fia-api-a4c6dkd0hvetgse9.italynorth-01.azurewebsites.net/calcola-percorso"
)

if "dati_api" not in st.session_state:
    st.session_state.dati_api = None
    st.session_state.payload_usato = None
if "storico" not in st.session_state:
    st.session_state.storico = []

with st.sidebar:
    st.header("Parametri di Ricerca")
    algoritmo = st.selectbox("Scegli l'algoritmo", ["A*", "Greedy", "Costo Uniforme"])
    
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
    calcola_btn = st.button("Calcola Percorso Ottimale", type="primary", use_container_width=True)

if calcola_btn:
    st.session_state.dati_api = None 
    st.session_state.payload_usato = None
    
    with st.spinner(f"Calcolo in corso con {algoritmo}..."):
        payload = {
            "famiglia": {
                "nome": "Fam. Esposito (Portici)",
                "lat": 40.8160,
                "lon": 14.3400,
                "in_auto": True if mezzo == "In Auto" else False,
                "con_fragili": fragili
            },
            "rifugi": [
                {"nome": "HUB Monterusciello (Pozzuoli)", "lat": 40.8650, "lon": 14.0630},
                {"nome": "Porto Turistico (Bacoli)", "lat": 40.7950, "lon": 14.0800},
                {"nome": "Stadio Romeo Menti (Castellammare)", "lat": 40.7050, "lon": 14.4850},
                {"nome": "Campo Sportivo (Sorrento)", "lat": 40.6280, "lon": 14.3820}
            ],
            "algoritmo": "CU" if algoritmo == "Costo Uniforme" else algoritmo,
            "euristica": euristica_scelta.lower()
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code != 200:
                st.error(f"Errore dal server (Codice {response.status_code})")
                st.code(response.text)
                st.stop()

            data = response.json()
            
            if data.get("status") == "success":
                st.session_state.dati_api = data
                st.session_state.payload_usato = payload
                
                distanza_km = data['tempo_stimato_minuti'] / 2
                
                nome_algo = payload["algoritmo"]
                if nome_algo != "CU":
                    nome_algo += f" ({payload['euristica'][:3].upper()})"
                    
                st.session_state.storico.append({
                    "Algoritmo": nome_algo,
                    "Rifugio": data["rifugio_assegnato"].split(" ")[0],
                    "Distanza": f"{distanza_km:.1f} km",
                    "Tempo": f"{data['tempo_stimato_minuti']} min",
                    "Nodi": data["nodi_esplorati"],
                    "Tempo AI": f"{data['tempo_esecuzione_ai_sec']:.4f} s"
                })
                
            else:
                st.error("Errore dall'API: " + data.get("message", "Sconosciuto"))
                
        except requests.exceptions.ConnectionError:
            st.error("Impossibile connettersi all'API. Assicurati che il server FastAPI locale sia acceso (uvicorn api.server:app)!")

if st.session_state.dati_api:
    data = st.session_state.dati_api
    payload = st.session_state.payload_usato
    
    st.success(f"Percorso trovato verso: **{data['rifugio_assegnato']}**")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Tempo di Viaggio", f"{data['tempo_stimato_minuti']} min")
    col2.metric("Nodi Esplorati", f"{data['nodi_esplorati']:,}".replace(",", "."))
    col3.metric("Tempo AI (sec)", f"{data['tempo_esecuzione_ai_sec']} s")

    st.markdown("---")
    
    col_mappa, col_storico = st.columns([6, 3])
    vesuvio_coords = [40.8213963, 14.4261967]
    
    with col_mappa:
        st.subheader("🗺️ Mappa del Percorso")
        m = folium.Map(location=[payload["famiglia"]["lat"], payload["famiglia"]["lon"]], zoom_start=11)
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

        folium.Circle(
            location=vesuvio_coords,
            radius=4500,
            color='black',
            fill=True,
            fill_color='black',
            fill_opacity=0.5,
            weight=1,
        ).add_to(m)

        folium.Marker(
        vesuvio_coords, 
        popup="Cratere Vesuvio", 
        icon=folium.Icon(color='black', icon='')
        ).add_to(m)

        colore_linea = "blue" if payload["algoritmo"] == "A*" else ("red" if payload["algoritmo"] == "CU" else "orange")
        folium.PolyLine(
            coords,
            color=colore_linea,
            weight=5,
            opacity=0.8
        ).add_to(m)

        st_folium(m, width=800, height=465, returned_objects=[])

    with col_storico:
        st.subheader("Storico Test")
        
        if st.session_state.storico:
            storico_inverso = list(reversed(st.session_state.storico))
            st.dataframe(storico_inverso, use_container_width=True, hide_index=True)
            
            if st.button("🗑️ Svuota Storico", use_container_width=True):
                st.session_state.storico = []
                st.rerun()
        else:
            st.info("Esegui un calcolo per popolare lo storico.")
