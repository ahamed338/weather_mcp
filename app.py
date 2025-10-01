import gradio as gr
import requests
import os

# OpenWeatherMap API key from environment
API_KEY = os.getenv("OWM_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OWM_API_KEY environment variable")

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        resp = requests.get(url, timeout=5).json()

        if resp.get("cod") != 200:
            return f"<div style='color:red; font-weight:bold;'>Error: {resp.get('message', 'City not found')}</div>"

        temp = resp["main"]["temp"]
        condition = resp["weather"][0]["description"].capitalize()

        # HTML card
        html = f"""
        <div style="
            background: linear-gradient(to right, #4facfe, #00f2fe);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            width: 300px;
            font-family: Arial, sans-serif;
        ">
            <h2>{city}</h2>
            <p style="font-size: 1.5em;">{temp}°C</p>
            <p style="font-size: 1.2em;">{condition}</p>
        </div>
        """
        return html
    except requests.exceptions.RequestException as e:
        return f"<div style='color:red;'>Server error: {e}</div>"
    except Exception as e:
        return f"<div style='color:red;'>Unexpected error: {e}</div>"

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
    outputs=gr.HTML(),  # Using HTML output for styling
    title="Weather Robot",
    description="Select a city and get real-time weather!"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    iface.launch(server_name="0.0.0.0", server_port=port)
