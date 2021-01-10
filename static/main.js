// Global variables
const images = document.querySelectorAll(".query-img");
const algorithmSelectElement = document.querySelector("#algorithm-select");
const queryImageElement = $("#query-image-show");
const searchingElement = $("#searching");
const errorElement = $("#error");
const succesElement = $("#success");
let data = [];
let isSearching = false;
let algorithm = "simple";


const init = () => {
    $("#results-table").hide();

    handleSearching(false);
    errorElement.hide();
    succesElement.hide();

    queryImageElement.hide();
    
    // Setting the event listeners.
    document.querySelector("#queryImage").addEventListener("change", queryImage);
    document.querySelector("#indexImages").addEventListener("change", sendImageForIndex);
    document.querySelector("#clearResultsBtn").addEventListener("click",removeResults);
    document.querySelector("#searchRocchio").addEventListener("click",querryWithRocchio);


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
	    displaySuccessMessage("Test");
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

function displaySuccessMessage(message) {
    successElement.text(message);
    successElement.show();
}

function hideSuccesMessage() {
    successElement.hide();
}

function markImage(event) {
    const image = event.target;

    if (image.classList.contains("relevant-img")) {
	removeStylesFromMarkedImg(image);
    } else { 
	addStylesToMarkedImg(image);
    }
}

function querryWithRocchio() {
    results_basic = document.querySelector("#results-basic").querySelectorAll("img");
    results_bovw = document.querySelector("#results-bovw").querySelectorAll("img");
    results_cnn = document.querySelector("#results-cnn").querySelectorAll("img");

    const url = "/all-rocchio";

    const relevant_basic = getRelevantResults(results_basic);
    const nonrelevant_basic = getNonRelevantResults(results_basic);
    const relevant_bovw = getRelevantResults(results_bovw);
    const nonrelevant_bovw = getNonRelevantResults(results_bovw);
    const relevant_cnn = getRelevantResults(results_cnn);
    const nonrelevant_cnn = getNonRelevantResults(results_cnn);

    removeResults();
    handleSearching(true);


    // console.log(relevant_basic);
    // console.log(nonrelevant_basic);
    // console.log(relevant_bovw);
    // console.log(nonrelevant_bovw);
    // console.log(relevant_cnn);
    // console.log(nonrelevant_cnn);

    data = {
	"relevant_basic": relevant_basic,
	"nonrelevant_basic": nonrelevant_basic,
	"relevant_bovw": relevant_bovw,
	"nonrelevant_bovw": nonrelevant_bovw,
	"relevant_cnn": relevant_cnn,
	"nonrelevant_cnn": nonrelevant_cnn,
    };

    console.log(data);

    fetch(url, {
	method: "POST",
	body: JSON.stringify(data),
	headers: {
		'Content-type': 'application/json; charset=UTF-8'
	}
    })
	.then (response => {
	    if (response.status !== 200) {
		console.log('Looks like there was a problem. Status Code: ' + response.status);
		return;
	    }

	    response.json().then(function(data) {
		displayResultsAll(data)
		handleSearching(false);
	    })
	})
	.catch (err => {
	    console.log(err);
	});

}


function getRelevantResults(results) {
    relevantResults = [];
    for (let i = 0; i < results.length; i++) {
	let img = results[i]
	if (img.classList.contains("relevant-img")) {
	    let img_str_array = img.src.split("/")
	    let img_name = img_str_array[img_str_array.length-1]
	    relevantResults.push(img_name);
	}
    }
    return relevantResults;
}

function getNonRelevantResults(results) {
    nonRelevantResults = [];
    for (let i = 0; i < results.length; i++) {
	let img = results[i]
	if (!img.classList.contains("relevant-img")) {
	    let img_str_array = img.src.split("/")
	    let img_name = img_str_array[img_str_array.length-1]
	    nonRelevantResults.push(img_name);
	}
    }
    return nonRelevantResults;
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
