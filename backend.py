import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="RedZone-AI SDMA Backend API",
    description="Pan-India GIS Relocation & Hazard Assessment Backend with ISRO Bhuvan Integration",
    version="2.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Data Models
# ==========================================

class HabitationUpdate(BaseModel):
    hazard: Optional[float] = Field(None, ge=0, le=100)
    vulnerability: Optional[float] = Field(None, ge=0, le=100)
    history: Optional[float] = Field(None, ge=0, le=100)


class SimulationRequest(BaseModel):
    rainfall_mm: float = Field(..., ge=0, le=300)


# ==========================================
# ISRO Bhuvan Endpoint Configurations
# ==========================================

BHUVAN_CONFIG = {
    "wms_base_url": "https://bhuvan-vec1.nrsc.gov.in/bhuvan/gwc/service/wms",
    "layers": {
        "satellite": "india3",
        "hybrid": "bhuvan_hybrid",
        "thematic_landuse": "LULC:LULC_50K_0506"
    },
    "note": "Official NRSC/ISRO Bhuvan OGC Tile Service"
}


# ==========================================
# Pan-India Relocation Hubs & Habitations
# ==========================================

SITES_DB = [
    {
        "id": "SITE_1",
        "name": "Narkanda High Ridge Ground",
        "lat": 31.2580,
        "lng": 77.4580,
        "capacity": 350,
        "ccs": 88.5,
        "ahpBreakdown": {"landAvailability": 90, "infraAccess": 85, "livelihoodScore": 80, "legalClearance": 95},
    },
    {
        "id": "SITE_2",
        "name": "Tehri Safe Terrace B",
        "lat": 30.3800,
        "lng": 78.4800,
        "capacity": 500,
        "ccs": 82.0,
        "ahpBreakdown": {"landAvailability": 85, "infraAccess": 78, "livelihoodScore": 82, "legalClearance": 88},
    },
    {
        "id": "SITE_3",
        "name": "Joshimath Plateau Relocation Hub",
        "lat": 30.5600,
        "lng": 79.5700,
        "capacity": 600,
        "ccs": 74.5,
        "ahpBreakdown": {"landAvailability": 70, "infraAccess": 65, "livelihoodScore": 75, "legalClearance": 88},
    },
    {
        "id": "SITE_4",
        "name": "Bhowali Elevated Zone",
        "lat": 29.3800,
        "lng": 79.5200,
        "capacity": 400,
        "ccs": 86.0,
        "ahpBreakdown": {"landAvailability": 88, "infraAccess": 82, "livelihoodScore": 85, "legalClearance": 90},
    },
    {
        "id": "SITE_5",
        "name": "Meppadi Safe Township Site",
        "lat": 11.5500,
        "lng": 76.1200,
        "capacity": 750,
        "ccs": 89.0,
        "ahpBreakdown": {"landAvailability": 92, "infraAccess": 86, "livelihoodScore": 84, "legalClearance": 94},
    },
    {
        "id": "SITE_6",
        "name": "Siliguri Elevated Urban Buffer",
        "lat": 26.7100,
        "lng": 88.4300,
        "capacity": 900,
        "ccs": 91.5,
        "ahpBreakdown": {"landAvailability": 95, "infraAccess": 90, "livelihoodScore": 88, "legalClearance": 93},
    },
]

