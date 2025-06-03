import requests
import tkinter as tk
from tkinter import messagebox

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App (weatherstack)")
        self.root.geometry("500x350")
        self.root.minsize(450, 300)
        
        # Initialize widgets
        self.location_entry = None
        self.result_label = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Location Entry Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Location:", font=('Arial', 12)).pack(side=tk.LEFT)
        self.location_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
        self.location_entry.pack(side=tk.LEFT, padx=10)

        # Search Button
        search_button = tk.Button(self.root, text="Get Weather", font=('Arial', 12), 
                                command=self.fetch_weather, bg='#4CAF50', fg='white')
        search_button.pack(pady=10)

        # Result Label with scrollbar
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_label = tk.Text(result_frame, font=('Arial', 11), wrap=tk.WORD,
                                  yscrollcommand=scrollbar.set, padx=10, pady=10,
                                  height=10, width=50)
        self.result_label.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.result_label.yview)
    
    def get_weather(self, api_key, location):
        base_url = "http://api.weatherstack.com/current"
        params = {
            'query': location,
            'access_key': api_key,
            'units': 'm'  # Metric units (temperature in Celsius)
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                messagebox.showerror("API Error", data['error']['info'])
                return None
                
            current = data.get('current', {})
            location_info = data.get('location', {})
            
            weather = {
                'city': location_info.get('name', 'N/A'),
                'region': location_info.get('region', 'N/A'),
                'country': location_info.get('country', 'N/A'),
                'temperature': current.get('temperature', 'N/A'),
                'description': current.get('weather_descriptions', ['N/A'])[0],
                'humidity': current.get('humidity', 'N/A'),
                'wind_speed': current.get('wind_speed', 'N/A'),
                'feelslike': current.get('feelslike', 'N/A'),
                'precip': current.get('precip', 'N/A'),
                'visibility': current.get('visibility', 'N/A')
            }
            return weather
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to weather service: {str(e)}")
            return None
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to parse weather data: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return None
    
    def fetch_weather(self):
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Warning", "Please enter a location")
            return
        
        api_key = "2085ddd538a1fc42e5f3f252edec0873"  # Replace with your actual weatherstack API key
        weather = self.get_weather(api_key, location)
        
        if weather:
            result_text = (
                f"Weather in {weather['city']}, {weather['region']}, {weather['country']}:\n"
                f"Temperature: {weather['temperature']}°C (Feels like {weather['feelslike']}°C)\n"
                f"Conditions: {weather['description']}\n"
                f"Humidity: {weather['humidity']}%\n"
                f"Wind Speed: {weather['wind_speed']} km/h\n"
                f"Precipitation: {weather['precip']} mm\n"
                f"Visibility: {weather['visibility']} km"
            )
            self.result_label.delete(1.0, tk.END)  # Clear previous content
            self.result_label.insert(tk.END, result_text)
        else:
            self.result_label.delete(1.0, tk.END)
            self.result_label.insert(tk.END, "Could not fetch weather data")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()