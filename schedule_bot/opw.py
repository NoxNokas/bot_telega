import requests as req

from .config import Config


def get_weather(location: str = 'Moscow') -> dict:
    res = req.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={Config.OPW_TOKEN}&units=metric")
    if res.status_code == 200:
        return res.json()
    else:
        return {}
