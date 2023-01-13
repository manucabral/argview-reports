from argview import ARGViewReport
from constants import Endpoints, Filenames

if __name__ == '__main__':
    argview = ARGViewReport(verbose=True)
    """
    argview.remove(Filenames.TODAY_FORECAST)
    argview.remove(Filenames.WEATHER_STATIONS)

    argview.download(Endpoints.TODAY, Filenames.TODAY_FORECAST_ZIP)
    argview.extract(Filenames.TODAY_FORECAST_ZIP, override=True, output=Filenames.TODAY_FORECAST)
    argview.remove(Filenames.TODAY_FORECAST_ZIP)

    argview.download(Endpoints.WEATHER_STATIONS, Filenames.WEATHER_STATIONS_ZIP)
    argview.extract(Filenames.WEATHER_STATIONS_ZIP, override=True, output=Filenames.WEATHER_STATIONS)
    argview.remove(Filenames.WEATHER_STATIONS_ZIP)
    """
    weather_stations = argview.parse_weather_stations(Filenames.WEATHER_STATIONS)
    today_forecast = argview.parse_today_forecast(Filenames.TODAY_FORECAST)
    weather_stations = argview.merge_weather_stations(weather_stations, today_forecast)
    for weather_station in weather_stations:
        print(weather_station.name, weather_station.temperature)
    