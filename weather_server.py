from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import requests

app = FastAPI()

class Request(BaseModel):
    method: str
    params: Dict[str, Any]

API_KEY = "de5e0342096a97b3bcfdcf9b3f627c15" # <-- Replace with your OpenWeatherMap API key

@app.post("/rpc")
async def rpc(request: Request):
    if request.method == "get_weather":
        city = request.params.get("city")
        if not city:
            return {"result": {"error": "City not provided"}}
        # Call OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            resp = requests.get(url, timeout=5).json()
            if resp.get("cod") != 200:
                return {"result": {"error": resp.get("message", "City not found")}}
            return {"result": {
                "city": city,
                "temperature": resp["main"]["temp"],
                "condition": resp["weather"][0]["description"]
            }}
        except requests.exceptions.RequestException as e:
            return {"result": {"error": f"Server error: {e}"}}
    return {"error": "Method not found"}
