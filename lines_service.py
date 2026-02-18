from fastapi import FastAPI, Depends
import httpx
import requests
API_KEY = "1d50d02b721a40b89d6b9a0a8088d855"
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}

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
