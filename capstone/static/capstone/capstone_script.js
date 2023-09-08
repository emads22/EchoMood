
const src_base = "https://drive.google.com/uc?id="
var currentSourceIndex = 0;
var sources = [];


document.addEventListener("DOMContentLoaded", function() {
    // console.log("ECHOMOOD");
    
    if (typeof all_tracks !== "undefined") {
        all_tracks.forEach(element => {
            // create a list of dict (objects) for each track in 'all_tracks' object
            sources.push({
                id: element.fields.gdrive_id,
                title: element.fields.title,
                artist: element.fields.artist,
                genre: element.fields.genre
            });

            musicPlayer(sources);
        })
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
    });

    pauseAllButton.addEventListener("click", () => {
        player.pause();
    });

    stopPlayerButton.addEventListener("click", () => {
        stopPlayer(player);
    })

    playNextButton.addEventListener("click", () => {
        playNext(player, title, loop, sources);
    });

    playPreviousButton.addEventListener("click", () => {
        playPrevious(player, title, sources);
    });

    player.addEventListener("ended", () => {
        playNext(player, title, loop, sources);
    });
}

    
function stopPlayer(player) {
    // reset playback position
    player.currentTime = 0; 
    // load to reset the element's state which is the start of song (current time is 0)
    player.load(); 
}
    

function playNext(player, title, loop, sources) {
    // even if index is the end of the playlist, using modulo '%' will return index to the start (0)
    // currentSourceIndex = (currentSourceIndex + 1) % sources.length;
    currentSourceIndex ++;
    player.src = `${src_base}${sources[currentSourceIndex].id}`;
    
    // in case index returned to start (0) and loop isnt checked then end of playlist is reached and player must stop without looping
    if (!loop.checked && currentSourceIndex >= sources.length) {
        console.log("end of playlist");
        // load to reset the element's state
        player.load(); // --fix                       starting index 0 no autopnext
    // otherwise keep playing the music playlist from the starting track cz loop is checked
    } else {
        title.innerHtml = `${sources[currentSourceIndex].title}`
        player.play(); 
    }
}

function playPrevious(player, title, sources) {
    // if index gets to 0 (start of playlist) it will remain at 0 without going negative
    currentSourceIndex = (currentSourceIndex === 0) ? 0 : (currentSourceIndex - 1) % sources.length;
    player.src = `${base}${sources[currentSourceIndex].id}`;
    title.innerHtml = `${sources[currentSourceIndex].title}`
    player.play();
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