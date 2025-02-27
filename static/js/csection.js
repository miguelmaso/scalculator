document.addEventListener("DOMContentLoaded", function () {
    
    document.querySelectorAll(".input-container input").forEach(input => {
        input.addEventListener("blur", validateInput);
        input.addEventListener("blur", sendCalculationRequest);
    });

    document.querySelectorAll(".tag-container").forEach(container => {
        let inputField = container.querySelector(".tagInput");

        // Trigger calculation when pressing Enter, Tab... to add a tag
        inputField.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === "Tab" || event.key === " " || event.key === ",") {
                sendCalculationRequest();
            }
        });

        // Trigger calculation when a tag is removed
        container.addEventListener("click", function (event) {
            if (event.target.classList.contains("remove-tag")) {
                sendCalculationRequest();
            }
        });
    });

    // Initialize empty results
    sendCalculationRequest();
    
    // Update the section input fields according to the section type
    const structureDropdown = document.getElementById("structure-options");
    const sectionDropdown = document.getElementById("section-options");
    const widthLabel = document.getElementById('width-label');
    const flangeInput = document.getElementById('flange');
    const depthInput = document.getElementById('depth');
    const webInput = document.getElementById('web');
    const sectionImage = document.getElementById("section-image");
    const flangeContainer = flangeInput.closest(".input-container");
    const depthContainer = depthInput.closest(".input-container");
    const webContainer = webInput.closest(".input-container");

    function updateSectionInputs() {
        const selectedSection = sectionDropdown.value;
        if (selectedSection === "t-section") {
            flangeContainer.classList.remove("hidden");
            webContainer.classList.remove("hidden");
            sectionImage.src = `/static/img/${selectedSection}.png`;
        }
        else {
            flangeContainer.classList.add("hidden");
            webContainer.classList.add("hidden");
        }
        if (selectedSection === "circular") {
            depthContainer.classList.add("hidden");
            widthLabel.textContent = "Diameter";
        }
        else {
            depthContainer.classList.remove("hidden");
            widthLabel.textContent = "Width";
        }
        const selectedStructure = structureDropdown.value;
        if (selectedStructure === "wall" || selectedStructure === "slab") {
            sectionImage.src = `/static/img/slab.png`;
        }
        else {
            sectionImage.src = `/static/img/${selectedSection}.png`;
        }
    }

    sectionDropdown.addEventListener("change", updateSectionInputs);
    updateSectionInputs();

    // Update the section stype according to the structure type
    const widthInput = document.getElementById("width");
    const structuralSectionOptions = {
        beam: ["Rectangular", "T-section"],
        slab: ["Rectangular"],
        wall: ["Rectangular"],
        column: ["Rectangular", "Circular"]
    };

    function updateStructuralSectionOptions() {
        // Clear previous options
        sectionDropdown.innerHTML = "";

        const selectedStructure = structureDropdown.value;
        if (selectedStructure) {
            // Populate it with new options
            structuralSectionOptions[selectedStructure].forEach(item => {
                let option = document.createElement("option");
                option.value = item.toLowerCase();
                option.textContent = item;
                sectionDropdown.appendChild(option);
            });
        }
        if (selectedStructure === "slab" || selectedStructure === "wall") {
            widthInput.disabled = true;
            widthInput.value = "1000";
        }
        else {
            widthInput.disabled = false;
        }
        updateSectionInputs();
    }

    structureDropdown.addEventListener("change", updateStructuralSectionOptions);
    updateStructuralSectionOptions();
});

function validateInput(event) {
    let input = event.target;
    let value = input.value.trim();

    if (isNaN(value) || parseFloat(value) <= 0) {
        alert("Enter a positive number for " + input.name + ".");
        input.value = "";
        input.focus();  // Keep focus on the input field
        event.preventDefault();  // Prevent focus from moving forward
    }
}

function sendCalculationRequest() {
    let formData = {};

    // Collect selection inputs
    document.querySelectorAll(".input-container select").forEach(select => {
        formData[select.name] = select.value;
    });

    // Collect numeric inputs
    document.querySelectorAll(".input-container input").forEach(input => {
        formData[input.name] = input.value;
    });

    // Collect tag inputs
    document.querySelectorAll(".tag-container").forEach(container => {
        let tagName = container.getAttribute("data-name");  // Get the tag field name
        let tags = Array.from(container.querySelectorAll(".tag")).map(tag => tag.textContent.replace("×", "").trim());  
        formData[tagName] = tags;  // Store as an array
    });

    // Send request
    fetch("/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => updateResults(data))
    .then(data => updateGraph(data))
    .catch(error => {
        console.error("Error:", error);
    });
}

function updateResults(data) {
    if (data.result) {
        document.getElementById("result").textContent = data.result;
    } else {
        document.getElementById("result").textContent = "";
    }
    return data;
}

function updateGraph(data) {
    if (data.graph) {
        let graphContainer = document.getElementById("graph-container-1");
        let plotData = JSON.parse(data.graph); // Parse JSON response from Flask
        Plotly.react(graphContainer, plotData.data, plotData.layout);
    }
    if (data.graph2) {
        let graphContainer = document.getElementById("graph-container-2");
        let plotData = JSON.parse(data.graph2); // Parse JSON response from Flask
        Plotly.react(graphContainer, plotData.data, plotData.layout);
    }
    return data;
}
