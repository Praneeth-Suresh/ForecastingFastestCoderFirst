import tkinter as tk
from PIL import ImageTk, Image
from APIGen import ParseRawWeatherFC, GetRawWeatherFC
import sys
import requests
from io import BytesIO
from datetime import date
from main import GetNextWeather

#Create Tkinter Window
window = tk.Tk()
window.title("Hourly Weather Comparison")

# Get city name from command line arguments
try:
    city = "+".join(sys.argv[1:])
except IndexError:
    print("Please enter a city name as an argument")
    sys.exit("Please enter a city name as an argument")


def AIInput(city) :
    api_weather_data = ParseRawWeatherFC(GetRawWeatherFC(city)) # [cityname, date, {hourly weather data}]
    ai_weather_data = []

    # Remove spaces and lowercase a string
    def CondenseName(string):
        return ''.join(c.lower() for c in string if not c.isspace())

    cities = ["newyork", "riodejaneiro", "capetown", "buenos+aires", "shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]

    # Create a dictionary with "not available" 
    blank = {'time': "Not available",
            'tempC': "Not available",
            'windspeedKmph': "Not available",
            'rainfall': "Not available",
            'humidity': "Not available",
            'pressure': "Not available",
            'cloudcover': "Not available"}

    for x in range(3):
        blank['time'] = str(x) + ":00"
        ai_weather_data.append(blank.copy())

    if CondenseName(city) in cities:
        # Use the AI model in addition to the API
        for hr in range(0, 24, 3):
            ai_input_data = [api_weather_data[hr+2]['time'][:2],
                    api_weather_data[hr+2]['tempC'],
                    api_weather_data[hr+2]['windspeedKmph'],
                    api_weather_data[hr+2]['rainfall'],
                    api_weather_data[hr+2]['humidity'],
                    api_weather_data[hr+2]['pressure'],
                    api_weather_data[hr+2]['cloudcover']
            ]

            ai_input_data = [float(ai_input_data[x]) for x in range(len(ai_input_data))]

            # model training goes here (output a list)
            hourly_ai_dict = GetNextWeather(cities.index(CondenseName(city)), ai_input_data)
            hourly_ai_dict['time'] = str(int(hourly_ai_dict['time'])) + ":00"
            ai_weather_data.append(hourly_ai_dict.copy())
            hourly_ai_dict.clear()
            ai_input_data.clear()

            for x in range(2):
                blank['time'] = str(hr + x + 1 + 3) + ":00"
                # print(" Added :"+ blank['time'])
                ai_weather_data.append(blank.copy())

    return ai_weather_data #(in form of list)

# Create a label to display the city and date
city_date_label = tk.Label(window, font=('Helvetica', 16))
city_date_label.pack(pady=10)

# Create a frame to hold the postcards
postcards_frame = tk.Frame(window)
postcards_frame.pack(pady=10, padx=10)

# Create a label to display the weather details for Dataset 1
weather_details1 = tk.Label(postcards_frame, font=('Helvetica', 14))
weather_details1.pack(side='left', padx=10, pady=10)

# Create a label to display the weather details for Dataset 2
weather_details2 = tk.Label(postcards_frame, font=('Helvetica', 14))
weather_details2.pack(side='left', padx=10)

# Crete a label to display the current postcard
current_postcard1 = tk.Label(postcards_frame, font=('Helvetica', 14))
current_postcard1.pack(side='left', padx=10)

# Function to update the postcards and weather details
def update_postcards(index):
    # Load the common weather icon from URL
    response = requests.get(api_weather_data[index]['weatherIconUrl'])
    weather_icon = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))

    # Update the city and date label
    city_date_label.config(text=f"{api_weather_data[0]} - {api_weather_data[1]}")

    # Update the postcards and weather details for Dataset 1
    current_postcard1.config(image=weather_icon)
    current_postcard1.image = weather_icon
    weather_details1.config(text=f"Time: {api_weather_data[index]['time']}\n"
                                 f"Temperature: {api_weather_data[index]['tempC']}°C\n"
                                 f"Weather: {api_weather_data[index]['weatherDesc']}\n"
                                 f"Windspeed: {api_weather_data[index]['windspeedKmph']} km/h\n"
                                 f"Rainfall: {api_weather_data[index]['rainfall']} mm\n"
                                 f"Humidity: {api_weather_data[index]['humidity']}%\n"
                                 f"Visibility: {api_weather_data[index]['visibility']} km\n"
                                 f"Pressure: {api_weather_data[index]['pressure']} hPa\n"
                                 f"Cloudcover: {api_weather_data[index]['cloudcover']}%\n"
                                 f"Feels Like: {api_weather_data[index]['FeelsLikeC']}°C")

    # Update the postcards and weather details for AI Dataset

    if CondenseName(city) in cities:
        weather_details2.config(text=f"Time: {ai_weather_data[index - 2]['time']}\n"
                                    f"Temperature: {ai_weather_data[index - 2]['tempC']}°C\n"
                                    f"Windspeed: {ai_weather_data[index - 2]['windspeedKmph']} km/h\n"
                                    f"Rainfall: {ai_weather_data[index - 2]['rainfall']} mm\n"
                                    f"Humidity: {ai_weather_data[index - 2]['humidity']}%\n"
                                    f"Pressure: {ai_weather_data[index - 2]['pressure']} hPa\n"
                                    f"Cloudcover: {ai_weather_data[index - 2]['cloudcover']}%\n")
    else:
        # The get a singular output only from the API
        pass


# Initial index for the postcards
current_index = 2
update_postcards(current_index)

# Button to swipe left
def swipe_left():
    global current_index
    if current_index > 2:
        current_index -= 1
        update_postcards(current_index)

left_button = tk.Button(window, text="Previous Hour", command=swipe_left)
left_button.pack(side='left', padx=10)

# Button to swipe right
def swipe_right():
    global current_index
    if current_index < len(api_weather_data) - 1:
        current_index += 1
        update_postcards(current_index)

right_button = tk.Button(window, text="Next Hour", command=swipe_right)
right_button.pack(side='left', padx=10)

# Run the Tkinter event loop
window.mainloop()
