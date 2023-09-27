
const src_base = "https://drive.google.com/uc?id="
var currentSourceIndex = 0;
var sources = [];



document.addEventListener("DOMContentLoaded", function() {
    handleDivs(); 
})



function handleDivs() {
    // when 'playlist_tracks' var from 'index' template is available and defined
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
        handleTracksDiv();
        musicPlayer(sources);
    } else if (typeof this_playlist_tracks !== "undefined") {
        // here 'this_playlist_tracks' var from 'playlists' template is available and defined
        this_playlist_tracks.forEach(element => {
            // create a list of dict (objects) for each track in 'playlist_tracks' object
            sources.push({
                id: element.fields.gdrive_id,
                title: element.fields.title,
                artist: element.fields.artist,
                genre: element.fields.genre
            });
        })
        handlePlaylistsDiv();
        musicPlayer(sources);
    } else {
        console.log("No Tracks Available");
    }
}



function handleTracksDiv() {
    const tracksDiv = document.getElementById("tracks-div");
    const moodDiv = document.getElementById("mood-div");
    // access the 'data-playable' attribute 
    const tracksPlayable = tracksDiv.dataset.playable;
    if (tracksPlayable === "True") {
        tracksDiv.style.display = "block";
        moodDiv.style.display = "none";
    } else {
        tracksDiv.style.display = "none";
        moodDiv.style.display = "block";
    }
}



function handlePlaylistsDiv() {
    const tracksDiv = document.getElementById("tracks-div");
    const playlistsDiv = document.getElementById("playlists-div");
    // access the 'data-playable' attribute 
    const tracksPlayable = tracksDiv.dataset.playable;
    if (tracksPlayable === "True") {
        tracksDiv.style.display = "block";
        playlistsDiv.style.display = "none";
    } else {
        tracksDiv.style.display = "none";
        playlistsDiv.style.display = "block";
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
        title.textContent = "Failed to Load Media";
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
