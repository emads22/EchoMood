
<div style="display: flex; align-items: center;">
  <img src="./capstone/static/capstone/assets/logo/EchoMood.png" alt="EchoMood Logo" style="width: 30%; height: auto; margin-right: 40px; margin-bottom: 20px;" />
  <div>
    <h1>EchoMood</h1>
    <h2>Description:</h2>
    <h3>
      In today's fast-paced world, music has become an integral part of our lives, influencing our moods, emotions, and even productivity.<br>
      We often find ourselves searching for the perfect playlist that resonates with our current feelings or activities.<br> 
      EchoMood, The Mood-Based Music Companion, is a web application designed to solve this problem by offering a personalized and dynamic music experience tailored to the mood.
    </h3>
    <h3>Video Demo: &lt;Insert video link here&gt;</h3>
  </div>
</div>
    

## Distinctiveness and Complexity:  

EchoMood's distinctiveness lies in its innovative use of Google Drive APIs, a complex synchronization system, and stringent password requirements, all aimed at providing users with a superior and secure music experience.

### 1. Leveraging Google Drive APIs for Music Streaming
 
Unlike most music streaming services that store audio files directly on their servers, EchoMood takes a more efficient and pro-active approach. It utilizes Google Drive APIs to fetch music tracks stored in the user's Google Drive, thus eliminating the need for massive server storage for audio files. This results in a significant reduction in storage requirements while allowing EchoMood to provide a vast library of royalty-free music sourced freely from&nbsp;&nbsp;[Free Music Archive](https://freemusicarchive.org/)&nbsp;&nbsp;and&nbsp;&nbsp;[YouTube Audio Library](https://studio.youtube.com/channel/) .

### 2. The Complexity of Secure Google Drive Integration

EchoMood's ability to seamlessly access and stream music from Google Drive is not a simple feat. It involves a complex set of operations to ensure the security and privacy of both the user's Google Drive account and the EchoMood platform. The application employs robust authentication mechanisms and carefully follows Google's security measures to access and fetch tracks from Google Drive. This complexity in integration ensures that user data remains protected while enjoying the convenience of accessing their music library.

### 3. Real-Time Synchronization for Fresh Content

To enhance user experience and keep the music library up-to-date, EchoMood employs a sophisticated synchronization system. Frequently, upon visiting the homepage, the application checks if the user's session has expired. If it detects that the session has expired (by examining the existence of a specific marker in the session), EchoMood re-establishes a connection with Google Drive to read the latest music tracks and sync their metadata with the database on the app server. This dynamic approach ensures that users always have access to the most recent music additions.

### 4. Enhancing Security with Complex Password Requirements

EchoMood goes beyond the standard password requirements to strengthen the security of user accounts. During the registration process, EchoMood enforces stringent password criteria. Each password must contain at least two uppercase letters, two digits, and two special characters. Moreover, it must be within a specific length range of 6 to 8 characters. This heightened level of password complexity strengthens user authentication and safeguards their accounts from unauthorized access.

In summary, EchoMood's distinctiveness and complexity stem from its unique approach to music storage and retrieval, intricate Google Drive integration, real-time synchronization capabilities, and stringent password security measures. These innovative features not only make EchoMood a standout music streaming platform but also ensure a secure and dynamic user experience. EchoMood sets a new standard in music streaming by combining convenience, efficiency, and security in an elegant and user-friendly package.


## EchoMood's Features:

### 1. Creating the Perfect Playlist 

EchoMood's primary function is to generate music playlists based on the user's mood input. 
It understands that music can convey a wide range of emotions and vibes, and taps into this knowledge to curate a unique playlist every time he visits the platform.

Upon logging in to EchoMood, users are greeted by an intuitive and user-friendly interface. 
To get started, users simply enter their current mood into the designated field. 
Whether they're feeling happy, melancholic, pumped up, or relaxed, EchoMood has got them covered. 
The application uses a vast music library to curate a playlist comprising 16 tracks, each carefully selected to resonate with their chosen mood.
        
### 2. Diversity in Music Genres 

EchoMood goes the extra mile by ensuring that a playlist isn't monotonous. 
It curates a 16-track playlist with a diverse selection of music genres related to the chosen mood, ensuring that users receive a diverse and captivating listening experience.
For instance, if they select "energetic," they may get a mix of rock, pop, and electronic tracks that match their desired energy level.
The user-friendly interface allows users to explore, interact, and enjoy their music seamlessly.
        
