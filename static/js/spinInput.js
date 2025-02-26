document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".spin-container").forEach(initSpinInput);
});

function initTagInput(container) {
    const allowedValues = [8, 10, 12, 16, 20, 25, 32, 40];
    const spinnerInput = container.querySelector("spinner-input");
    const decreaseBtn = container.querySelector("decrease-btn");
    const increaseBtn = container.querySelector("increase-btn");

    function findClosest(value) {
        return allowedValues.reduce((prev, curr) =>
            Math.abs(curr - value) < Math.abs(prev - value) ? curr : prev
        );
    }

    function updateValue(newValue) {
        let closest = findClosest(newValue);
        spinnerInput.value = closest;
    }

    decreaseBtn.addEventListener("click", function () {
        let currentIndex = allowedValues.indexOf(parseInt(spinnerInput.value, 10));
        if (currentIndex > 0) {
            updateValue(allowedValues[currentIndex - 1]);
        }
    });

    increaseBtn.addEventListener("click", function () {
        let currentIndex = allowedValues.indexOf(parseInt(spinnerInput.value, 10));
        if (currentIndex < allowedValues.length - 1) {
            updateValue(allowedValues[currentIndex + 1]);
        }
    });

    spinnerInput.addEventListener("change", function () {
        updateValue(parseInt(this.value, 10));
    });
}
