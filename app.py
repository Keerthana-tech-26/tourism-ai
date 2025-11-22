import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def get_coords(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json"}
    try:
        r = requests.get(url, params=params, timeout=5, headers={"User-Agent": "tourism-ai"})
        data = r.json()
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None

def get_weather(place):
    coords = get_coords(place)
    if not coords:
        return f"Cannot find {place}"
    
    lat, lon = coords
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation_probability"
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        temp = data['current']['temperature_2m']
        rain = data['current']['precipitation_probability']
        return f"In {place} it's currently {temp}°C with {rain}% chance to rain."
    except:
        return f"Could not fetch weather for {place}"

def get_places(place):
    coords = get_coords(place)
    if not coords:
        return f"Cannot find {place}"
    
    lat, lon = coords
    south = lat - 0.1
    north = lat + 0.1
    west = lon - 0.1
    east = lon + 0.1
    
    query = f"[out:json];(node[tourism](bbox:{south},{west},{north},{east});way[tourism](bbox:{south},{west},{north},{east}););out center 100;"
    
    try:
        r = requests.post("https://overpass-api.de/api/interpreter", data=query, timeout=15)
        if r.status_code == 200:
            data = r.json()
            sites = []
            for elem in data.get('elements', []):
                tags = elem.get('tags', {})
                name = tags.get('name')
                ttype = tags.get('tourism')
                if name and ttype == 'attraction' and name not in sites:
                    sites.append(name)
                if len(sites) >= 5:
                    break
            
            if sites:
                return "Tourist attractions in " + place + ":\n" + "\n".join(f"- {s}" for s in sites)
        return f"No attractions found for {place}"
    except:
        return f"Could not fetch places for {place}"

def process(query):
    extract_prompt = f"Extract the place name from this query: '{query}'. Return ONLY the place name."
    extract_resp = model.generate_content(extract_prompt)
    place = extract_resp.text.strip()

    result = ""

    if any(word in query.lower() for word in ["weather", "temperature"]):
        result += get_weather(place) + "\n"

    if any(word in query.lower() for word in ["visit", "places", "attractions", "plan"]):
        result += get_places(place)

    if not result.strip():
        result = get_places(place)

    return result.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        result = process(query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
