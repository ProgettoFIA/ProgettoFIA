# Eruplan FIA

<p align="center">
  <img src="eruplanlogo.png" alt="Eruplan Logo" height="400"/>
</p>




## 👥 Authors

- **Camilla Piceda** - [CamillaPiceda](https://github.com/camilla554) as Developer.
- **Salvatore Mastellone** - [SalvatoreMastellone](https://github.com/Salvatore-Mastellone) as Developer.
- **Christian Comiato** - [ChristianComiato](https://github.com/christiancomiato) as Developer.

We are students at the **University of Salerno (UNISA)**. This module was developed for the *Fondamenti di Intelligenza Artificiale* (FIA) exam.



## 💡 What is it?

**Eruplan FIA** is the Artificial Intelligence extension of the Eruplan ecosystem. It provides a dynamic, intelligent core capable of calculating optimal emergency evacuation routes for families during a simulated eruption of Vesuvius.

Instead of relying on static plans, this module:
- Downloads real map data from **OpenStreetMap**
- Dynamically disables road networks inside the volcanic **Black Zone** (4.5 km radius from the crater)
- Computes the fastest escape routes to designated **Safe Hubs**



## 🧠 Core Features & Benchmarking

The system acts as a benchmark tool to compare different pathfinding algorithms in a real-world crisis scenario:

- **Algorithms:** A\* (Optimal), Uniform Cost Search (Non-Informed), and Greedy Best-First Search
- **Heuristics:** Euclidean, Manhattan, and Chebyshev distances
- **Interactive Dashboard:** A visual interface to test specific families (accounting for vehicles and vulnerable members) and compare algorithm execution times, explored nodes, and path optimality side-by-side



## 🚀 How to Try It

The project consists of a **Python backend** (FastAPI) and a **frontend dashboard** (Streamlit).

### Prerequisites

- Python 3.11+
- `pip` (Python package installer)

### Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ProgettoFIA/ProgettoFIA.git
   cd ProgettoFIA
   ```

2. **Configure the Virtual Environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend (FastAPI):**
   Open a terminal and start the API server. On the first run, this will also download the map (`mappa_napoli.pkl`).
   ```bash
   uvicorn api.server:app --reload
   ```

5. **Run the Frontend (Streamlit Dashboard):**
   Open a **second terminal**, ensure the virtual environment is active, then run:
   ```bash
   streamlit run ui/dashboard.py
   ```
   The dashboard will automatically open in your browser at [http://localhost:8501](http://localhost:8501).

   >**_NOTE:_ For benchmarks and visual graphs run the scripts in /scripts:**
   >```bash
   >python main.py
   >python benchmark_plots.py
   >```


## ☁️ Deployment

The backend API is configured for continuous deployment on **Azure Web Apps** via a GitHub Actions workflow.
Configuration file: `.github/workflows/deploy-azure.yml`



## 🛠️ Built With

| Technology | Purpose |
|------------|---------|
| [Python](https://www.python.org/) | Core language |
| [FastAPI](https://fastapi.tiangolo.com/) | High-performance backend framework |
| [Streamlit](https://streamlit.io/) | Frontend web dashboard |
| [NetworkX](https://networkx.org/) | Graph theory and complex network structures |
| [Folium](https://python-visualization.github.io/folium/) & Leaflet.js | Interactive map visualization |
| [OSMnx](https://osmnx.readthedocs.io/) / Overpass API | Real-world street network data extraction |
| [Pydantic](https://docs.pydantic.dev/) | Data validation and settings management |



## 🔗 Related Resources

- [Eruplan Server](https://github.com/T-R-M-V-spin-off/eruplanserver) - The official backend system
- [Eruplan Web Client](https://github.com/T-R-M-V-spin-off/eruplanwebclient) - The official web frontend
- [Eruplan Mobile Client](https://github.com/T-R-M-V-spin-off/eruplanmobileclient) - The official mobile app
