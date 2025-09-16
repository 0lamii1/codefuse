
document.getElementById("country").addEventListener("change", function () {
        const value = this.value;

        // Hide all first
        document.getElementById("us-service").classList.add("hidden");
        document.getElementById("german-service").classList.add("hidden");
        document.getElementById("other-service").classList.add("hidden");

        if (value === "us") {
            document.getElementById("us-service").classList.remove("hidden");
            populateUSServices();
        }
        if (value === "germany") {
            document.getElementById("german-service").classList.remove("hidden");
            populateGermanServices();
        }
        if (value === "other") {
            document.getElementById("other-service").classList.remove("hidden");
            populateOtherServices();
        }
    });

    // --- US Service Search ---
    document.getElementById("us-service-search").addEventListener("input", function () {
        const val = this.value.toLowerCase();
        const listEl = document.getElementById("us-service-list");
        listEl.querySelectorAll("button").forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(val) ? "block" : "none";
        });
        listEl.classList.remove("hidden");
    });

    document.getElementById("us-area-code-search").addEventListener("input", function () {
        const val = this.value.toLowerCase();
        const listEl = document.getElementById("us-area-code-list");
        listEl.querySelectorAll("button").forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(val) ? "block" : "none";
        });
        listEl.classList.remove("hidden");
    });

    // --- German Service Search ---
    document.getElementById("german-service-search").addEventListener("input", function () {
        const val = this.value.toLowerCase();
        const listEl = document.getElementById("german-service-list");
        listEl.querySelectorAll("button").forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(val) ? "block" : "none";
        });
        listEl.classList.remove("hidden");
    });

    // --- Other Service Search ---
    document.getElementById("other-service-search").addEventListener("input", function () {
        const val = this.value.toLowerCase();
        const listEl = document.getElementById("other-service-list");
        listEl.querySelectorAll("button").forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(val) ? "block" : "none";
        });
        listEl.classList.remove("hidden");
    });

    // Close dropdowns when clicking outside
    document.addEventListener("click", function (e) {
        ["us-service", "german-service", "other-service"].forEach(serviceId => {
            const container = document.getElementById(serviceId);
            if (container && !container.contains(e.target)) {
                const listEl = container.querySelector(".service-dropdown");
                if (listEl) listEl.classList.add("hidden");
            }
        });
    });
