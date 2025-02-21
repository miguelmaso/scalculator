document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".input-container input").forEach(input => {
        input.addEventListener("blur", sendCalculationRequest);
    });

    function sendCalculationRequest() {
        let formData = {};
        document.querySelectorAll(".input-container input").forEach(input => {
            formData[input.name] = input.value;
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
