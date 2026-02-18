from fastapi import FastAPI, Depends
import httpx
import requests
API_KEY = "1d50d02b721a40b89d6b9a0a8088d855"
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()

# Dependency to fetch all alerts
async def get_all_alerts(route: str = None, stop: str = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route

    if stop:
        params["filter[stop]"] = stop

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}alerts", params=params)
        response.raise_for_status()
        return response.json()


# Dependency to fetch a specific alert by ID
async def get_alert_by_id(alert_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}alerts/{alert_id}?api_key={API_KEY}")
        response.raise_for_status()
        return response.json()

# Dependency to fetch all vehicles
async def get_all_vehicles(route: str = None, revenue: str = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route
    if revenue:
        params["filter[revenue]"] = revenue

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ENDPOINT_URL}vehicles", params=params)
            response.raise_for_status()
            return response.json()
#Dependency to fetch a specific vehicle by ID
async def get_vehicle_by_id(vehicle_id: str):
    params = {"api_key": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}vehicles/{vehicle_id}", params=params)
        response.raise_for_status()
        return response.json()



@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}

@app.get("/routes")
def get_routes():
    routes_list = []
    response = requests.get(ENDPOINT_URL + f"routes?api_key={API_KEY}")
    routes = response.json()["data"]

    for route in routes:
        routes_list.append({
            "id": route["id"],
            "type": route["type"],
            "color": route["attributes"]["color"],
            "text_color": route["attributes"]["text_color"],
            "description": route["attributes"]["description"],
            "long_name": route["attributes"]["long_name"],
        })

    return {"routes": routes_list}

@app.get("/routes/{route_id}")
def get_route(route_id: str):
    response = requests.get(ENDPOINT_URL + f"routes/{route_id}?api_key={API_KEY}")
    route_data = response.json()["data"]

    route = {
        "id": route_data["id"],
        "type": route_data["type"],
        "color": route_data["attributes"]["color"],
        "text_color": route_data["attributes"]["text_color"],
        "description": route_data["attributes"]["description"],
        "long_name": route_data["attributes"]["long_name"],
    }

    return {"route": route}

@app.get("/lines")
def get_lines():
    lines_list = []
    response = requests.get(ENDPOINT_URL + f"lines?api_key={API_KEY}")
    lines = response.json()["data"]

    for line in lines:
        lines_list.append({
            "id": line["id"],
            "text_color": line["attributes"]["text_color"],
            "short_name": line["attributes"]["short_name"],
            "long_name": line["attributes"]["long_name"],
            "color": line["attributes"]["color"],
        })

    return {"lines": lines_list}

@app.get("/lines/{line_id}")
def get_line(line_id: str):
    response = requests.get(ENDPOINT_URL + f"lines/{line_id}?api_key={API_KEY}")
    line_data = response.json()["data"]

    line = {
        "id": line_data["id"],
        "text_color": line_data["attributes"]["text_color"],
        "short_name": line_data["attributes"]["short_name"],
        "long_name": line_data["attributes"]["long_name"],
        "color": line_data["attributes"]["color"],
    }
    return {"line": line}

@app.get("/alerts")
async def read_alerts(alerts=Depends(get_all_alerts)):
    return alerts

@app.get("/alerts/{alert_id}")
async def read_alert(alert_id: str):
    return await get_alert_by_id(alert_id)

@app.get("/vehicles")
async def read_vehicles(vehicles=Depends(get_all_vehicles)):
    return vehicles
@app.get("/vehicles/{vehicle_id}")
async def read_vehicle(vehicle_id: str):
    return await get_vehicle_by_id(vehicle_id)


