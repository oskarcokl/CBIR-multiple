const images = document.querySelectorAll(".img")

let data = [];


for (let image of images) {
    image.addEventListener("click", function () {

        // Remove stylng from other images.
        removeClassAll(images);

        // Make the selected image more noticable
        this.classList.add("active")
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
                    resultImg.classList.add("result-image")

                    thImage.append(resultImg);
                    thScore.append(`${data[i].score}`);

                    tr.append(thImage);
                    tr.append(thScore);

                    document.querySelector("#results").append(tr);
                };
            },
            // handle error
            error: function (error) {
                console.log(error);
            }
        });
    });
}

document.querySelector("#clearResultsBtn").addEventListener("click", function () {
    removeChildNodes(document.querySelector("#results"));
});

const removeChildNodes = (parentNode) => {
    while (parentNode.lastElementChild) {
        parentNode.removeChild(parentNode.lastElementChild);
    }
}


const removeClassAll = (images) => {
    for (let image of images) {
        removeClass(image, "active");
    }
}

const removeClass = (object, cssClass) => {
    object.classList.remove(cssClass)
}