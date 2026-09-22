import pandas as pd 
import requests
from typing import  Dict, List, Callable
import concurrent.futures
import json
from dotenv import load_dotenv
load_dotenv()
import os

class APIClient:

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def build_url(self, endpoints: str):
        return f"{self.base_url}/{endpoints.lstrip('/')}"

    def get(self, endpoints: str, params: Dict) -> Dict:

        url = self.build_url(endpoints)

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            print(f"Request timed out for {url}")
            raise
        except requests.exceptions.ConnectionError:
            print(f"Connection error for {url}")
            raise
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {e.response.status_code}")
            raise
        except requests.JSONDecodeError:
            print(f"JSON Decode Error for {url}")
            raise


class BatchCollection:

    def __init__(self, api_client: APIClient, max_workers: int = 10):
        self.api_client = api_client
        self.max_workers = max_workers

    def collect_data_parallel(self, endpoints: str, params: List[Dict]) -> List[Dict]:

        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_parameter = {
                executor.submit(self.api_client.get, endpoints, params=param): param
                for param in params
            }

            for future in concurrent.futures.as_completed(future_to_parameter):
                param = future_to_parameter[future]

                try:
                    data = future.result()
                    results[param.get('q')] = data
                    print(f"Succesfully Fetched Data")
                except Exception as e:
                    print(f"Failed To fetch Data From {param}")
                    results[param.get('q')] = None

        return results



client = APIClient('https://api.openweathermap.org/data/2.5/')
collector = BatchCollection(client, max_workers=5)


cities = ['New York', 'Los Angeles', 
          'Chicago', 'Houston', 'Phoenix', 
          'Philadelphia', 'San Antonio', 
          'San Diego', 'Dallas', 'Fort Worth']

params = []

api_key = os.getenv("API_KEY_OWM")

for city in cities:
    param = {'q': city, 'appid': api_key}
    params.append(param)


data = collector.collect_data_parallel('/weather', params=params)

for city in data:
    with open('weather_data.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)

# Flatten the nested data using pandas 
with open('weather_data.json', 'r') as f:
    json_data = json.load(f)

def transform_weather_data():
    rows = []

    for city, weather_data in json_data.items():
        row = {
            'id': weather_data['id'],
            'city': city,
            'weather_id': weather_data['weather'][0]['id'],
            'weather_condition': weather_data['weather'][0]['main'],
            'description': weather_data['weather'][0]['description'],
            'temperature': weather_data['main']['temp'],
            'pressure': weather_data['main']['pressure'],
            'humidity': weather_data['main']['humidity'],
            'sea_level': weather_data['main']['sea_level'],
            'wind_speed': weather_data['wind']['speed']
        }
        rows.append(row)
        print(f"Succesfully loaded {city} weather data")

    return rows

df = pd.DataFrame(transform_weather_data())

print(df)