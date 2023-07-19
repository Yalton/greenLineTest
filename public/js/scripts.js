function handleFormSubmission() {
    document.getElementById('uploadForm').addEventListener('submit', function (e) {
        e.preventDefault();

        // Get the spinner and start it
        const loadingSpinner = document.getElementById('loadingSpinner');
        loadingSpinner.style.display = 'block';

        const formData = new FormData();
        formData.append('image', document.getElementById('image').files[0]);

        fetch('/predict', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Error during image processing, Try another image');
            }
            return response.json();
        }).then(data => {
            // Create a URL for the base64 image
            const url = 'data:image/png;base64,' + data.base64_image;

            // Update the image element
            const outputImage = document.getElementById('outputImage');
            outputImage.src = url;

            // Update the download button
            const downloadButton = document.getElementById('downloadButton');
            downloadButton.href = url;
            downloadButton.style.display = 'inline-block';

            // Stop the spinner
            loadingSpinner.style.display = 'none';
        }).catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            // Display the error message from the backend
            alert(error.message);
            // Stop the spinner even if there's an error
            loadingSpinner.style.display = 'none';
        });
    });
}


function startAnimation() {
    let canvas = document.getElementById('backgroundCanvas');
    let ctx = canvas.getContext('2d');

    // Create an array to hold the lines
    let lines = [];

    // Create six lines
    for (let i = 0; i < 6; i++) {
        lines.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            color: `hsl(${Math.random() * 360}, 100%, 50%)` // Use hsl to get different colors for each line
        });
    }

    function animate() {
        // Clear the canvas with a semi-transparent color to create a trail effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Loop over each line
        for (let line of lines) {
            // Update position
            line.x += line.vx;
            line.y += line.vy;

            // Reverse velocity when hitting an edge
            if (line.x < 0 || line.x > canvas.width) line.vx = -line.vx;
            if (line.y < 0 || line.y > canvas.height) line.vy = -line.vy;

            // Draw the line
            ctx.strokeStyle = line.color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(line.x - line.vx, line.y - line.vy);
            ctx.lineTo(line.x, line.y);
            ctx.stroke();
        }

        requestAnimationFrame(animate);
    }

    animate();
}


// function handleFormSubmission() {
//     document.getElementById('uploadForm').addEventListener('submit', function (e) {
//         e.preventDefault();
//         const formData = new FormData();
//         formData.append('image', document.getElementById('image').files[0]);

//         fetch('/predict', {
//             method: 'POST',
//             body: formData
//         }).then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         }).then(data => {
//             // Create a URL for the base64 image
//             const url = 'data:image/png;base64,' + data.base64_image;
            
//             // Update the image element
//             const outputImage = document.getElementById('outputImage');
//             outputImage.src = url;

//             // Update the download button
//             const downloadButton = document.getElementById('downloadButton');
//             downloadButton.href = url;

//             // Show the download button
//             downloadButton.style.display = 'inline-block';
//         }).catch(error => {
//             console.error('There has been a problem with your fetch operation:', error);
//         });
//     });
// }

window.onload = function() {
    handleFormSubmission();
    startAnimation();
}



// async function getFormats() {
//     const urlInput = document.querySelector('#url');
//     const url = urlInput.value;
//     const getFormatsButton = document.querySelector('#getFormatsButton');

//     // Create a loading spinner element
//     const loadingSpinner = document.createElement('div');
//     loadingSpinner.classList.add('spinner'); // Add class for styling (in CSS)
//     loadingSpinner.innerText = ''; // Or add an image/gif

//     const form = document.querySelector('form');

//     // Replace the Get Formats button with the loading spinner
//     form.replaceChild(loadingSpinner, getFormatsButton);

//     const response = await fetch('/formats', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ url }),
//     });

//     if (!response.ok) {
//         console.error('An error occurred while fetching the formats.');
//     } else {
//         const data = await response.json();
//         const formatSelect = document.querySelector('#formatId');
//         formatSelect.innerHTML = ''; // Remove existing options

//         data.formats.forEach(({ id, resolution }) => {
//             const option = document.createElement('option');
//             option.value = id;
//             option.textContent = id + " (" + resolution + ")";
//             formatSelect.appendChild(option);
//         });

//         document.querySelector('.download-button').style.display = 'none'; // Initially hide the download button
//     }

//     // Replace the loading spinner with the Get Formats button
//     form.replaceChild(getFormatsButton, loadingSpinner);
// }

// async function downloadVideo(event) {
//     event.preventDefault();

