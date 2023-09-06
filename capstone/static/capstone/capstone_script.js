
const sources = Object.keys(all_tracks);

const base = "https://drive.google.com/uc?id="

let currentSourceIndex = 0;

console.log(sources.length);


document.addEventListener("DOMContentLoaded", function() {
    // console.log("ECHOMOOD");

    const player = document.getElementById("player1");
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
        playNext(player, loop);
    });

    playPreviousButton.addEventListener("click", () => {
        playPrevious(player);
    });

    player.addEventListener("ended", playNext);


})

    
function stopPlayer(player) {
    player.currentTime = 0; // Reset playback position
    player.load(); // Load to reset the element's state
}
    

function playNext(player, loop) {
    currentSourceIndex = (currentSourceIndex + 1) % sources.length;
    player.src = `${base}${sources[currentSourceIndex]}`;
    if (!loop.checked && currentSourceIndex === 0) {
        console.log("end of playlist");
        player.load(); // Load to reset the element's state
    } else {
        player.play(); 
    }
}

function playPrevious(player) {
    currentSourceIndex = (currentSourceIndex === 0) ? 0 : (currentSourceIndex - 1) % sources.length;
    player.src = `${base}${sources[currentSourceIndex]}`;
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