# Tourism AI System

Multi-agent tourism system that provides weather and tourist attractions for any place.

## Features
- Weather information (temperature, precipitation chance)
- Tourist attractions recommendations
- Multi-agent orchestration using Gemini AI

## APIs Used
- **Nominatim API** - Geocoding (place name to coordinates)
- **Open-Meteo API** - Weather data
- **Overpass API** - Tourist attractions from OpenStreetMap
- **Gemini AI** - Orchestration and natural language processing

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Create `.env` file with: `GOOGLE_API_KEY=your_key_here`
6. Run: `python tourism_ai.py`

## Usage
```
Enter your query (or 'exit' to quit): I'm going to go to Bangalore, let's plan my trip.
```

## Examples

- Weather: "I'm going to go to Bangalore, what is the temperature there"
- Places: "I'm going to go to Bangalore, let's plan my trip"
- Combined: "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"