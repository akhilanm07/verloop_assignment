import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
BASE_URL = "https://weatherapi-com.p.rapidapi.com/current.json"


def get_weather_data(city):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    params = {
        "q": city
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json() if response.ok else None

 
@app.route('/getCurrentWeather', methods=['POST'])
def get_current_weather():
    data = request.get_json()
    city = data.get('city')
    output_format = data.get('output_format')

    if not city or not output_format:
        return jsonify({'error': 'City and output_format are required.'}), 400

    weather_data = get_weather_data(city)
    if not weather_data:
        return jsonify({'error': 'Unable to fetch weather data.'}), 500

    response_data = {
        "Weather": weather_data["current"]["temp_c"],
        "Latitude": weather_data["location"]["lat"],
        "Longitude": weather_data["location"]["lon"],
        "City": f'{weather_data["location"]["name"]}, {weather_data["location"]["country"]}'
    }

    if output_format.lower() == 'xml':
        xml_response = f'<?xml version="1.0" encoding="UTF-8" ?>\n'
        xml_response += "<root>\n"
        for key, value in response_data.items():
            xml_response += f'<{key}>{value}</{key}>\n'
        xml_response += "</root>\n"
        return xml_response, 200, {'Content-Type': 'application/xml'}
    elif output_format.lower() == 'json':
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Invalid output_format. Only json and xml are supported.'}), 400


if __name__ == '__main__':
    app.run()