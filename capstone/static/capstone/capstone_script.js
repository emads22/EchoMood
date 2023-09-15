
const src_base = "https://drive.google.com/uc?id="
var currentSourceIndex = 0;
var sources = [];


document.addEventListener("DOMContentLoaded", function() {
    // console.log("ECHOMOOD");

    // when 'all_tracks' var is available and defined
    if (typeof all_tracks !== "undefined") {
        all_tracks.forEach(element => {
            // create a list of dict (objects) for each track in 'all_tracks' object
            sources.push({
                id: element.fields.gdrive_id,
                title: element.fields.title,
                artist: element.fields.artist,
                genre: element.fields.genre
            });
        })
        musicPlayer(sources);
    }
})



function musicPlayer(sources) {
    
    const player = document.getElementById("player");
    const title = document.getElementById("trackTitle");
    const loop = document.getElementById("checkLoop");
    
    const playAllButton = document.getElementById("playAll");
    const pauseAllButton = document.getElementById("pauseAll");
    const stopPlayerButton = document.getElementById("stopPlayer");
    const playNextButton = document.getElementById("playNext");
    const playPreviousButton = document.getElementById("playPrevious");

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

    player.addEventListener("ended", () => {
        playNext(player, title, loop, sources);
    }) 

    // add an event listener for the "play" event
    player.addEventListener("play", () => {
        // this function will be called when the audio starts or resumes playing
        highlightTrack(player, sources);
    })

    // select all <button> elements with class "track"
    const trackButtons = document.querySelectorAll("button.track");

    trackButtons.forEach(function(button) {         
        button.addEventListener("dblclick", function() {
            // if '() =>' is used instead of 'function()', current event target 'this' wont be accessible
            playClickedTrack(this, title, sources);
        })
    })
}

    
function stopPlayer(player) {
    // reset playback position
    player.currentTime = 0; 
    // load to reset the element's state which is the start of song (current time is 0)
    player.load(); 
}
    

function playNext(player, title, loop, sources) {    
    // even if index is the end of the playlist, using modulo '%' will return index to the start (0)
    currentSourceIndex = (currentSourceIndex + 1) % sources.length;
    // currentSourceIndex ++;
    player.src = `${src_base}${sources[currentSourceIndex].id}`;
    
    // in case index returned to start (0) and loop isnt checked then end of playlist is reached and player must stop without looping
    if (!loop.checked && currentSourceIndex === 0) {
        console.log("end of playlist");
        // load to reset the element's state 
        player.load(); 
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
    title.textContent = `${sources[currentSourceIndex].title}`;
    player.play();
}


function playClickedTrack(element, title, sources) {
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
        // play the audio track
        player.play(); 
    } else {
        console.log("Track source not found in sources array.");
    }
}


function highlightTrack(player, sources) {
    // console.log(sources[currentSourceIndex].title);
    thisTrack = document.getElementById(sources[currentSourceIndex].id);
    playlistTracks = document.querySelectorAll(".track");
    playlistTracks.forEach((track) => {
        if (track.id === sources[currentSourceIndex].id) {
            // console.log("Found it: ", sources[currentSourceIndex].title);
            // add the highlighted class to this track
            track.classList.add("highlighted");
        } else {
            // console.log("Not found it: ");
            // check if 'highlighted' class exists in this track's classList in order to remove it
            if (track.classList.contains('highlighted')) {
                // remove a class from this track
                track.classList.remove("highlighted");
            }
        }
    })
    
    

    

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