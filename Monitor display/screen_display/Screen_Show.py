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
import paramiko

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

SFTP_HOST = "192.168.1.128"
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
    play_video_from_sftp(SFTP_USER, SFTP_HOST, select_random_video(), SFTP_PORT,SFTP_PASSWORD) #change the video path
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

# Function to play video from SFTP server using VLC
def play_video_from_sftp(sftp_user, sftp_host, video_path, sftp_port, password):
    vlc_command = f'vlc --fullscreen sftp://{sftp_user}:{sftp_port}@{sftp_host}/{video_path} :vout-filter=transform --video-filter --no-autoscale vlc://quit'
    #sudo apt-get install sshpass
    subprocess.run(vlc_command, shell=True)

def select_random_video():

    # SFTP connection details
    hostname = SFTP_HOST
    port = 2223
    username = SFTP_USER
    password = SFTP_PASSWORD
    remote_folder = '/home/'+SFTP_USER+'/video/'

    # Establish an SFTP connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    sftp = ssh.open_sftp()

    # Get a list of all files in the remote folder
    file_list = sftp.listdir(remote_folder)

    # Filter the list to only include video files with .mp4 extension
    video_files = [file for file in file_list if file.lower().endswith('.mp4')]

    # Randomly select a video file
    selected_file = random.choice(video_files)
    selected_file = str(remote_folder + selected_file)

    # Close the SFTP connection
    sftp.close()
    ssh.close()

    print(f"Selected file '{selected_file}'.")

    return selected_file

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

    process = subprocess.Popen(["firefox", "--new-window", "-kiosk", URL_TO_DISPLAY])
    time.sleep(SECOND_TRANSITION) # Wait for 10 seconds
    process.terminate()

    #print("Destroing root process")
    #root.destroy()

if __name__ == "__main__":
        
        update_and_switch()
        # Main loop to display the weather continuously
        root.mainloop()

        #while True:
        #    select_random_video()
