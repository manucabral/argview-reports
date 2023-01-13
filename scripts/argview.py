from urllib.request import urlopen
from shutil import copyfileobj
from zipfile import ZipFile
from weather_station import WeatherStation
import os
import re

class ARGViewReport:

    def __init__(self, verbose = False):
        self.verbose = verbose

    def log(self, msg: str) -> None:
        if self.verbose:
            print(msg)
    
    def exists(self, filename: str) -> bool:
        return os.path.exists(filename)

    def download(self, url: str, dst: str) -> None:
        self.log(f'Downloading {url} to {dst}')
        with urlopen(url) as response, open(dst, 'wb') as output_file:
            copyfileobj(response, output_file)
            output_file.close()
        self.log('Download done')

    def extract(self, filename: str, override: bool = False, output: str = None) -> str:
        file = ZipFile(filename)
        file.extractall()
        extracted_file = file.namelist()[0]
        file.close()
        if override and output:
            self.log(f'Overriding {extracted_file} with {output}')
            os.rename(extracted_file, output)
        extracted_file = output
        self.log(f'Extraction of {filename} done, result -> {extracted_file}')
        return extracted_file

    def remove(self, filename: str) -> None:
        try:
            os.remove(filename)
        except Exception as exc:
            self.log(f'Error removing file: {exc}')
        self.log(f'File {filename} removed')
    
    def generate_weather_station(self, data: str) -> WeatherStation:
        data = re.split(r'\s{2,}', data)
        data = [i for i in data if i]
        # exclude corrupted data
        if len(data) < 2:
            return None
        # name is soo long, fix that error
        if 'SAENZ' in data[0] or 'MILITAR' in data[0]:
            data.insert(1, 'undefined')
        weather_station = WeatherStation(*data)
        return weather_station
        
    def parse_weather_stations(self, filename: str) -> [WeatherStation]:
        self.log('Parsing weather stations')
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
            file.close()
        # remove headers
        lines = lines[2:]
        weather_stations = []
        for line in lines:
            weather_station = self.generate_weather_station(line)
            if weather_station:
                weather_stations.append(weather_station)
        self.log(f'Generated {len(weather_stations)} weather stations')
        return weather_stations

    def merge_weather_stations(self, weather_stations: [WeatherStation], today_forecast: [str]) -> [WeatherStation]:
        self.log('Merging weather stations')
        for weather_station in weather_stations:
            for forecast in today_forecast:
                if forecast[0].lower() in weather_station.name.lower():
                    weather_station.status = forecast[2]
                    weather_station.wind = forecast[3]
                    weather_station.temperature = forecast[4]
                    break
        self.log('Merge done')    
    
    def parse_today_forecast(self, filename: str) -> [str]:
        self.log('Parsing today forecast')
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
            file.close()
        today_forecast = []
        for line in lines:
            line = line.strip()
            # removing last 2 characters
            line = line.replace(line[-2:], '')
            data = line.split(';')
            today_forecast.append(data)
            print(data)
        self.log(f'Generated {len(today_forecast)} today forecast')
        return today_forecast
            

        
