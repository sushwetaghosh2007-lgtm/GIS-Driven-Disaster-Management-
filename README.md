# GIS-Driven-Disaster-Management-
Pan-India Intelligent GIS Relocation Decision Support System (DSS) powered by FastAPI, Leaflet, and ISRO Bhuvan satellite/thematic layers.


# 🔴 RedZone-AI: Pan-India Intelligent GIS Relocation DSS

**RedZone-AI** is an advanced, full-stack geospatial Decision Support System (DSS) designed for State Disaster Management Authorities (SDMA). It calculates Relocation Priority Index (RPI) scores for vulnerable habitations across India, estimates rapid aerial and ground evacuation times, leverages **ISRO Bhuvan WMS/OGC services**, and simulates the impact of extreme weather events (such as cloudbursts or flash floods).

---

## 🚀 Key Features

* **🛰️ ISRO Bhuvan Integration:** Direct rendering of NRSC/ISRO Bhuvan tile services (`india3` satellite basemap and `LULC` land cover thematic overlays).
* **⚡ Live Weather Simulation:** Interactive simulation engine to evaluate risk escalation under extreme precipitation scenarios (e.g., up to 300 mm rainfall).
* **📊 AHP Suitability Breakdown:** Analytical Hierarchy Process (AHP) evaluation metrics for safe relocation sites (Land Availability, Infrastructure Access, Livelihood Potential, and Legal/Env Clearance).
* **🚁 Evacuation Route & Time Modeling:** Haversine direct air distance calculations alongside mountain-adjusted road transit estimations for both choppers and evacuation transport.
* **📄 SDMA Report Ready:** Print/Export-optimized CSS layout tailored for official disaster management reporting.

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Pydantic, Uvicorn, CORS Middleware
* **Frontend:** HTML5, CSS3, JavaScript (ES6+), Leaflet.js
* **GIS & Tile Providers:** ISRO Bhuvan (NRSC), CartoDB, OpenStreetMap, RainViewer Radar

---

## 📁 Project Structure

```text
├── backend.py        # FastAPI server, data models, and RPI calculation logic
├── index.html        # Interactive single-page frontend dashboard (Leaflet + UI)
└── README.md         # Project documentation
