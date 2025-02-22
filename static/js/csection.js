document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".input-container input").forEach(input => {
        input.addEventListener("blur", sendCalculationRequest);
    });

    document.querySelectorAll(".tag-container").forEach(container => {
        let inputField = container.querySelector(".tagInput");

        // Trigger calculation when pressing Enter, Tab... to add a tag
        inputField.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === "Tab" || event.key === " " || event.key === ",") {
                // if (inputField.value.trim() !== "") {
                    sendCalculationRequest();
                // }
            }
        });

        // Trigger calculation when a tag is removed
        container.addEventListener("click", function (event) {
            if (event.target.classList.contains("remove-tag")) {
                sendCalculationRequest();
            }
        });
    });

    function sendCalculationRequest() {
        let formData = {};

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
});
