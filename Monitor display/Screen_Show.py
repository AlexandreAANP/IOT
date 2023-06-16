import requests
import tkinter as tk
from PIL import ImageTk, Image
import time
import threading
import random
import io
import subprocess
import screeninfo
import psutil 


# WeatherAPI configuration
API_KEY = '2a9180234a8640d1955201144232805'
LOCATION = 'Faro'

# Pexels API configuration
PEXELS_API_KEY = 'tDAOCCyiVdAgtn5Z6n8xDRhzCsT46vZAmEDP67Oi71Y9yEPQnRaP11B3'
PEXELS_API_URL = f'https://api.pexels.com/v1/search?query={LOCATION}&per_page=10'
HEADERS = {'Authorization': PEXELS_API_KEY}

URL_TO_DISPLAY = "https://cnnportugal.iol.pt/"

FIRST_TRANSITION = 20
SECOND_TRANSITION = 30

root = tk.Tk()
root.title("Weather Display")

SFTP_HOST = "10.20.74.26"
SFTP_USER = "ORV"
SFTP_PASSWORD = "password"
SFTP_PORT = 2223

# Function to fetch weather data from the API
def fetch_weather():
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"
        response = requests.get(url)
        data = response.json()
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        location = data['location']['name']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']
        with open("environmentLogs","w") as f:
            f.write('{"temperature":"'+str(temperature)+'","condition":"'+str(condition)+'","location":"'+str(location)+'","humidity":"'+str(humidity)+'","wind_kph":"'+str(wind_kph)+'"}')
        weather_label.config(
            text=f"Location: {location}\nTemperature: {temperature}°C\nCondition: {condition}\nHumidity: {humidity}%\nWind Speed: {wind_kph} kph"
        )
    except requests.exceptions.RequestException as e:
        weather_label.config(text="Error fetching weather data.")

# Function to fetch random image URL from Pexels
def fetch_random_image():
    try:
        response = requests.get(PEXELS_API_URL, headers=HEADERS)
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            photo = random.choice(photos)
            image_url = photo.get('src', {}).get('large2x', '')  # Use larger image size
            return image_url
    except requests.exceptions.RequestException as e:
        print("Error fetching random image.")
    return None

# Function to switch to video display
def switch_to_video():
    #rotate_screen(90)  # Reset screen rotation before playing the video
    play_video_from_sftp(SFTP_USER, SFTP_HOST, "test.mp4", SFTP_PORT,SFTP_PASSWORD) #change the video path
    open_website()
    #rotate_screen(90)  # Reset the screen rotation after playing the video

# Function to update weather data and schedule video display
def update_and_switch():
    set_background_image()
    fetch_weather()
    threading.Timer(FIRST_TRANSITION, switch_to_video).start()

# Function to rotate the screen using platform-specific commands
def rotate_screen(degrees):
    system = tk.sys.platform
    if system == 'win32':
        command = f"powershell.exe -Command \"$monitor = Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBasicDisplayParams -Filter 'Active=\\'True\\''; $monitor.WmiSetMethod('Rotate', {degrees});\""
        subprocess.call(command, shell=True)
    elif system == 'linux':
        command = f"xrandr --output $(xrandr --listmonitors | awk '/\\*/{{print $4}}') --rotate {'left' if degrees == 90 else 'right'}"
        subprocess.call(command, shell=True)
    elif system == 'darwin':  # macOS
        command = f"osascript -e 'tell application \"System Events\" to tell orientation preferences to set landscape'"
        subprocess.call(command, shell=True)
    else:
        print(f"Screen rotation not supported on {system}.")


#Function to read a log file with the name of the video that should transmitte
def whichVideo():
    try:
        with open("videoToRead","r") as f:
            return f.read()
    except Exception as e:
        return "default.mp4"
# Function to play video from SFTP server using VLC
def play_video_from_sftp(sftp_user, sftp_host, video_path, sftp_port, password):
    print(whichVideo())
    vlc_command = f'vlc --fullscreen sftp://{sftp_user}:{password}@{sftp_host}:{sftp_port}/videos/{whichVideo()} :vout-filter=transform --video-filter --no-autoscale vlc://quit'
    #sudo apt-get install sshpass
    subprocess.run(vlc_command, shell=True)


def find_pid(process_name): 

    for proc in psutil.process_iter(['pid', 'name']): 
        if proc.info['name'] == process_name: 
            return proc.info['pid'] 

    return None

# Tkinter setup
root.attributes("-fullscreen", True)

# Get screen dimensions
screen_info = screeninfo.get_monitors()[0]
screen_width = screen_info.width
screen_height = screen_info.height

# Calculate portrait dimensions
portrait_width = int(screen_height * 2)
portrait_height = int(screen_width * 2)

# Calculate portrait position
portrait_x = (screen_width - portrait_width) // 2
portrait_y = (screen_height - portrait_height) // 2

# Background label for portrait image
background_label = tk.Label(root, bg='black')
background_label.place(x=portrait_x, y=portrait_y, width=portrait_width, height=portrait_height)

# Weather display label
weather_label = tk.Label(root, font=("Helvetica", 24), bg='white', fg='black', anchor='center')
weather_label.place(relx=0.5, rely=0.5, anchor='center')  # Place the label in the center

# Function to set background image
def set_background_image():
    # Tkinter setup
    image_url = fetch_random_image()
    if image_url:
        #rotate_screen(90)
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))

        # Resize and crop the image to maintain portrait aspect ratio
        image = image.resize((portrait_width, portrait_height))
        background_image = ImageTk.PhotoImage(image)
        background_label.config(image=background_image)
        background_label.image = background_image
    
    #rotate_screen(90)

def open_website():

    process = subprocess.Popen(["firefox", "-kiosk", URL_TO_DISPLAY])
    time.sleep(SECOND_TRANSITION) # Wait for 10 seconds
    process.terminate()
    #print("Destroing root process")
    #root.destroy()

import paho.mqtt.client as mqtt
import signal
from mqttController import MQTTClient

dev = {
    "hostname" : SFTP_HOST,
    "port" : 2222,
    "wbport" : 2225,
    "ALLOWED_EXTENSIONS" : ['mp4','jpg','png'],
    "VIDEOS_PATH" : "../videos"
}
prod = {
    "hostname" : "iot_docker-mosquitto-mqtt-1",
    "port" : 1883,
    "wbport" : 9006,
    "ALLOWED_EXTENSIONS" : ['mp4'],
    "VIDEOS_PATH" : "../videos"
}

ALLOWED_EXTENSIONS = dev["ALLOWED_EXTENSIONS"]
VIDEOS_PATH = dev["VIDEOS_PATH"]


ListenerMQTT = MQTTClient.getMQTTClient(name="raspberrypi1",hostname=dev["hostname"], port=dev["port"], subscribeList=["raspberrypi1", "raspberrypi2", "raspberrypi3"])
t1 = threading.Thread(target=ListenerMQTT.getClient().loop_start)

#function to terminated when ctrl + c is pressed
def terminateThread(signum, frame):
    print("CTRL + C")
    ListenerMQTT.getMQTTClient().bSendStatus = False
    ListenerMQTT.getClient().disconnect()
    ListenerMQTT.getClient().loop_stop(force=True)
    raise KeyboardInterrupt


if __name__ == "__main__":
        signal.signal(signal.SIGINT, terminateThread)
        t1.start()
        update_and_switch()
        
        # Main loop to display the weather continuously
        root.mainloop()

        #while True:
        #    select_random_video()
