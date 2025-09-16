

const input = document.getElementById("area-code-input");
const container = document.getElementById("area-code-container");
const hiddenInput = document.getElementById("area-codes-hidden");
let tags = [];

function updateHiddenInput() {
    hiddenInput.value = tags.join(",");
}

function addTag(code) {
    if (code && !tags.includes(code)) {
        tags.push(code);

        const tag = document.createElement("span");
        tag.className = "bg-blue-100 text-blue-800 px-2 py-1 rounded-lg text-sm flex items-center gap-1";
        tag.innerHTML = `
        ${code}
        <button type="button" class="ml-1 text-red-500 hover:text-red-700">&times;</button>
      `;

        // remove tag when clicked
        tag.querySelector("button").addEventListener("click", () => {
            tags = tags.filter(t => t !== code);
            container.removeChild(tag);
            updateHiddenInput();
        });

        container.insertBefore(tag, input);
        input.value = "";
        updateHiddenInput();
    }
}

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === ",") {
        e.preventDefault();
        const code = input.value.trim();
        addTag(code);
    }
});