document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".tag-container").forEach(initTagInput);

    function initTagInput(container) {
        const tagInput = container.querySelector(".tagInput");
        const hiddenInput = container.nextElementSibling; // Hidden input field
        let tags = [];

        function updateHiddenInput() {
            hiddenInput.value = tags.join(",");
        }

        function isValidFormat(value) {
            const validNumbers = ["8", "10", "12", "16", "20", "25", "32", "40"];
            const regex = /^(\d+)([Hh])(\d+)$/; // Only matches nHd (H required)

            const match = value.match(regex);
            if (!match) {
                alert("Invalid format! Use: nHd, Hd@s or nHd@s, where the diameter d is specified after the letter H and the spacing s is specified after the letter @.");
                return false;
            }

            let prefix = match[1];  // First number (X)
            let letter = match[2];   // H (required)
            let num = match[3];      // The number after H

            // Ensure H is uppercase
            letter = "H";
            value = `${prefix}${letter}${num}`;

            // Validate number after H
            if (!validNumbers.includes(num)) {
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
            tag.textContent = value;

            const removeBtn = document.createElement("span");
            removeBtn.classList.add("remove-tag");
            removeBtn.innerHTML = "&times;";
            removeBtn.addEventListener("click", function () {
                container.removeChild(tag);
                tags = tags.filter(t => t !== value);
                updateHiddenInput();
            });

            tag.appendChild(removeBtn);
            container.insertBefore(tag, tagInput);
            tags.push(value);
            updateHiddenInput();
        }

        tagInput.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === ",") {
                event.preventDefault();
                createTag(tagInput.value);
                tagInput.value = "";
            }
        });
    }
});