HABITATIONS_DB = [
    {
        "id": "HAB_1",
        "name": "Kotropi Slopes",
        "region": "Mandi, Himachal Pradesh",
        "lat": 31.8500,
        "lng": 76.9300,
        "hazardType": "Landslide",
        "households": 84,
        "hazard": 88.0,
        "vulnerability": 82.0,
        "history": 90.0,
        "baseline_hazard": 88.0,
        "siteId": "SITE_1",
    },
    {
        "id": "HAB_2",
        "name": "Malana River Bank",
        "region": "Kullu, Himachal Pradesh",
        "lat": 32.0600,
        "lng": 77.2600,
        "hazardType": "Cloudburst",
        "households": 120,
        "hazard": 92.0,
        "vulnerability": 78.0,
        "history": 85.0,
        "baseline_hazard": 92.0,
        "siteId": "SITE_1",
    },
    {
        "id": "HAB_3",
        "name": "Sunil Ward (Joshimath)",
        "region": "Chamoli, Uttarakhand",
        "lat": 30.5500,
        "lng": 79.5600,
        "hazardType": "Subsidence",
        "households": 165,
        "hazard": 85.0,
        "vulnerability": 89.0,
        "history": 75.0,
        "baseline_hazard": 85.0,
        "siteId": "SITE_3",
    },
    {
        "id": "HAB_4",
        "name": "Dharali Basin",
        "region": "Uttarkashi, Uttarakhand",
        "lat": 31.0300,
        "lng": 78.7800,
        "hazardType": "Erosion",
        "households": 62,
        "hazard": 65.0,
        "vulnerability": 60.0,
        "history": 70.0,
        "baseline_hazard": 65.0,
        "siteId": "SITE_2",
    },
    {
        "id": "HAB_5",
        "name": "Manikaran Valley",
        "region": "Kullu, Himachal Pradesh",
        "lat": 32.0270,
        "lng": 77.3450,
        "hazardType": "Cloudburst",
        "households": 95,
        "hazard": 89.0,
        "vulnerability": 76.0,
        "history": 88.0,
        "baseline_hazard": 89.0,
        "siteId": "SITE_1",
    },
    {
        "id": "HAB_6",
        "name": "Karnaprayag Confluence",
        "region": "Chamoli, Uttarakhand",
        "lat": 30.2600,
        "lng": 79.2150,
        "hazardType": "Subsidence",
        "households": 110,
        "hazard": 81.0,
        "vulnerability": 84.0,
        "history": 80.0,
        "baseline_hazard": 81.0,
        "siteId": "SITE_3",
    },
    {
        "id": "HAB_8",
        "name": "Thathri Village",
        "region": "Doda, Jammu & Kashmir",
        "lat": 33.1400,
        "lng": 75.7600,
        "hazardType": "Subsidence",
        "households": 78,
        "hazard": 84.0,
        "vulnerability": 80.0,
        "history": 70.0,
        "baseline_hazard": 84.0,
        "siteId": "SITE_3",
    },
    {
        "id": "HAB_9",
        "name": "Gaurikund Base",
        "region": "Rudraprayag, Uttarakhand",
        "lat": 30.6500,
        "lng": 79.0200,
        "hazardType": "Cloudburst",
        "households": 130,
        "hazard": 94.0,
        "vulnerability": 90.0,
        "history": 96.0,
        "baseline_hazard": 94.0,
        "siteId": "SITE_2",
    },
    {
        "id": "HAB_10",
        "name": "Chooralmala Slopes",
        "region": "Wayanad, Kerala",
        "lat": 11.5320,
        "lng": 76.1680,
        "hazardType": "Landslide",
        "households": 210,
        "hazard": 96.0,
        "vulnerability": 91.0,
        "history": 95.0,
        "baseline_hazard": 96.0,
        "siteId": "SITE_5",
    },
    {
        "id": "HAB_11",
        "name": "Mundakkai Village",
        "region": "Wayanad, Kerala",
        "lat": 11.5150,
        "lng": 76.1830,
        "hazardType": "Landslide",
        "households": 180,
        "hazard": 97.0,
        "vulnerability": 93.0,
        "history": 98.0,
        "baseline_hazard": 97.0,
        "siteId": "SITE_5",
    },
    {
        "id": "HAB_12",
        "name": "Ketti Valley Edge",
        "region": "Nilgiris, Tamil Nadu",
        "lat": 11.3800,
        "lng": 76.7100,
        "hazardType": "Landslide",
        "households": 90,
        "hazard": 79.0,
        "vulnerability": 74.0,
        "history": 82.0,
        "baseline_hazard": 79.0,
        "siteId": "SITE_5",
    },
    {
        "id": "HAB_7",
        "name": "Mirik Lake Ridge",
        "region": "Darjeeling, West Bengal",
        "lat": 26.8850,
        "lng": 88.1810,
        "hazardType": "Landslide",
        "households": 140,
        "hazard": 83.0,
        "vulnerability": 79.0,
        "history": 85.0,
        "baseline_hazard": 83.0,
        "siteId": "SITE_6",
    },
    {
        "id": "HAB_13",
        "name": "Ghoramara Island",
        "region": "Sundarbans, West Bengal",
        "lat": 21.6200,
        "lng": 88.1300,
        "hazardType": "Erosion",
        "households": 310,
        "hazard": 91.0,
        "vulnerability": 95.0,
        "history": 92.0,
        "baseline_hazard": 91.0,
        "siteId": "SITE_6",
    },
    {
        "id": "HAB_14",
        "name": "Haflong Hill Slopes",
        "region": "Dima Hasao, Assam",
        "lat": 25.1700,
        "lng": 93.0200,
        "hazardType": "Subsidence",
        "households": 125,
        "hazard": 87.0,
        "vulnerability": 83.0,
        "history": 88.0,
        "baseline_hazard": 87.0,
        "siteId": "SITE_6",
    },
    {
        "id": "HAB_15",
        "name": "Chungthang Basin",
        "region": "Mangan, Sikkim",
        "lat": 27.6000,
        "lng": 88.6400,
        "hazardType": "Cloudburst",
        "households": 150,
        "hazard": 95.0,
        "vulnerability": 88.0,
        "history": 94.0,
        "baseline_hazard": 95.0,
        "siteId": "SITE_6",
    },
]


