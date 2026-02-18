from fastapi import FastAPI, Depends
import httpx
import requests
API_KEY = "1d50d02b721a40b89d6b9a0a8088d855"
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}

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

@app.get("/alerts")
async def read_alerts(alerts=Depends(get_all_alerts)):
    return alerts

@app.get("/alerts/{alert_id}")
async def read_alert(alert_id: str):
    return await get_alert_by_id(alert_id)