import requests
from pprint import pprint
from .utils import convert_seconds_to_data
import json
import config
from db import queires as sql


def get_weather():
    data = []

    username = input("Enter username:\t")
    is_exists, user_id = sql.check_user_exists("weather.db", username)

    if not is_exists:
        sql.add_user("weather.db", username)
        get_weather()

    else:
        while True:
            city = input("Напишите свой город:\t")
            if city == "save":
                with open("save.json", mode='w', encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                continue

            elif city == "show":
                all_weather = sql.get_user_weather("weather.db", user_id)
                if not all_weather:
                    continue
                for item in all_weather:
                    name, _, sunrise, dt, speed = item[1:-1]
                    pprint(f'''
                    ==========================
                    В городе {name}:
                    Скорость ветра : {speed}
                    Восход солнца : {sunrise}
                    Время отправки запроса : {dt}
                    ==========================
                    ''')
                continue
            elif city == "clear":
                sql.clear_user_weather("weather.db", user_id)
                print("history of brazzers cleaned")

                continue

            config.parameters["q"] = city
            resp = requests.get(config.url, params=config.parameters).json()
            tz = resp["timezone"]
            sunrise = convert_seconds_to_data(seconds=resp["sys"]["sunrise"], timezone=tz)
            dt = convert_seconds_to_data(seconds=resp["dt"], timezone=tz)
            name = resp["name"]

            speed = resp["wind"]["speed"]
            sql.add_weather("weather.db",
                            name=name,
                            tz=tz,
                            sunrise=sunrise,
                            dt=dt,
                            speed=speed,
                            user_id=user_id
                            )

            pprint(f'''
    ==========================
    В городе {name}:
    Скорость ветра : {speed}
    Восход солнца : {sunrise}
    Время отправки запроса : {dt}
    ==========================
    ''')
