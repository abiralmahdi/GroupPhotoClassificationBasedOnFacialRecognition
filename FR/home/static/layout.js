// Sidebar Handling
function openNav() {
    let sidebar = document.getElementById("mySidenav");
    if (sidebar.classList.contains("open")) {
        closeNav();
    } else {
        sidebar.classList.add("open");
        sidebar.style.width = "250px";

        // Show invisible items after a slight delay
        setTimeout(() => {
            Array.from(document.getElementsByClassName("invisible-items")).forEach(element => {
                element.style.visibility = "visible";
            });
        }, 50);

        // Dim the main section
        Array.from(document.getElementsByClassName("mainSection")).forEach(element => {
            element.style.filter = "brightness(0.5)";
        });
    }
}

function closeNav() {
    let sidebar = document.getElementById("mySidenav");
    sidebar.classList.remove("open");
    sidebar.style.width = "0";
    
    // Hide invisible items
    Array.from(document.getElementsByClassName("invisible-items")).forEach(element => {
        element.style.visibility = "hidden";
    });

    // Restore brightness of main section
    Array.from(document.getElementsByClassName("mainSection")).forEach(element => {
        element.style.filter = "brightness(1)";
    });
}

// Handle main content clicks to close sidebar
document.addEventListener("DOMContentLoaded", function () {
    const mainContent = document.querySelector(".mainSection");
    if (mainContent) {
        mainContent.addEventListener("click", closeNav);
    }
});

// Dropzone JS configuration
Dropzone.autoDiscover = false; // Prevent Dropzone from auto initializing

Dropzone.options.fileDropzone = {
    url: myurl,
    maxFilesize: 20, // Max file size in MB
    acceptedFiles: '.jpeg,.jpg,.png',
    autoProcessQueue: false,
    uploadMultiple: true, // Allow multiple file uploads
    parallelUploads: 10, // Max number of concurrent uploads
    addRemoveLinks: true,
    dictDefaultMessage: "Drag & drop images here to upload",
    init: function () {
        var myDropzone = this; // Reference to Dropzone instance
        let isSubmitted = false;

        // Form submission handler
        const eventForm = document.querySelector("#eventForm");

        // Define the function for form submission
        const handleFormSubmit = function (e) {
            console.log("Form submission handler called"); // Debugging line
            e.preventDefault(); // Prevent default form submission
            e.stopPropagation(); // Stop event propagation

            if (!isSubmitted) {
                isSubmitted = true;
                document.querySelector("button[type=submit]").disabled = true; // Disable the submit button

                // Create FormData object for the entire form including Dropzone files
                let formData = new FormData(eventForm);
                
                // Append all files in the Dropzone to the FormData
                myDropzone.files.forEach(file => {
                    formData.append("files[]", file); // Use "files[]" to send as an array
                });

                // Create the event via Ajax
                fetch(myurl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken") // Add CSRF token
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // If event creation is successful, clear Dropzone
                        myDropzone.removeAllFiles(); // Clear files from Dropzone
                    } else {
                        throw new Error('Failed to create event');
                    }
                })
                .catch(error => {
                    console.log('Event creation failed:', error);
                    alert('Event creation failed. Please try again.'); // Alert user about the failure
                    isSubmitted = false;
                });
            }
        };

        // Ensure the listener is only added once
        eventForm.addEventListener("submit", handleFormSubmit);

        // Reset after the queue is processed
        myDropzone.on("queuecomplete", function () {
            isSubmitted = false;
            document.querySelector("button[type=submit]").disabled = false; // Re-enable the submit button
        });

        // Handle errors during upload
        myDropzone.on("error", function (file, response) {
            console.log('File upload failed:', response);
            alert('File upload failed. Please try again.'); // Alert user about the failure
            isSubmitted = false;
        });
    },
    sending: function (file, xhr, formData) {
        // This method is overridden to allow the default processing to continue
        // No additional processing needed here, files are added in handleFormSubmit
    }
};

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Load sidebar in closed state
function onLoadNav() {
    let sidebar = document.getElementById("mySidenav");
    if (sidebar) {
        sidebar.style.width = "0";
        Array.from(document.getElementsByClassName("invisible-items")).forEach(element => {
            element.style.visibility = "hidden";
        });
    }
}
window.addEventListener("load", onLoadNav);