//     const urlInput = document.querySelector('#url');
//     const formatIdInput = document.querySelector('#formatId');
//     const downloadButton = document.querySelector('.download-button');

//     const url = urlInput.value;
//     const formatId = formatIdInput.value;

//     const loadingSpinner = document.createElement('div');
//     loadingSpinner.classList.add('spinner');
//     loadingSpinner.innerText = '';

//     const form = document.querySelector('form');

//     form.replaceChild(loadingSpinner, downloadButton);

//     const response = await fetch('/download', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ url, formatId }),
//     });

//     if (!response.ok) {
//         console.error('An error occurred while downloading the video.');
//     } else {
//         const data = await response.json();
//         const downloadId = data.downloadId;

//         // Start polling for the download status
//         checkDownloadStatus(downloadId, loadingSpinner, downloadButton, form);
//         //checkDownloadStatus(downloadId, loadingSpinner, downloadButton);
//     }

//     urlInput.value = '';
//     formatIdInput.value = '';
// }

// async function checkDownloadStatus(downloadId, loadingSpinner, downloadButton, form) {
//     const response = await fetch(`/status/${downloadId}`);

//     if (!response.ok) {
//         console.error('An error occurred while checking the download status.');
//     } else {
//         const status = await response.json();

//         // Check if the download is completed
//         if (status.status === 'completed') {
//             const downloadLink = document.createElement('a');
//             downloadLink.href = status.downloadUrl;
//             downloadLink.innerText = 'View Video';
//             downloadLink.classList.add('button-link');  // Add a class to the download link for styling

//             // Replace the loading spinner with the download link if it is still a child of the form
//             if (form.contains(loadingSpinner)) {
//                 form.replaceChild(downloadLink, loadingSpinner);
//             }
//         } else if (status.status === 'error') {
//             console.error(status.message);
//             // Replace the loading spinner with the download button if it is still a child of the form
//             if (form.contains(loadingSpinner)) {
//                 form.replaceChild(downloadButton, loadingSpinner);
//             }
//         } else {
//             // If the download is still in progress, poll again in a few seconds
//             setTimeout(() => checkDownloadStatus(downloadId, loadingSpinner, downloadButton, form), 5000);
//         }
//     }
// }


// async function fetchQueueSize() {
//     const response = await fetch('/queue-size');
//     const data = await response.json();
//     return data.size;
// }

// document.addEventListener('DOMContentLoaded', () => {
//     const queueSizeElement = document.getElementById('queue-size');

//     setInterval(async () => {
//         if (queueSizeElement) {
//             const size = await fetchQueueSize();
//             queueSizeElement.textContent = `Queue size: ${size}`;
//         }
//     }, 5000);
// });

// // A function to show the download button when a format is selected
// function showDownloadButton() {
//     const formatIdInput = document.querySelector('#formatId');
//     if (formatIdInput.value) {  // Only show the button if a format is selected
//         document.querySelector('.download-button').style.display = 'block'; // Show the download button
//     }
// }


// // async function downloadVideo(event) {
// //     event.preventDefault();

// //     const urlInput = document.querySelector('#url');
// //     const formatIdInput = document.querySelector('#formatId');
// //     const downloadButton = document.querySelector('.download-button');

// //     const url = urlInput.value;
// //     const formatId = formatIdInput.value;

// //     // Need to Validate and sanitize the input

// //     // Create a loading spinner element
// //     const loadingSpinner = document.createElement('div');
// //     loadingSpinner.classList.add('spinner'); // Add class for styling (in CSS)
// //     loadingSpinner.innerText = ''; // Or add an image/gif

// //     const form = document.querySelector('form');

// //     // Replace the download button with the loading spinner
// //     form.replaceChild(loadingSpinner, downloadButton);

// //     const response = await fetch('/download', {
// //         method: 'POST',
// //         headers: {
// //             'Content-Type': 'application/json',
// //         },
// //         body: JSON.stringify({ url, formatId }),
// //     });

// //     if (!response.ok) {
// //         console.error('An error occurred while downloading the video.');
// //     } else {
// //         const data = await response.json();
// //         console.log(data);

// //         // Provide a download link
// //         const downloadLink = document.createElement('a');
// //         downloadLink.href = data.downloadUrl;
// //         downloadLink.innerText = 'View Video';
// //         downloadLink.classList.add('button-link');  // Add a class to the download link for styling

// //         // Replace the loading spinner with the download link
// //         form.replaceChild(downloadLink, loadingSpinner);

// //         // Clear the resolution options
// //         formatIdInput.innerHTML = '';
// //     }

// //     urlInput.value = '';
// //     formatIdInput.value = '';
// // }