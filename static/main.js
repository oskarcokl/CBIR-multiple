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
    $("#results-table").hide();

    handleSearching(false);
    errorElement.hide();

    queryImageElement.hide();
    
    // Setting the event listeners.
    document.querySelector("#queryImage").addEventListener("change", queryImage);
    document.querySelector("#indexImages").addEventListener("change", sendImageForIndex);
    document.querySelector("#clearResultsBtn").addEventListener("click",removeResults);
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


    removeResults();
    disableImageUpload();
    displayQueryImage(image);

    $.ajax({
        type: "POST",
        url: "/all-search",
        data: formData,
	contentType: false,
        processData: false,
        // handle success
        success: function(result) {
	    displayResultsAll(result);
	},
        // handle error
        error: function (error) {
            errorElement.show();
            console.log(error);
        }
    });
}

function sendImageForIndex() {
    const formData = new FormData();

    for (let i = 0; i < this.files.length; i++) {
	formData.append("img_"+i, this.files[i]);
    }

    
    console.log(formData);
    const url = "/all-index";

    fetch(url, {
	method: "POST",
	body: formData
    })
	.then (response => {
	    console.log(response);
	})
	.then (success => {
	    console.log(success);
	})
	.catch (err => {
	    console.log(err);
	});
}

function removeResults() { 
    $("#results-table").hide();
    removeChildNodes(document.querySelector("#results-basic"));
    removeChildNodes(document.querySelector("#results-bovw"));
    removeChildNodes(document.querySelector("#results-cnn"));
}

function displayResultsAll(result) {
    console.log(result[0]);
    $("#results-table").show();
    styleResultsAndShow(result[0].basic, "#results-basic");
    styleResultsAndShow(result[0].bovw, "#results-bovw");
    styleResultsAndShow(result[0].cnn, "#results-cnn");
    handleSearching(false);
    enableImageUpload();
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

	let resultImg = document.createElement("img");
	resultImg.src = `static/images/${data[i].image}`;
	resultImg.style.width = "300px";
	resultImg.style.height = "300px";


	thImage.append(resultImg);

	tr.append(thImage);

	document.querySelector("#results").append(tr);
    };
    handleSearching(false);
    enableImageUpload();
}

function styleResultsAndShow(data, id) {
    console.log(data);
    for (i = 0; i < data.length; i++) {
	let tr = document.createElement("tr");
	let thImage = document.createElement("th");

	let resultImg = document.createElement("img");
	resultImg.src = `static/images/${data[i].image}`;
	resultImg.style.width = "300px";
	resultImg.style.height = "300px";

	// Add class for marking for rocchio
	resultImg.addEventListener("click", markImage);


	thImage.append(resultImg);

	tr.append(thImage);

	document.querySelector(id).append(tr);
    };

}

function markImage(event) {
    const image = event.target;
    console.log(image);

    if (image.classList.contains("relevant-img")) {
	removeStylesFromMarkedImg(image);
    } else { 
	addStylesToMarkedImg(image);
    }
}

function reQuerryWithRocchio() {
    console.log("You are using Rocchio.")
}

function addStylesToMarkedImg(image) {
    image.classList.add("border")
    image.classList.add("border-info")
    image.classList.add("border-5")
    image.classList.add("relevant-img")
}


function removeStylesFromMarkedImg(image) {
    image.classList.remove("border")
    image.classList.remove("border-info")
    image.classList.remove("border-5")
    image.classList.remove("relevant-img")
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
