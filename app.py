import os
import gradio as gr
import requests

# Read API key from environment
API_KEY = os.getenv("OWM_API_KEY")

if not API_KEY:
    raise ValueError("OpenWeatherMap API key not found. Set the OWM_API_KEY environment variable.")

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        resp = requests.get(url, timeout=5).json()
        
        if resp.get("cod") != 200:
            return f"Error: {resp.get('message', 'Unknown')}"
        
        return f"Weather in {resp['name']}: {resp['main']['temp']}°C, {resp['weather'][0]['description'].capitalize()}"
    
    except requests.exceptions.RequestException as e:
        return f"Server error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Cities for the dropdown
cities = [
    "Delhi", "Mumbai", "Hyderabad", "Bangalore", "Chennai", "Kolkata",
    "Pune", "Jaipur", "Lucknow", "Ahmedabad", "Kochi", "Visakhapatnam",
    "Toronto", "New York", "London", "Paris", "Berlin", "Tokyo",
    "Sydney", "Melbourne", "Beijing", "Shanghai", "Dubai", "Singapore",
    "Moscow", "Los Angeles", "San Francisco", "Chicago"
]

# Build Gradio interface
iface = gr.Interface(
    fn=get_weather,
    inputs=gr.Dropdown(cities, label="Select a city"),
    outputs="text",
    title="Weather Robot",
    description="Select a city and get real-time weather from OpenWeatherMap!"
)

# Launch GUI in browser (Railway will automatically handle ports)
iface.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 8080)))
