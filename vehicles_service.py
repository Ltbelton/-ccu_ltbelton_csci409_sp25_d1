from fastapi import FastAPI, Depends
import httpx
import requests
API_KEY = "1d50d02b721a40b89d6b9a0a8088d855"
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}

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


@app.get("/vehicles")
async def read_vehicles(vehicles=Depends(get_all_vehicles)):
    return vehicles
@app.get("/vehicles/{vehicle_id}")
async def read_vehicle(vehicle_id: str):
    return await get_vehicle_by_id(vehicle_id)
