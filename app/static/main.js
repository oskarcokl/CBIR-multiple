// Global variables
const images = document.querySelectorAll(".query-img");
const algorithmSelectElement = document.querySelector("#algorithm-select");
const searchingElement = $("#searching");
const errorElement = $("#error");
let data = [];
let isSearching = false;
let algorithm = "simple";


const init = () => {
    handleSearching(false);
    errorElement.hide();


    // Setting the event listeners.
    for (let image of images) {
        image.addEventListener("click", onQueryImageClick);
    }
    document.querySelector("#clearResultsBtn").addEventListener("click", function () {
        removeChildNodes(document.querySelector("#results"));
    });
    algorithmSelectElement.addEventListener("change", function (event) {
        algorithm = event.target.value;
        console.log(algorithm);
    })
}

function onQueryImageClick(event) {
    // Check if we are already performing a search.
    if (isSearching) {
        return
    }

    handleSearching(true);

    // Remove stylng from other images.
    removeClassAll(images);

    // Make the selected image more noticable
    makeHighlighted(this);
    let image = this.src

    // Remove previous results
    removeChildNodes(document.querySelector("#results"));


    $.ajax({
        type: "POST",
        url: "/search",
        data: {
            img: image
        },
        // handle success
        success: function (result) {
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
                resultImg.src = `static/images/${data[i].image}`
                resultImg.classList.add("img-thumbnail")

                thImage.append(resultImg);
                thScore.append(`${data[i].score}`);

                tr.append(thImage);
                tr.append(thScore);

                document.querySelector("#results").append(tr);
            };

            handleSearching(false);

        },
        // handle error
        error: function (error) {
            errorElement.show();
            console.log(error);
        }
    });
}

const makeHighlighted = (image) => {
    image.classList.add("border");
    image.classList.add("border-danger");
    image.classList.add("border-3");
    image.classList.add("rounded");
}

const removeHighlighted = (image) => {
    image.classList.remove("border");
    image.classList.remove("border-danger");
    image.classList.remove("border-3");
    image.classList.remove("rounded");
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