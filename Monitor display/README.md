Monitor Display Project
=======================

The Monitor Display project is a Python-based application designed to display weather information and play videos on a monitor screen. It provides a dynamic and engaging display that combines weather data with video content.

Features
--------

*   **Weather Display**: The application fetches weather data from the WeatherAPI and displays information such as temperature, condition, humidity, and wind speed. This feature allows users to stay informed about the current weather conditions.
    
*   **Background Image**: The application fetches a random image related to the specified location from the Pexels API and sets it as the background image. This creates an attractive and visually appealing display.
    
*   **Video Playback**: The application can play videos stored on a remote server using the SFTP protocol. It randomly selects a video file from the specified directory and plays it using VLC player. This feature enables users to showcase promotional videos or other relevant content.
    
*   **Website Display**: The application can open a specified website in a web browser for a predefined duration. This feature allows users to display website content or advertisements during the specified time period.
    

Requirements
------------

To run the Monitor Display application, you need the following:

*   **Python 3.x**: The application is built using Python, so make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/)
    
*   **Python Dependencies**: The application relies on several Python libraries. You can install them by running the following command:
    
    Copy code
    
    `pip install -r requirements.txt`
    
*   **WeatherAPI key**: The application uses the WeatherAPI to fetch weather data. You need to sign up for an API key at [WeatherAPI](https://www.weatherapi.com/). Once you have the key, update the `API_KEY` variable in the `status_checker.py` file with your own API key.
    
*   **Pexels API key**: The application fetches background images from the Pexels API. You can obtain a free API key by creating an account at [Pexels API](https://www.pexels.com/api/new/). Update the `PEXELS_API_KEY` variable in the `status_checker.py` file with your API key.
    
*   **SFTP server**: If you want to play videos from a remote server, make sure you have access to an SFTP server. Update the `SFTP_HOST`, `SFTP_USERNAME`, `SFTP_PASSWORD`, and `VIDEO_DIRECTORY` variables in the `status_checker.py` file with the appropriate server details and video directory path.
    

Project Files and Folders
-------------------------

The project repository consists of the following files and folders:

*   `status_checker.py`: The main script that runs the Monitor Display application. It contains the logic for fetching weather data, displaying information, setting background images, playing videos, and opening websites.
    
*   `requirements.txt`: A text file that lists the Python dependencies required by the application. You can install them using the `pip` command as mentioned earlier.
    
*   `README.md`: This markdown file provides an overview of the project, its features, requirements, and usage instructions.
    
*   `images/`: A folder that contains sample background images used by the application. You can replace these images with your own collection or let the application fetch images from the Pexels API.
    
*   `videos/`: A folder where you can store video files to be played by the application. If you are using a remote server, make sure the videos are uploaded to the appropriate directory and update the `VIDEO_DIRECTORY` variable accordingly.
    

Make sure to organize the project files and folders appropriately and update the necessary variables with your own API keys, server details, and file paths before running the application.

How to Use
----------

To use the Monitor Display application, follow the instructions below. Make sure you have fulfilled the requirements mentioned above.

1.  Clone or download the project repository to your local machine.
    
2.  Open the terminal or command prompt and navigate to the project directory.
    
3.  Run the following command to install the required Python dependencies:
    
    Copy code
    
    `pip install -r requirements.txt`
    
4.  Open the `status_checker.py` file and update the variables mentioned in the requirements section (API keys, server details, etc.) according to your setup.
    
5.  Save the changes and run the following command to start the application:
    
    Copy code
    
    `python status_checker.py`
    
6.  The application will display the weather information and set a background image based on the fetched data.
    
7.  After a specified time interval (defined in the `FIRST_TRANSITION` variable), the application will switch to video playback mode. It will randomly select a video file from the specified directory (either local or remote) and play it using VLC player.
    
8.  Simultaneously, the application will open a web browser and display the specified website for a predefined duration (defined in the `SECOND_TRANSITION` variable).
    
9.  Once the video and website display are complete, the application will loop back to displaying weather information and continue the cycle.
    
10.  To exit the application, close the terminal or command prompt window.
    

Please note that the application is designed to run on a monitor screen and requires an internet connection for fetching weather data and images, as well as for playing videos from a remote server.

Feel free to customize the application by modifying the API keys, location, video directory, and other variables according to your requirements.

Enjoy using the Monitor Display application to create an interactive and informative display on your monitor!