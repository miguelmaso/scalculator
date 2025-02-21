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
        if (data.error) {
            document.getElementById("result").textContent = "Error: " + data.error;
        } else {
            document.getElementById("result").textContent = data.result;
        }
        return data;
    }

    function updateGraph(data) {
        let graphContainer = document.getElementById("graph-container");
        let graphJson = data.graph;

        if (!graphJson || graphJson.trim() === "{}") {
            console.error("Invalid graph data:", graphJson);
            return;
        }
    
        let plotData;
        try {
            plotData = JSON.parse(graphJson);
        } catch (error) {
            console.error("Error parsing graph JSON:", error);
            return;
        }
    
        if (!plotData.data || plotData.data.length === 0) {
            console.error("Graph data is empty:", plotData);
            return;
        }

        console.error("AAAAAAA", plotData);
        Plotly.react(graphContainer, plotData.data, plotData.layout);
        // if (data.graph) {
        //     let graphContainer = document.getElementById("graph-container");
        //     let plotData = JSON.parse(data.graph); // Parse JSON response from Flask
        //     Plotly.react(graphContainer, plotData.data, plotData.layout);
        // }
        // return data;
    }
});
