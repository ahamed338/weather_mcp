import gradio as gr
import requests

SERVER_URL = "http://127.0.0.1:8000/rpc"

def get_weather(city):
    try:
        req = {"method": "get_weather", "params": {"city": city}}
        resp = requests.post(SERVER_URL, json=req, timeout=5).json()
        result = resp.get("result")
        if not result:
            return "No response from server."
        if "error" in result:
            return f"Error: {result['error']}"
        return f"Weather in {result['city']}: {result['temperature']}°C, {result['condition'].capitalize()}"
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
    description="Select a city and get real-time weather from your MCP server!"
)

# Launch GUI in browser
iface.launch(inbrowser=True)
