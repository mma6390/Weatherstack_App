import requests
import tkinter as tk
from tkinter import messagebox

def get_weather():
    location = entry.get()
    if not location:
        messagebox.showwarning("Warning", "Please enter a location")
        return
    
    try:
        response = requests.get(
            "http://api.weatherstack.com/current",
            params={
                'query': location,
                'access_key': '2085ddd538a1fc42e5f3f252edec0873',  
                'units': 'm'
            }
        )
        data = response.json()
        
        if 'error' in data:
            messagebox.showerror("Error", data['error']['info'])
            return
            
        current = data['current']
        
        weather_info = (
            
            f"Temperature: {current['temperature']}°C\n"
            f"Humidity: {current['humidity']}%\n"
            f"Wind Speed: {current['wind_speed']} km/h\n"
            f"Pressure: {current['pressure']} MB\n"
            f"Precipitation: {current['precip']} MM\n"
        )
        result.config(text=weather_info)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather: {e}")

# Create main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# Widgets
tk.Label(root, text="Enter location:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack()

tk.Button(root, text="Get Weather", command=get_weather).pack(pady=10)

result = tk.Label(root, text="", justify='left')
result.pack(pady=20)

root.mainloop()