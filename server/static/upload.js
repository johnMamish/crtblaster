function uploadVideo() {
    const selectedFile = document.getElementById("videoSelector").files[0];

    let formData = new FormData();
    formData.append("video", selectedFile);
    formData.append("videoname", document.getElementById("videoName").value);
    fetch('/upload/video', {method: "POST", body: formData});

    alert("Uploading video. This may take a minute.");
}