# ==========================================
# Calculations & Helpers
# ==========================================

def calculate_haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def compute_rpi(hazard: float, vulnerability: float, history: float) -> float:
    rpi = (0.45 * hazard) + (0.35 * vulnerability) + (0.20 * history)
    return round(rpi, 1)


def get_priority_tier(rpi: float) -> str:
    if rpi >= 80.0:
        return "immediate"
    elif rpi >= 65.0:
        return "short"
    return "medium"


def enrich_habitation(hab: dict) -> dict:
    rpi = compute_rpi(hab["hazard"], hab["vulnerability"], hab["history"])
    tier = get_priority_tier(rpi)

    site = next((s for s in SITES_DB if s["id"] == hab["siteId"]), SITES_DB[0])
    
    # Direct Air Distance (Haversine)
    direct_km = calculate_haversine_km(hab["lat"], hab["lng"], site["lat"], site["lng"])

    # Flying Time (Chopper Speed = 180 km/h)
    flight_speed_kmh = 180.0
    flight_minutes = int((direct_km / flight_speed_kmh) * 60)
    flight_time_str = f"{flight_minutes // 60}h {flight_minutes % 60}m" if flight_minutes >= 60 else f"{flight_minutes} min" if flight_minutes > 0 else "< 1 min"

    # Ground / Road Distance (1.4x Mountain Circuity)
    road_km = round(direct_km * 1.4, 2)

    # Car Time (Car Evacuation Speed = 35 km/h)
    car_speed_kmh = 35.0
    car_minutes = int((road_km / car_speed_kmh) * 60)
    car_time_str = f"{car_minutes // 60}h {car_minutes % 60}m" if car_minutes >= 60 else f"{car_minutes} min"

    return {
        **hab,
        "rpi": rpi,
        "tier": tier,
        "siteName": site["name"],
        "distanceKm": direct_km,
        "roadDistanceKm": road_km,
        "flyingTime": flight_time_str,
        "carTime": car_time_str,
        "ahpBreakdown": site["ahpBreakdown"],
    }


# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def read_root():
    return {"status": "online", "system": "RedZone-AI Pan-India DSS", "version": "2.2.0"}


@app.get("/api/v1/bhuvan-config")
def get_bhuvan_config():
    """Returns official ISRO Bhuvan WMS capabilities."""
    return {"status": "success", "config": BHUVAN_CONFIG}


@app.get("/api/v1/habitations")
def get_habitations(hazard_type: Optional[str] = Query(None)):
    filtered = HABITATIONS_DB
    if hazard_type:
        filtered = [h for h in HABITATIONS_DB if h["hazardType"].lower() == hazard_type.lower()]

    enriched = [enrich_habitation(h) for h in filtered]
    enriched.sort(key=lambda x: x["rpi"], reverse=True)
    return {"status": "success", "count": len(enriched), "data": enriched}


@app.get("/api/v1/sites")
def get_sites():
    return {"status": "success", "count": len(SITES_DB), "data": SITES_DB}


@app.patch("/api/v1/habitations/{hab_id}")
def update_habitation(hab_id: str, payload: HabitationUpdate):
    hab = next((h for h in HABITATIONS_DB if h["id"] == hab_id), None)
    if not hab:
        raise HTTPException(status_code=404, detail="Habitation not found")

    if payload.hazard is not None:
        hab["hazard"] = payload.hazard
    if payload.vulnerability is not None:
        hab["vulnerability"] = payload.vulnerability
    if payload.history is not None:
        hab["history"] = payload.history

    return {"status": "updated", "data": enrich_habitation(hab)}


@app.post("/api/v1/simulate-cloudburst")
def simulate_cloudburst(payload: SimulationRequest):
    rainfall = payload.rainfall_mm

    for hab in HABITATIONS_DB:
        if rainfall == 0.0:
            hab["hazard"] = hab["baseline_hazard"]
        else:
            added_risk = (rainfall / 300.0) * 20.0
            hab["hazard"] = min(100.0, round(hab["baseline_hazard"] + added_risk, 1))

    enriched = [enrich_habitation(h) for h in HABITATIONS_DB]
    enriched.sort(key=lambda x: x["rpi"], reverse=True)
    return {"status": "simulation_applied", "rainfall_mm": rainfall, "data": enriched}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
