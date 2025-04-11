let animateDots = 0;
let currentUploadName;

let ONE_GIGABYTE = (1 << 30);
let MAX_FILESIZE = ONE_GIGABYTE / 2;

async function uploadVideo() {
    const selectedFile = document.getElementById("videoSelector").files[0];
    let name = document.getElementById("videoName").value;
    let uploadStatus = document.getElementById("uploadStatus");

    if (selectedFile.size > MAX_FILESIZE) {
        uploadStatus.replaceChildren();
        uploadStatus.appendChild(document.createTextNode(
            "Won't upload, file too big. Max is " +
                (MAX_FILESIZE >> 20) + " MBytes, yours is " +
                (selectedFile.size >> 20) + " MBytes."));
        return;
    }

    let formData = new FormData();
    formData.append("video", selectedFile);
    formData.append("videoname", name);

    // kick off animation
    currentUploadName = name;
    animateDots = 0;
    let anim = setInterval(animateUpload, 300);

    let response = await fetch('/upload/video', {method: "POST", body: formData});
    console.log(response);

    clearInterval(anim);
    uploadStatus.replaceChildren();
    if (response.status == 200) {
        uploadStatus.appendChild(document.createTextNode("Done uploading " + name + "!"));
    } else {
        uploadStatus.appendChild(document.createTextNode("Failed to upload file " + name +
                                                         ". Server rejected the file due to " +
                                                        response.statusText));
    }
}

async function animateUpload() {
    uploadStatus.replaceChildren();
    uploadStatus.appendChild(document.createTextNode("Uploading video " + currentUploadName + '.'.repeat(animateDots)));

    animateDots = (animateDots + 1) % 4;
}
