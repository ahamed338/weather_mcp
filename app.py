import gradio as gr
import requests
import os

# If you have a real MCP server, replace this URL with its Railway URL
SERVER_URL = os.getenv("SERVER_URL", "https://example-mcp-server.up.railway.app/rpc")

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

cities = [
    "Delhi", "Mumbai", "Hyderabad", "Bangalore", "Chennai", "Kolkata",
    "Pune", "Jaipur", "Lucknow", "Ahmedabad", "Kochi", "Visakhapatnam",
    "Toronto", "New York", "London", "Paris", "Berlin", "Tokyo",
    "Sydney", "Melbourne", "Beijing", "Shanghai", "Dubai", "Singapore",
    "Moscow", "Los Angeles", "San Francisco", "Chicago"
]

iface = gr.Interface(
    fn=get_weather,
    inputs=gr.Dropdown(cities, label="Select a city"),
    outputs="text",
    title="Weather Robot",
    description="Select a city and get real-time weather from your MCP server!"
)

if __name__ == "__main__":
    # Railway sets PORT environment variable automatically
    port = int(os.environ.get("PORT", 7860))
    iface.launch(server_name="0.0.0.0", server_port=port)
