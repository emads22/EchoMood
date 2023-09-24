
const src_base = "https://drive.google.com/uc?id="
var currentSourceIndex = 0;
var sources = [];



document.addEventListener("DOMContentLoaded", function() {

    handleMoodSelectDiv();
    handleTracksDiv();
    handlePlayerDiv();
    
})



function handleMoodSelectDiv() {
    const moodDiv = document.getElementById("mood-div");
    // access the 'data-mood-select' attribute (JavaScript converts the hyphenated attribute names to camelCase when accessing them through the 
    // dataset object so 'mood-select' is now 'moodSelect' )
    const moodSelection = moodDiv.dataset.moodSelect;
    if (moodSelection === "True") {
        moodDiv.style.display = "block";
    } else {
        moodDiv.style.display = "none";
    }
}



function handleTracksDiv() {
    const tracksDiv = document.getElementById("tracks-div");
    // access the 'data-mood-select' attribute (JavaScript converts the hyphenated attribute names to camelCase when accessing them through the 
    // dataset object so 'mood-select' is now 'moodSelect' )
    const tracksPlayable = tracksDiv.dataset.playable;
    if (tracksPlayable === "True") {
        tracksDiv.style.display = "block";
    } else {
        tracksDiv.style.display = "none";
    }
}



function handlePlayerDiv() {
    const playerDiv = document.getElementById("player-div");
    // access the 'data-playable' attribute
    const playableValue = playerDiv.dataset.playable;
    if (playableValue === "True") {
        playerDiv.style.display = "block";
    } 
    // when 'playlist_tracks' var is available and defined
    if (typeof playlist_tracks !== "undefined") {
        playlist_tracks.forEach(element => {
            // create a list of dict (objects) for each track in 'playlist_tracks' object
            sources.push({
                id: element.fields.gdrive_id,
                title: element.fields.title,
                artist: element.fields.artist,
                genre: element.fields.genre
            });
        })
        musicPlayer(sources);
    } else {
        console.log("No Tracks Available");
    }
}



function musicPlayer(sources) {    
    const player = document.getElementById("musicPlayer");
    const title = document.getElementById("trackTitle");
    const loop = document.getElementById("checkLoop");    
    const playAllButton = document.getElementById("playAll");
    const pauseAllButton = document.getElementById("pauseAll");
    const stopPlayerButton = document.getElementById("stopPlayer");
    const playNextButton = document.getElementById("playNext");
    const playPreviousButton = document.getElementById("playPrevious");

    // set the initial volume when the audio element loads (0.2 represents 20% volume)
    player.volume = 0.2; 
    // set the src for the music layer (1st track)
    player.src = `${src_base}${sources[currentSourceIndex].id}`;
    // load src of player
    player.load();

    playAllButton.addEventListener("click", () => {
        player.play();
    })

    pauseAllButton.addEventListener("click", () => {
        player.pause();
    })

    stopPlayerButton.addEventListener("click", () => {
        stopPlayer(player);
    })

    playNextButton.addEventListener("click", () => {
        playNext(player, title, loop, sources);
    })

    playPreviousButton.addEventListener("click", () => {
        playPrevious(player, title, sources);
    })

    // Add an event listener to handle errors
    player.addEventListener('error', () => {
        const errorCode = player.error.code;
        let errorMessage = '';

        switch (errorCode) {
            case MediaError.MEDIA_ERR_ABORTED:
                errorMessage = `The fetching process for the media resource was aborted.`;
                break;
            case MediaError.MEDIA_ERR_NETWORK:
                errorMessage = `A network error occurred while fetching the media resource.`;
                break;
            case MediaError.MEDIA_ERR_DECODE:
                errorMessage = `The media resource couldn't be decoded.`;
                break;
            case MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED:
                errorMessage = `The media resource format is not supported.`;
                break;
            default:
                errorMessage = `An unknown error occurred.`;
        }
        // handle the error and display a message on the console
        console.error(`Audio error: ${errorMessage}`);
        // another handling of error which is signaling user that theres an error of loading media
        title.textContent = "Error Loading Media";
    });
    
    // add an event listener for the "play" event in order to highlight the track that is being played
    player.addEventListener("play", () => {
        // this function will be called when the audio starts or resumes playing
        highlightTrack(sources);
        title.textContent = `${sources[currentSourceIndex].title}`;
    })

    player.addEventListener("ended", () => {
        playNext(player, title, loop, sources);
    }) 

    // select all <button> elements with class "track"
    const trackButtons = document.querySelectorAll("button.track");

    trackButtons.forEach(function(button) {         
        button.addEventListener("dblclick", function() {
            // if '() =>' is used instead of 'function()', current event target 'this' wont be accessible
            playClickedTrack(player, this, title, sources);
        })
    })
}

    

