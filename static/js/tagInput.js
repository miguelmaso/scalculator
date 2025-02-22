document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".tag-container").forEach(initTagInput);
});

function initTagInput(container) {
    const tagInput = container.querySelector(".tagInput");
    const hiddenInput = container.nextElementSibling; // Hidden input field
    let tags = [];

    function updateHiddenInput() {
        hiddenInput.value = tags.join(",");
    }

    function isValidFormat(value) {
        const validNumbers = ["8", "10", "12", "16", "20", "25", "32", "40"];
        const regex = /^(\d*)([Hh])(\d+)(?:(@)(\d+))?$/; // Matches 3H25@100, where 3 is optional, H25 is mandatory and @100 is optional

        const match = value.match(regex);
        if (!match) {
            alert("Invalid format! Type 4H12 or H12@100, where H20 represent the diameter specified in mm and @100 is the spacing.");
            return false;
        }

        let prefix = match[1] || "";  // First number (optional)
        let letter = match[2];        // H (required)
        let diam = match[3];          // The diameter in mm
        let schar = match[4] || "";   // The spacing character (optional)
        let spac = match[5] || "";    // The spacing in mm (optional)

        // Ensure H is uppercase
        letter = "H";
        value = `${prefix}${letter}${diam}${schar}${spac}`;

        // Validate number after H
        if (!validNumbers.includes(diam)) {
            alert("Invalid diameter. Allowed values: 8, 10, 12, 16, 20, 25, 32, 40.");
            return false;
        }

        return value; // Return corrected value
    }

    function createTag(value) {
        value = value.trim();
        if (value === "" || tags.includes(value)) return;

        // Validate the input
        const validatedValue = isValidFormat(value);
        if (!validatedValue) return;

        const tag = document.createElement("span");
        tag.classList.add("tag");
        tag.textContent = validatedValue;

        const removeBtn = document.createElement("span");
        removeBtn.classList.add("remove-tag");
        removeBtn.innerHTML = "&times;";
        removeBtn.addEventListener("click", function () {
            container.removeChild(tag);
            tags = tags.filter(t => t !== validatedValue);
            updateHiddenInput();
        });

        tag.appendChild(removeBtn);
        container.insertBefore(tag, tagInput);
        tags.push(validatedValue);
        updateHiddenInput();
    }

    tagInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === "Tab" || event.key === " " || event.key === ",") {
            if (tagInput.value.trim() !== "") {
                event.preventDefault();
                createTag(tagInput.value);
                tagInput.value = "";
            }
        }
    });
}
