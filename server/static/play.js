// This variable holds the name of the currently selected item in the video library
var selected_video_name = null;

// This variable holds the name of the currently selected item in the playlist
var selected_playlist_item = null;

// This variable maintains the list of video names

// This function takes in an array of video descriptors (name, thumbnail) and renders them
async function renderVideoThumbnails(videos) {
    console.log(videos);
    let thumbnailDiv = document.getElementById("videoList");
    thumbnailDiv.replaceChildren();
    for (let video of videos) {
        console.log(video["name"]);
        
        // create a new thumbnail and append it
        let s = document.createElement("div");
        s.classList.add("thumbnail");
        s.addEventListener('click', function () {
            let videoName = video["name"];
            let me = s;
            function selectButton() {
                console.log(videoName);
                for (let thumbnail of thumbnailDiv.children) {
                    thumbnail.classList.remove("thumbnail_selected");
                }
                me.classList.add("thumbnail_selected");
                selected_video_name = video["name"];
            }
            selectButton();
        });

        img = document.createElement("img");
        img.setAttribute('src', video["thumbnail_url"]);
        img.setAttribute('width', 120);
        img.setAttribute('height', 80);
        s.appendChild(img);
        
        s.appendChild(document.createElement("br"));
        s.appendChild(document.createTextNode(video["name"]));
        thumbnailDiv.appendChild(s);
    }
}

async function fetchAndRenderThumbs() {
    // request all video thumbnails
    let response = await fetch("/upload/videoinfo");
    let json = await response.json();
    renderVideoThumbnails(json);
}

// When the page is done loading, we should request all thumbnails
document.addEventListener("DOMContentLoaded", fetchAndRenderThumbs);

// When the page is done loading, subscribe to server-sent-events about 
// thumbnail and playlist updates.
document.addEventListener("DOMContentLoaded", function () {
    let upload_event_source = new EventSource('/upload/videouploadevents');
    upload_event_source.onmessage = async function() {
        console.log("video list updated");
        fetchAndRenderThumbs();
    }

    //let playlist_event_source = new EventSource('');
});

///////////////////////////////////////////////
// Functions for handling user button presses

// Send a request to the server to delete the video with the selected name
async function deleteVideo(selected_video_name) {
    const response = await fetch("/upload/deletevideo", {
        method: "POST",
        headers: {
            'Content-Type' : 'application/json'
        },
        body: "{\"name\": \"" + selected_video_name + "\"}"
    });
}

// Sends a request asking the selected video to be added to the playlist
async function addVideoToPlaylist(selected_video_name) {
    const response = await fetch("/playlist/playvideo", {
        method: "POST",
        headers: {
            'Content-Type' : 'application/json'
        },
        body: "{\"name\": \"" + selected_video_name + "\"}"
    });

}

async function togglePlaylistShuffle() {

}

async function playPlaylist() {

}

async function stopPlaylist() {

}

async function removeItemFromPlaylist() {

}