function playNext(player, title, loop, sources) {    
    // even if index is the end of the playlist, using modulo '%' will return index to the start (0)
    currentSourceIndex = (currentSourceIndex + 1) % sources.length;
    player.src = `${src_base}${sources[currentSourceIndex].id}`;
    // load new src of player 
    player.load();
    
    // in case index returned to start (0) and loop isnt checked then end of playlist is reached and player must stop without looping
    if (!loop.checked && currentSourceIndex === 0) {
        console.log("end of playlist");
    // otherwise keep playing the music playlist from the starting track cz loop is checked
    } else {
        title.textContent = `${sources[currentSourceIndex].title}`;
        player.play(); 
    }
}



function playPrevious(player, title, sources) {    
    // if index gets to 0 (start of playlist) it will remain at 0 without going negative
    currentSourceIndex = (currentSourceIndex === 0) ? 0 : (currentSourceIndex - 1) % sources.length;
    player.src = `${src_base}${sources[currentSourceIndex].id}`;
    // load new src of player 
    player.load();
    title.textContent = `${sources[currentSourceIndex].title}`;    
    player.play();
}



function stopPlayer(player) {
    // reset playback position
    // player.currentTime = 0; 
    // load to reset the element's state which is the start of song (current time is 0)
    player.load(); 
}



function playClickedTrack(player, element, title, sources) {
    // store the clicked button ID in a variable
    const clickedButtonId = element.id;
    // the 'Array.findIndex()' method is called on 'sources', it takes a function as an argument, and this function is executed for each 
    // element in the array. it returns the index of the first element that satisfies the condition of having an id property equal to 
    // 'this.id'. if no such element is found, it returns -1
    currentSourceIndex = sources.findIndex(function(track) {
        return track.id === clickedButtonId;
    })
    
    if (currentSourceIndex !== -1) {
        // update the player source and title for the current playing track
        player.src = `${src_base}${sources[currentSourceIndex].id}`;
        title.textContent = `${sources[currentSourceIndex].title}`;
        // load and play the audio track
        player.load();
        player.play(); 
    } else {
        console.log("Track source not found in sources array.");
        title.textContent = "Error Loading Media";
    }
}



function highlightTrack(sources) {
    const playlistTracks = document.querySelectorAll(".track");
    playlistTracks.forEach((playlistTrack) => {
        if (playlistTrack.id === sources[currentSourceIndex].id) {
            // add the highlighted class to this track
            playlistTrack.classList.add("highlighted");
        } else {
            // check if 'highlighted' class exists in this track's classList in order to remove it
            if (playlistTrack.classList.contains('highlighted')) {
                // remove a class from this track
                playlistTrack.classList.remove("highlighted");
            }
        }
    }) 
}



function openPlaylist() {
    console.log("OPEN PLAYLIST");

    const allPlaylists = document.getElementById("playlists-div");
    const thisPlaylist = document.getElementById("open-playlist-div");

    allPlaylists.style.display = "none";
    thisPlaylist.style.display = "block";
}



// const sources = [
//     "1dS9V_4mPfOnm0SMzdLqHjIDaLNOBKSO0",
//     "1aDd5FTDAoKqXHwqrb0XpyA1F-qUTPJta",
//     "1YisZ5e8B5K_ocIBiGk7Wz-iTUuLpMnUk",
//     "1KipsIxQu9tvwcbmytGFcvdKPr7gOa-0h",
//     "1nto-03CIGSk5zqB8pElY_rgBr2GMuiB1",
//     "1g4xbf6E93WM71-guvglLI-j7oaDlCeBP",
//     "1xGZpoQD-Sl6fukZXUtRWUc8HBmpcdJ8w",
// ]





// function handleLandingTrack() {
//     const landingTrack = document.getElementById("musicPlayer");
//     // set the initial volume when the audio element loads (0.2 represents 20% volume)
//     landingTrack.volume = 0.2;  
//     // on the first interaction from user (any mouse click) start playing landing track
//     // document.addEventListener("click", () => {
//     //     landingTrack.play();
//     // })
//     // restart the audio when it ends
//     landingTrack.addEventListener("ended", () => {
//         // reset the audio to the beginning
//         landingTrack.currentTime = 0; 
//         landingTrack.play();
//     })
// }