### 3. Music Streaming Made Easy

EchoMood takes music streaming to the next level. 
With the click of a button, users can begin streaming the 16-track playlist online. 
The music player boasts a unique and interactive interface, offering features such as play, stop, pause, play next, play previous, and loop. 
It's all at their fingertips, enhancing their control over the music.
        
### 4. Instant Gratification

For those who can't wait, EchoMood offers the convenience of double-clicking on any track in the playlist. 
This feature allows them to instantly play a specific track without waiting for it to follow the order. 
Users musical desires are prioritized.

### 5. Customization and Variety

EchoMood doesn't stop at just one playlist. 
Users have the option to save the generated playlist, ensuring that the perfect soundtrack is always within reach. 
Even better, if the mood strikes for something different, EchoMood allows them to regenerate a playlist for the same mood, offering variety and spontaneity.

### 6. Managing Playlists

EchoMood doesn't just stop at generating playlists; it also provides a robust playlist management system. 
All of the saved playlists are neatly organized in the "Playlists" page. 
Here, they can view all the playlists they've saved, each neatly organized by mood.
EchoMood gives them the power to rename or delete playlists at their discretion, giving them full control over their musical collection, and ensuring that it stays organized and tailored to their preferences.

### 7. Smart Playlist Handling

EchoMood is designed to prevent clutter and redundancy in the saved playlists. 
To maintain the integrity of the saved playlists, the application won't allow users to save a playlist if all 16 tracks already exist in one of their saved playlists, regardless of their order. 
This feature ensures that each saved playlist is unique and tailored to their mood at the time offering a distinctive listening experience.

Additionally, EchoMood is intelligent enough to handle playlist naming conflicts. 
If a user tries to save a new playlist with a name that already exists for another saved playlist, EchoMood automatically appends a number to the name to make it distinct. 
For example, if a playlist named "Chill Vibes", the new playlist will be named "Chill Vibes_1."

### 8. Mobile Responsiveness

EchoMood understands the importance of music on the go.
To cater to users on all devices, the web app is designed to be fully mobile responsive. 
Whether using a smartphone, tablet, or desktop computer, EchoMood adapts seamlessly to any screen size, ensuring that users can enjoy their mood-based playlists no matter where they are.


In conclusion, EchoMood is a personalized music companion, designed to enhance the music-listening experience for every user. 
Whether he is in need of a pick-me-up playlist for a rainy day or a relaxing selection for winding down, EchoMood is his go-to destination.
With its mood-based playlist generation, interactive music player, playlist management tools, and mobile responsiveness, EchoMood is set to redefine how he connects with music. 
The web application continues to evolve and grow, continuously expanding its music library and refining its algorithms to ensure that every playlist generated is nothing short of perfect for each user's mood.
Here are some exciting ideas for upgrades and improvements:

- User-Generated Playlists: Empower users to create their personalized playlists from the tracks available for the current mood. 
                            This feature allows users to curate their music collections, adding a personal touch to their listening experience.

- Dynamic Webpage Animations:   Integrate JavaScript to add dynamic animations and designs to the webpage, enhancing the visual 
                                appeal and interactivity of the application. Visual effects synchronized with music playback can create a captivating and immersive experience.

- Track Uploads:    Enable users to contribute to the music repertoire by allowing them to upload their tracks. 
                    This user-generated content can diversify the music selection.

- Offline Mode: Develop an offline mode that allows users to download playlists for offline listening, 
                catering to users who may not always have internet connectivity.

- Enhanced User Feedback: Implement a feedback system that encourages users to rate and review playlists. 


## Contents of the Files:

