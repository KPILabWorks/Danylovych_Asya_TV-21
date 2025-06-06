import requests
import mysql.connector
from datetime import datetime, timedelta
import schedule
import time

# Повний URL для запиту
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=Europe%2FBerlin&past_days=2"

def fetch_and_save_data():
    # Виконання запиту
    response = requests.get(url)

    # Перевірка статусу відповіді
    if response.status_code == 200:
        data = response.json()

        # Перевірка наявності необхідних полів у відповіді
        if 'current' in data and all(field in data['current'] for field in
                                     ['temperature_2m', 'relative_humidity_2m', 'surface_pressure', 'wind_speed_10m',
                                      'wind_direction_10m']):
            # Підключення до бази даних
            connection = mysql.connector.connect(
                user='root',
                password='Pass123!',
                host='localhost',
                port='3306',
                database='weather_monitoring'
            )
            cursor = connection.cursor()

            # Отримання поточного часу
            current_time = datetime.now()

            # Отримання даних з відповіді
            current = data['current']
            temperature = current['temperature_2m']
            humidity = current['relative_humidity_2m']
            pressure = current['surface_pressure']
            wind_speed = current['wind_speed_10m']
            wind_direction = current['wind_direction_10m']

            # Вставка даних у таблицю
            sql = """
            INSERT INTO weather_data (timestamp, temperature, humidity, pressure, wind_speed, wind_direction)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (current_time, temperature, humidity, pressure, wind_speed, wind_direction)
            cursor.execute(sql, values)

            # Збереження змін
            connection.commit()

            # Закриття підключення
            cursor.close()
            connection.close()

            print("Дані збережено в базі даних")
        else:
            print("Помилка: відсутні необхідні поля в відповіді API")
    else:
        print(f"Помилка: {response.status_code}")

def calculate_apparent_temperature(temperature, wind_speed, humidity): # Відчутна температура
    if not (0 <= humidity <= 100):
        raise ValueError("Вологість повинна бути в межах від 0 до 100%")
    if wind_speed == 0: # вплив вітру відсутній, темп стабільна
        return temperature
    if temperature < 10: #холодна температура, холодний індекс
        wind_chill = 13.12 + 0.6215 * temperature - 11.37 * (wind_speed ** 0.16) + 0.3965 * temperature * (wind_speed ** 0.16)
        return wind_chill
    elif temperature > 27: # спекотна темп, індекс нагрівання
        temp_f = temperature * 9 / 5 + 32
        heat_index = -42.379 + 2.04901523 * temp_f + 10.14333127 * humidity - 0.22475541 * temp_f * humidity - 6.83783 * 10 ** -3 * temp_f ** 2 - 5.481717 * 10 ** -2 * humidity ** 2 + 1.22874 * 10 ** -3 * temp_f ** 2 * humidity + 8.5282 * 10 ** -4 * temp_f * humidity ** 2 - 1.99 * 10 ** -6 * temp_f ** 2 * humidity ** 2
        return (heat_index - 32) * 5 / 9
    else:
        return temperature

def get_wind_direction_string(degrees):
    degrees = degrees % 360
    # 8 діапазонів
    if 0 <= degrees < 22.5 or 337.5 <= degrees < 360:
        return "Північ"
    elif 22.5 <= degrees < 67.5:
        return "Північний схід"
    elif 67.5 <= degrees < 112.5:
        return "Схід"
    elif 112.5 <= degrees < 157.5:
        return "Південний схід"
    elif 157.5 <= degrees < 202.5:
        return "Південь"
    elif 202.5 <= degrees < 247.5:
        return "Південний захід"
    elif 247.5 <= degrees < 292.5:
        return "Захід"
    elif 292.5 <= degrees < 337.5:
        return "Північний захід"

def analyze_data():
    connection = mysql.connector.connect(
        user='root',
        password='Pass123!',
        host='localhost',
        port='3306',
        database='weather_monitoring'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT AVG(temperature) FROM weather_data")
    avg_temp = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(humidity) FROM weather_data")
    avg_humidity = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(pressure) FROM weather_data")
    avg_pressure = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(wind_speed) FROM weather_data")
    avg_wind_speed = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(temperature), MIN(temperature) FROM weather_data")
    max_temp, min_temp = cursor.fetchone()

    cursor.execute("SELECT MAX(humidity), MIN(humidity) FROM weather_data")
    max_humidity, min_humidity = cursor.fetchone()

    cursor.execute("SELECT MAX(pressure), MIN(pressure) FROM weather_data")
    max_pressure, min_pressure = cursor.fetchone()

    cursor.execute("SELECT MAX(wind_speed), MIN(wind_speed) FROM weather_data")
    max_wind_speed, min_wind_speed = cursor.fetchone()

    # Виведення результатів аналізу
    print(f"Середня температура: {avg_temp:.2f} °C")
    print(f"Середня вологість: {avg_humidity:.2f} %")
    print(f"Середній тиск: {avg_pressure:.2f} гПа")
    print(f"Середня швидкість вітру: {avg_wind_speed:.2f} км/год")

    print(f"Максимальна температура: {max_temp} °C, Мінімальна температура: {min_temp} °C")
    print(f"Максимальна вологість: {max_humidity} %, Мінімальна вологість: {min_humidity} %")
    print(f"Максимальний тиск: {max_pressure} гПа, Мінімальний тиск: {min_pressure} гПа")
    print(f"Максимальна швидкість вітру: {max_wind_speed} км/год, Мінімальна швидкість вітру: {min_wind_speed} км/год")

    # Аналіз змін температури за останні два дні
    two_days_ago = datetime.now() - timedelta(days=2)
    cursor.execute(""" 
    SELECT temperature FROM weather_data
    WHERE timestamp >= %s 
    ORDER BY timestamp ASC
    """, (two_days_ago,))
    temperatures = [row[0] for row in cursor.fetchall()]

    if len(temperatures) > 1:
        temp_change = temperatures[-1] - temperatures[0]
        if temp_change > 0:
            trend = "зростає"
        elif temp_change < 0:
            trend = "зменшується"
        else:
            trend = "стабільна"
        print(f"Тенденція температури за останні 2 дні: {trend} ({temp_change:.2f} °C)")
    else:
        print("Недостатньо даних для визначення тенденції температури.")

    print("------ Аналіз виконаний -------")

def check_weather_warnings():
    connection = mysql.connector.connect(
        user='root',
        password='Pass123!',
        host='localhost',
        port='3306',
        database='weather_monitoring'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(wind_speed) FROM weather_data")
    max_wind_speed = cursor.fetchone()[0]

    if max_wind_speed > 90:
        print("Попередження: Висока швидкість вітру!")

    cursor.close()
    connection.close()

def update_data():
    fetch_and_save_data()
    analyze_data()
    check_weather_warnings()

    # Виведення актуальних даних
    connection = mysql.connector.connect(
        user='root',
        password='Pass123!',
        host='localhost',
        port='3306',
        database='weather_monitoring'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT timestamp, temperature, humidity, pressure, wind_speed, wind_direction FROM weather_data ORDER BY timestamp DESC LIMIT 1")
    last_entry = cursor.fetchone()

    if last_entry:
        timestamp, temperature, humidity, pressure, wind_speed, wind_direction = last_entry
        wind_direction_str = get_wind_direction_string(wind_direction)
        print("\nАктуальні дані:")
        print(f"Час: {timestamp}")
        print(f"Температура: {temperature} °C")
        print(f"Вологість: {humidity} %")
        print(f"Тиск: {pressure} гПа")
        print(f"Швидкість вітру: {wind_speed} км/год")
        print(f"Напрямок вітру: {wind_direction_str}")
    # Розрахунок відчутної температури
    cursor.execute("SELECT temperature, wind_speed, humidity FROM weather_data ORDER BY timestamp DESC LIMIT 1")
    last_data = cursor.fetchone()
    if last_data:
        last_temp, last_wind_speed, last_humidity = last_data
        apparent_temp = calculate_apparent_temperature(last_temp, last_wind_speed, last_humidity)
        print(f"Температура відчувається як: {apparent_temp:.2f} °C")
    cursor.close()
    connection.close()

# Оновлення даних та аналіз
update_data()

# Планування оновлення даних кожну годину
schedule.every(1).hour.do(update_data)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)