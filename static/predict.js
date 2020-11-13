let imageLoaded = false;
$(".selected-image").attr("src", "none.jpeg");

//  function to run for selecting an image

$("#image-selector").change(function () {
    imageLoaded = false;
    let reader = new FileReader();
    reader.onload = function () {
        let dataURL = reader.result;
        $(".selected-image").attr("src", dataURL);
        $(".prediction-list").empty();
        imageLoaded = true;
    }

    let file = $("#image-selector").prop('files')[0];
    reader.readAsDataURL(file);
});


// function to run for loading model
let model;
let modelLoaded = false;
$(document).ready(async function () {
    modelLoaded = false;
    $('.loader').show();
    document.querySelector('.prediction-list').style.display = "none";
    console.log("Loading model...");
    model = await tf.loadGraphModel('model/model.json');
    console.log("Model loaded.");
    $('.loader').hide();
    modelLoaded = true;
});

// function to predict image

$("#predict-button").click(async function () {
    if (!modelLoaded)
    {
        alert("The model must be loaded first"); 
        return; 
    }
    if (!imageLoaded) 
    { 
        alert("Please select an image first"); 
        return; 
    }

    let image = $('.selected-image').get(0);

    // Pre-process the image
    console.log("Loading image...");
    let tensor = tf.browser.fromPixels(image, 3)
        .resizeNearestNeighbor([224, 224]) // change the image size
        .expandDims()
        .toFloat()
        .reverse(-1); // RGB -> BGR
    let predictions = await model.predict(tensor).data();
    console.log(predictions, "are here");

    
    let predictor = Array.from(predictions)
        .map(function (p, i) { // this is Array.map
            return {
                probability: p,
                className: TARGET_CLASSES[i] // we are selecting the value from the obj
            };
        }).sort(function (a, b) {
            return b.probability - a.probability;
        }).slice(0, 3);

    $(".prediction-list").empty();

    predictor.forEach(function (p) {
        p.probability *= 100;
        document.querySelector('.not-pedictions').style.display = "none";
        document.querySelector('.prediction-list').style.display = "table";
        $(".prediction-list").append(`<tr class="tab-div-val"><td>${p.className}</td> <td>${p.probability.toFixed(2)}% </td></tr>`);     
    });
});
