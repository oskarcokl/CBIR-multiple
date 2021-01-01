// Global variables
const images = document.querySelectorAll(".query-img");
const algorithmSelectElement = document.querySelector("#algorithm-select");
const queryImageElement = $("#query-image-show");
const searchingElement = $("#searching");
const errorElement = $("#error");
let data = [];
let isSearching = false;
let algorithm = "simple";


const init = () => {
    handleSearching(false);
    errorElement.hide();

    queryImageElement.hide();
    
    // Setting the event listeners.
    document.querySelector("#queryImage").addEventListener("change", queryImage);
    document.querySelector("#clearResultsBtn").addEventListener("click", function () {
        removeChildNodes(document.querySelector("#results"));
    });
    algorithmSelectElement.addEventListener("change", function (event) {
        algorithm = event.target.value;
        console.log(algorithm);
    })
}

function queryImage(event) {
    const image = this.files[0];
    const formData = new FormData();
    formData.append("img", image);

    // THis can be checked in the HTML itself
    if (!isFileImage(image)) {
	console.log("Please upload an image.")
	return;
    }

    const endpoint = "/" + algorithm + "-search";

    console.log("Using", algorithm);
    handleSearching(true);

    removeChildNodes(document.querySelector("#results"));
    disableImageUpload();
    displayQueryImage(image);  

    $.ajax({
        type: "POST",
        url: endpoint,
        data: formData,
	contentType: false,
        processData: false,
        // handle success
        success: function(result) {
	    displayResults(result);
	},
        // handle error
        error: function (error) {
            errorElement.show();
            console.log(error);
        }
    });
}

function displayResults(result) {
    console.log(result.results);
    data = result.results
    // show table
    $("#results-table").show();
    // loop through results, append to dom
    for (i = 0; i < data.length; i++) {
	let tr = document.createElement("tr");
	let thImage = document.createElement("th");
	let thScore = document.createElement("th");

	let resultImg = document.createElement("img");
	resultImg.src = `static/images/${data[i].image}`;
	resultImg.style.width = "300px";
	resultImg.style.height = "300px";


	thImage.append(resultImg);
	thScore.append(`${data[i].score}`);

	tr.append(thImage);
	tr.append(thScore);

	document.querySelector("#results").append(tr);
    };
    handleSearching(false);
    enableImageUpload();
}


function displayQueryImage(image) {
    document.querySelector("#query-image-show").src = URL.createObjectURL(image);
    queryImageElement.show();
}

function disableImageUpload() {
    document.querySelector("#queryImage").disabled = true;
}

function enableImageUpload() {
    document.querySelector("#queryImage").disabled = false;
}

function isFileImage(file) {
    const acceptedImageTypes = ['image/jpeg', 'image/png'];
 
    return file && acceptedImageTypes.includes(file['type'])
}


const removeChildNodes = (parentNode) => {
    while (parentNode.lastElementChild) {
        parentNode.removeChild(parentNode.lastElementChild);
    }
}

const handleSearching = (searching) => {
    isSearching = searching;
    if (searching) {
        searchingElement.show();
    } else {
        searchingElement.hide();
    }
}

const removeClassAll = (images) => {
    for (let image of images) {
        removeHighlighted(image, "active");
    }
}

const removeClass = (object, cssClass) => {
    object.classList.remove(cssClass)
}

// Waiting for the window to load and then calling the init function
window.onload = (event) => {
    console.log("Page loaded");
    init();
}
