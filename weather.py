from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

def get_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/', methods=['POST', 'GET'])
def weather():
    api_key = '84d490224bf7fc25d752cd709f77386c'
    if request.method == 'POST':
        city = request.form['city']
    else:
        # For default name: Hyderabad
        city = 'hyderabad'
    
    # Fetch weather data from the API
    weather_data = get_weather_data(city, api_key)

    # Process the weather data and extract relevant information
    if weather_data['cod'] == 200:
        temperature_kelvin = weather_data['main']['temp']
        temperature_celsius = round(float(temperature_kelvin) - 273.15, 2)
        humidity = weather_data['main']['humidity']
        country_code = weather_data['sys']['country']
    else:
        # If the API response is not successful, handle the error here.
        # You can return an error message or redirect the user to an error page.
        # For simplicity, let's set default values for weather details.
        temperature_celsius = '--'
        humidity = '--'
        country_code = '--'

    # Prepare the data to be rendered in the template
    data = {
        "country_code": country_code,
        "temp_cel": temperature_celsius,
        "humidity": humidity,
        "cityname": city,
    }

    # Render the template with the weather data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
