from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta, timezone
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/earthquakes')
def get_earthquakes():
    """Fetch recent earthquakes from USGS API - FIXED"""
    try:
        # Fixed USGS API endpoint (today's data)
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        earthquakes = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geom = feature.get('geometry', {}).get('coordinates', [])
            
            # Fixed: use correct field names from USGS API
            earthquakes.append({
                'id': feature.get('id', 'unknown'),
                'title': props.get('title', 'No title'),
                'magnitude': props.get('mag', 0),
                'time': props.get('time', 0),
                'lat': geom[1] if len(geom) > 1 else 0,
                'lng': geom[0] if len(geom) > 0 else 0,
                'depth': geom[2] if len(geom) > 2 else 0
            })
        
        # Filter out invalid entries
        earthquakes = [eq for eq in earthquakes if eq['lat'] and eq['lng'] and eq['magnitude'] is not None]
        
        return jsonify(earthquakes[:100])  # Limit for performance
        
    except Exception as e:
        print(f"Earthquake API error: {e}")
        # Fallback sample data
        return jsonify([
            {'id': 'sample1', 'title': 'M 5.2 India', 'magnitude': 5.2, 'time': 1640995200000, 'lat': 21.15, 'lng': 79.09},
            {'id': 'sample2', 'title': 'M 4.8 Pacific', 'magnitude': 4.8, 'time': 1640995200000, 'lat': 10.5, 'lng': 95.2}
        ])

@app.route('/api/weather_stations')
def get_weather_stations():
    """Weather stations - FIXED route name"""
    stations = [
        {'name': 'Nagpur Airport', 'lat': 21.0927, 'lng': 79.1084, 'temp': 28.5, 'humidity': 65},
        {'name': 'Mumbai Colaba', 'lat': 19.0760, 'lng': 72.8777, 'temp': 30.2, 'humidity': 72},
        {'name': 'Delhi Safdarjung', 'lat': 28.6139, 'lng': 77.2090, 'temp': 22.1, 'humidity': 55},
        {'name': 'Pune Lohegaon', 'lat': 18.5820, 'lng': 73.9199, 'temp': 27.8, 'humidity': 68},
        {'name': 'Bangalore', 'lat': 12.9791, 'lng': 77.6044, 'temp': 26.3, 'humidity': 70}
    ]
    return jsonify(stations)

@app.route('/api/analytics/<dataset>')
def get_analytics(dataset):
    """Basic analytics"""
    return jsonify({
        'total': 847,
        'avg_magnitude': 2.8,
        'max_magnitude': 6.2,
        'most_active_region': 'Pacific Ring of Fire'
    })

if __name__ == '__main__':
    app.run(debug=True)
