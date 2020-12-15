const images = document.querySelectorAll(".img")

let data = [];
let pathToImages = "../../data/"

for (let image of images) {
    image.addEventListener("click", function () {
        this.classList.add("active")
        let image = this.src

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
                    /*                     console.log('<tr><th><img src="{{ url_for(\'static\', filename=\'images/' + data[i].image +
                                            '\') }} class="result-img"></th><th>' + data[i].score + '</th></tr>');
                                        $("#results").append('<tr><th><img src="{{ url_for(\'static\', filename=\'images/' + data[i].image +
                                            '\') }} class="result-img"></th><th>' + data[i].score + '</th></tr>') */
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
    })
}