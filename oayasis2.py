import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import requests
import csv
from datetime import datetime


class WeatherApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Weather App")

        self.api_key = "f675a8fdd91bb0eba612e25b7b2d485b"  # Replace with your API key

        self.create_widgets()

    def create_widgets(self):
        self.city_label = tk.Label(self.root, text="Enter City:")
        self.city_label.pack()

        self.city_entry = tk.Entry(self.root)
        self.city_entry.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.get_weather)
        self.search_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        if city:
            weather = self.fetch_weather(city)
            if weather:
                self.display_weather(weather)
                self.save_weather_data(city, weather)
            else:
                messagebox.showerror("Error", "Could not retrieve weather data.")
        else:
            messagebox.showwarning("Input Error", "Please enter a city name.")

    def fetch_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def display_weather(self, weather):
        description = weather['weather'][0]['description']
        temperature = weather['main']['temp']
        city_name = weather['name']

        result_text = f"City: {city_name}\nWeather: {description}\nTemperature: {temperature}°C"
        self.result_label.config(text=result_text)

    def save_weather_data(self, city, weather):
        # Prepare the data to be saved
        data = {
            "city": city,
            "description": weather['weather'][0]['description'],
            "temperature": weather['main']['temp'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save the data to a CSV file
        with open('weather_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data['timestamp'], data['city'], data['description'], data['temperature']])


if _name_ == "_main_":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()