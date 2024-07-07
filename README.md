# Update: EchoMood

![EchoMood_logo](./capstone/static/capstone/assets/logo/EchoMood_logo.png)

## Overview:
In today's fast-paced world, music has become an integral part of our lives, influencing our moods, emotions, and even productivity.
We often find ourselves searching for the perfect playlist that resonates with our current feelings or activities.
EchoMood, The Mood-Based Music Companion, is a web application designed to solve this problem by offering a personalized and dynamic music experience tailored to the mood.

---

## Update
This version represents an updated iteration of the original **`EchoMood`** app developed during my [**CS50W**](https://cs50.harvard.edu/web/2020/) **`Final Project`** in 2023. You can explore its development on [me/50](https://github.com/me50/emads22) repository.

### Key Enhancements:
- **Improved Music Streaming**: Removed reliance on Google Drive APIs, now storing tracks locally for enhanced performance.
- **Optimized User Experience**: Refined styles, improved logic, and enhanced functionality throughout the application.

---

Enjoy the updated EchoMood experience, tailored to provide the best music companion service possible.

## Features
- **Creating the Perfect Playlist**: Generate music playlists based on the user's mood input, curating a unique 16-track playlist every time.
- **Diversity in Music Genres**: Ensures a diverse selection of music genres related to the chosen mood for a captivating listening experience.
- **Music Streaming Made Easy**: An interactive music player offering features such as play, stop, pause, play next, play previous, and loop.
- **Instant Gratification**: Allows users to double-click on any track in the playlist to instantly play it.
- **Customization and Variety**: Option to save generated playlists and regenerate them for the same mood, offering variety and spontaneity.
- **Managing Playlists**: Robust playlist management system where users can rename or delete playlists, ensuring a well-organized musical collection.
- **Smart Playlist Handling**: Prevents clutter and redundancy in saved playlists by ensuring each is unique.
- **Mobile Responsiveness**: Fully mobile responsive design for seamless music experience on any device.
- **Secure Authentication**: Implements a highly secure password pattern (e.g., abAB12!@) during user registration to enhance account security.

## Technologies Used
- **Django**: A high-level Python web framework for developing web applications.
- **re**: A module for regular expression operations.

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure the necessary parameters such as database settings and other configurations in `constants.py`.
   - Adjust any additional setup steps as necessary.
5. Run the Django development server using `python manage.py runserver`.

## Usage
1. Run the Django development server using `python manage.py runserver`.
2. Access the web app through your browser at `http://127.0.0.1:8000/`.
3. Log in or create an account to start generating mood-based playlists.
4. Explore, interact with, and enjoy the personalized music experience.

## Example
#### John's User Profile:
- **Username**: `john`
- **Password**: `abAB12!@` (utilizing **`EchoMood`**'s highly secure password pattern)

John enjoys a personalized music experience with EchoMood, exploring various moods and enjoying curated playlists tailored to his preferences. You can view his playlists in the `Playlists` section on `http://127.0.0.1:8000/playlists`.

## Update
This update improves EchoMood by:
- Dropping the use of Google Drive APIs for music streaming.
- Storing tracks directly in a local directory within the server, eliminating the reliance on network connections and fetching requests.
- Optimizing the app for better performance.
- Making style adjustments and refactoring logic and functions for a smoother user experience.

In conclusion, EchoMood continues to be your go-to destination for personalized music, now with enhanced performance and user experience. Enjoy your mood-based playlists seamlessly and securely!

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.