### 1. assets directory contains:
- EchoMood Logo image
- All the icons used on the application webpages whether for buttons or designs sourced freely from [Flaticon](https://www.flaticon.com/)


### 2. layout.html file contains:
- Meta Information: Contains meta tags for character encoding and viewport settings.
- Title: Sets the webpage's title, which can be customized in individual pages using blocks.
- Bootstrap: Links to Bootstrap CSS and JavaScript for responsive design and styling.
- Favicon: Includes a transparent image as a favicon to prevent browser requests for the favicon.ico file.
- Stylesheet and JavaScript: Links to custom styles and a JavaScript file for additional functionality.
- Navigation Bar: Defines a responsive navigation bar with links to home, login, and registration pages when the user is not authenticated. 
  When authenticated, it provides links to playlists and the user's username with a dropdown menu for logging out.
- Content Area: Contains a content block where individual page content is inserted using blocks.
- Footer: Displays a copyright notice for EchoMood.
- Bootstrap JavaScript: Includes Bootstrap JavaScript for enhanced functionality.

### 3. index.html file contains:
- Parsing JSON data for playlist tracks.
- Displaying messages and automatic page refresh.
- EchoMood logo.
- List of tracks with details.
- Option to save and regenerate playlists.
- Player controls for streaming tracks with loop functionality.

### 4. login.html file contains:
- Extends the 'capstone/layout.html' template.
- Loads static files.
- Displays warning messages, if any, in an alert box.
- Redirects to the login page after 1 second if there are messages.
- Contains a header, logo, and a login form.
- Form includes fields for username and password.
- Provides a "Log In" button.
- Offers a link to the registration page for new users.


### 5. register.html file contains:
- Extends the 'capstone/layout.html' template.
- Loads static files.
- Displays warning messages if any.
- Refreshes the page after 20 seconds if messages are present.
- Presents a logo and a brief description.
- Provides a registration form for users.
- Collects user data such as username, email, password, and password confirmation.
- Includes a "Register" button to submit the form.
- Offers a link to the login page for users who already have an account.

### 6. playlists.html file contains:
- Layout Inheritance: The HTML file extends a layout template ('capstone/layout.html').
- Loading Static Resources: It loads static resources using {% load static %}.
- Alert Messages: The file checks for alert messages and displays them if present, including a refresh meta tag.
- EchoMood Logo: It displays the EchoMood logo using an image sourced from static files.
- User Playlists: User's playlists are displayed, with options to rename and delete each playlist.
- Playlist Content: Each playlist's name, tracks, and creation date are shown.
- Playlist Interaction: Users can rename or delete playlists with modals for each action.
- Tracks Display: Within a playlist, the tracks are listed, and each track has an option to play.
- Audio Player: An audio player allows users to play tracks and includes play, pause, stop, previous, and next buttons.
- Looping Option: Users can enable loop playback for tracks.
- Mobile Responsiveness: The layout adjusts for different screen sizes.
- JavaScript Integration: JavaScript code is included for playlist functionality, and playlist data is passed from the backend.
- No Playlists Message: If the user has no playlists, a message is displayed.
- No Tracks Message: If a playlist has no tracks, a message is displayed.

### 7. capstone_script.js file contains:
- The script defines the 'src_base' variable for the base URL to access music tracks on Google Drive.
- It initializes variables such as 'currentSourceIndex' and an empty array 'sources'.
- The 'DOMContentLoaded' event listener calls the 'handleDivs' function when the page content is loaded.
- The 'handleDivs' function checks if the 'playlist_tracks' or 'this_playlist_tracks' variables are defined, 
  creates a list of dictionaries (objects) for each track, and sets up the user interface accordingly.
- Depending on the availability of tracks, it either displays a list of tracks or mood-related content.
- The script contains functions like 'handleTracksDiv' and 'handlePlaylistsDiv' to toggle between displaying tracks and playlists based on user interaction.
- The 'musicPlayer' function sets up the music player interface, including play, pause, stop, next, and previous buttons, and handles track-related events.
- The 'playNext', 'playPrevious', and other functions manage the playback of music tracks, handle errors, and highlight the currently playing track.

### 8. styles.css file contains:
- HTML Elements:
    - Styles for the 'body' element, setting background and text colors.
    - Styling for 'audio' elements and customizing the appearance of the play button.
    - Styling for links with class 'login-link.'
    - Hover effects for links with class 'dropdown-item' and buttons with class 'track.'
    - Styling for buttons with class 'highlighted.'
    - Styles for ordered lists with class 'form-control.'
    - Styles for links with class 'btn-link' and 'cite' within them.

- IDs:
    - Styles for elements with the 'player-div' ID, including background and border properties.
    - Styles for elements with the 'musicPlayer' ID, including border properties and hover effect.
    - Styles for elements with the 'media-btns' ID, including border properties.
    - Hover effect styles for elements with the 'trackTitle' and 'loop' IDs.

- Classes:
    - Background color styles for elements with classes 'bg-navbar,' 'dropdown-menu,' and 'track.'
    - Styles for 'container-fluid' class.
    - Margin and width styles for elements with classes 'home-icon' and 'small-logo.'
    - Button styles for elements with class 'btn-green.'
    - Hover effects for buttons, form-selects, and card titles.
    - Styles for alerts with class 'alert-warning.'
    - Margin style for elements with class 'content.'
    - Border and font styles for elements with class 'track.'
    - Width style for elements with class 'mood-form.'
    - Font and color styles for elements with class 'playlist.'
    - Styles for elements with class 'sound.'
    - Background and border-color styles for form-check-input elements.
    - Background color styles for form-select elements.
    - Styles for modal-header, modal-body, and modal-footer.
    - Border and background styles for elements with class 'card,' 'card-title,' 'card-body,' and 'card-footer.'
    - Width and background color styles for elements with class 'btn-card.'
    - Hover effect styles for elements with class 'btn-card' and 'card-track.'
    - Styles for elements with class 'no-playlists' and its hover effect.

### 9. admin.py file contains:
- Imports modules from Django's admin package.
- Registers models for User, Mood, Genre, Track, and Playlist in the Django admin interface.

### 10. models.py file contains:
- Defines a custom user model named 'User' inheriting from 'AbstractUser.'
- Includes a 'playlists' field in the 'User' model, establishing a Many-to-Many relationship with the 'Playlist' model.
- Defines a 'Genre' model with a 'name' field, allowing for unique genre names.
- Defines a 'Mood' model with a 'name' field and a Many-to-Many relationship with the 'Genre' model. 
  This model represents moods associated with various genres.
- Defines a 'Track' model with fields for 'title,' 'gdrive_id,' 'artist,' 'added_on,' and a Foreign Key relationship with 
  the 'Genre' model. The 'gdrive_id' field is unique.
- Defines a 'Playlist' model with fields for 'name,' 'created_on,' and a Many-to-Many relationship with the 'Track' model. 
  It also has a Foreign Key relationship with the 'Mood' model.
    
### 11. tools.py file contains:

- Imports various modules and libraries, including Google APIs, Django-related modules, and others.
- Defines a regular expression (PASSWORD_PATTERN) for validating password complexity during user registration.
- Sets a constant 'PLAYLIST_MAX_TRACKS' to limit the number of tracks in a playlist to 16.
- Functions and Their Purposes:
    - fetch_tracks_info(page_token=None): Retrieves file names and IDs from a specific Google Drive folder using the Drive v3 API, 
      with the ability to handle pagination.
    - sync_drive_db(drive_tracks): Synchronizes the application's database with the tracks from Google Drive, 
      adding new tracks and removing tracks that are no longer in Drive.
    - create_context(**kwargs): Creates a context template for views to avoid repetitive argument passing. 
      Sets default values for various template context variables.
    - create_playlist(mood): Generates a playlist by randomly selecting tracks associated with a given mood and shuffling them.
    - rename_playlist_numbered(playlist_name): Renames a playlist by incrementing a number if the name ends with a digit, otherwise appending "_1".
    - shuffle_list(this_list, num_shuffles): Recursively shuffles a list a specified number of times, ensuring a randomized order.

### 12. urls.py file contains:
- Defines URL patterns for various views in the Django web application.
- Includes paths for the homepage, login, logout, registration, mood-based playlist generation, playlist management, saving playlists, 
  opening playlists, renaming playlists, and deleting playlists.

### 13. views.py file contains:
- Imports various modules and classes from Django, including forms, authentication, database models, and HTTP-related components.
- Defines several Django forms used for user login, registration, mood selection, and playlist creation.
- Functions and Their Purposes:
    - index(request): Displays the homepage, generates mood-based playlists, and synchronizes music tracks with Google Drive.
    - login_view(request): Handles user login, authentication, and redirects to the homepage.
    - logout_view(request): Logs the user out and redirects to the login page.
    - register(request): Handles user registration, enforces password complexity rules, and logs in the user upon successful registration.
    - this_mood_playlist(request): Generates a mood-based playlist based on user-selected mood.
    - generate_playlist(request, mood): Generates a playlist for a specific mood and displays it.
    - playlists(request): Displays the user's playlists and provides options for renaming and deleting them.
    - save_playlist(request, playlist_mood): Saves a user-generated playlist and performs necessary checks to prevent duplicates.
    - open_playlist(request, playlist_id): Opens and displays a user's playlist for playback and management.
    - rename_playlist(request, playlist_id): Allows the user to rename a playlist.
    - delete_playlist(request, playlist_id): Deletes a user's playlist.