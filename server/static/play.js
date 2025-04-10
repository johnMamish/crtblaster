// This variable holds the name of the currently selected item in the video library
var selected_video_name = null;

// This variable holds the name of the currently selected item in the playlist
var selected_playlist_item = null;

// This variable maps video names to thumbnail urls
var thumbnail_url_dict = null;

// This function takes in an array of video descriptors (name, thumbnail) and renders them
async function renderVideoThumbnails(videos) {
    let thumbnailDiv = document.getElementById("videoList");
    thumbnailDiv.replaceChildren();
    thumbnail_url_dict = new Object();
    for (let video of videos) {
        thumbnail_url_dict[video["name"]] = video["thumbnail_url"];

        // create a new thumbnail and append it
        let thumbnail = document.createElement("table");
        thumbnail.classList.add("thumbnail");
        thumbnail.addEventListener('click', function () {
            let videoName = video["name"];
            let me = thumbnail;
            function selectButton() {
                console.log(videoName);
                for (let t of thumbnailDiv.children) {
                    t.classList.remove("thumbnail_selected");
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
        
        label = document.createTextNode(video["name"]);
        
        imgcell = document.createElement('td');
        imgcell.classList.add("thumbnail_image");
        imgcell.appendChild(img);
        tr1 = document.createElement('tr');
        tr1.appendChild(imgcell);
        //imgcell.classList.add("thumbnail_label");
        thumbnail.appendChild(tr1);
        
        labelcell = document.createElement('td');
        labelcell.appendChild(label);
        tr2 = document.createElement('tr');
        labelcell.classList.add("thumbnail_label");
        tr2.appendChild(labelcell);
        thumbnail.appendChild(tr2);
        
        // hacky to manually specify these
        thumbnail.setAttribute('style', 'width: 160px; height: 120px');
        
        thumbnailDiv.appendChild(thumbnail);
    }
}

// The playlist is represented by a json object:
// {
//     now_playing: string     // name of the currently playing video
//     playlist: array of strings    // name of all videos in playlist in order
// }
// Given a json object representing a playlist, 
async function renderPlaylist(playlist_json) {
    let playlistDiv = document.getElementById("playList");
    playlistDiv.replaceChildren();

    for (let videoname of playlist_json.playlist) {
        // create a new playlist entry and append it
        let playlistEntry = document.createElement("table");
        let row = document.createElement('tr');

        img = document.createElement("img");
        img.setAttribute('src', thumbnail_url_dict[videoname]);
        img.setAttribute('width', 120);
        img.setAttribute('height', 80);
        
        
        label = document.createTextNode(videoname);
        
        imgcell = document.createElement('td');
        imgcell.appendChild(img);
        imgcell.setAttribute('style', 'border: 1px black;');
        imgcell.setAttribute('width', 125);
        
        labelcell = document.createElement('td');
        labelcell.setAttribute('style', 'text-align: left; border: 1px black;');
        labelcell.appendChild(label);
        
        row.appendChild(imgcell);
        row.appendChild(labelcell);
        
        playlistEntry.appendChild(row);

        playlistDiv.appendChild(playlistEntry);
    }
}

async function fetchAndRenderPlaylist() {
    let response = await fetch("/playlist/getcurrentplaylist");
    let json = await response.json();
    renderPlaylist(json);
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

    let playlist_event_source = new EventSource('/playlist/playlistevents');
    playlist_event_source.onmessage = async function() {
        console.log("playlist updated");
        fetchAndRenderPlaylist();
    }
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
