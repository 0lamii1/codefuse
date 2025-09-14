async function populateUSServices() {
    const listEl = document.getElementById("us-service-list");
    const searchInput = document.getElementById("us-service-search");
    const costInput = document.getElementById("max-cost");

    listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>Loading...</p>";

    try {
        const res = await fetch("/api/services/us/numbers");
        if (!res.ok) throw new Error("Failed to fetch US services");

        const data = await res.json();
        renderUSServices(data);

        // --- search by name or price ---
        searchInput.addEventListener("input", () => {
            renderUSServices(data, searchInput.value, costInput.value);
        });

        // --- filter by cost field ---
        costInput.addEventListener("input", () => {
            renderUSServices(data, searchInput.value, costInput.value);
        });

    } catch (err) {
        listEl.innerHTML = `<p class='px-4 py-2 text-red-500'>Error loading services</p>`;
        console.error(err);
    }
}

function renderUSServices(data, searchVal = "", costVal = "") {
    const listEl = document.getElementById("us-service-list");
    const searchInput = document.getElementById("us-service-search");
    const costInput = document.getElementById("max-cost");

    const search = searchVal.toLowerCase().trim();
    const costFilter = costVal ? parseInt(costVal, 10) : null;

    listEl.innerHTML = "";

    const filtered = data.filter(s => {
        const matchName = s.service_name.toLowerCase().includes(search) || s.cost.toString().includes(search);
        const matchCost = costFilter ? s.cost <= costFilter : true;
        return matchName && matchCost;
    });

    if (filtered.length === 0) {
        listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>No matching services</p>";
        listEl.classList.remove("hidden");
        return;
    }

    filtered.forEach(service => {
        const btn = document.createElement("button");
        btn.textContent = `${service.service_name} - ₦${service.cost}`;
        btn.className = "block w-full text-left px-4 py-2 hover:bg-blue-100";
        btn.onclick = () => {
            searchInput.value = service.service_name;
            searchInput.setAttribute("data-label", service.service_code);
            costInput.value = service.cost;
            listEl.classList.add("hidden");
        };
        listEl.appendChild(btn);
    });

    listEl.classList.remove("hidden");
}


// --- Fetch US area code from restcountries ---
async function getUSAreaCode() {
    const listEl = document.getElementById("us-area-code-list");
    const inputEl = document.getElementById("us-area-code-search");

    listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>Loading...</p>";
    listEl.classList.remove("hidden");

    try {
        const res = await fetch("https://restcountries.com/v3.1/name/united states");
        if (!res.ok) throw new Error("Failed to fetch US country data");

        const data = await res.json();
        const root = data[0].idd.root;          // "+1"
        const suffixes = data[0].idd.suffixes;  // ["201","202",...]
        const allCodes = suffixes.map(suffix => root + suffix);   // "+1201"
        const allCodesData = suffixes.map(suffix => suffix);      // "201"

        // --- render + filter ---
        function renderAreaCodes(filter = "") {
            listEl.innerHTML = "";
            const search = filter.trim();

            // Limit to 30 results for performance
            const filtered = allCodes
                .map((code, idx) => ({ text: code, value: allCodesData[idx] }))
                .filter(item => item.text.includes(search))
                .slice(0, 30);

            if (filtered.length === 0) {
                listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>No matching codes</p>";
                listEl.classList.remove("hidden");
                return;
            }

            filtered.forEach(item => {
                const btn = document.createElement("button");
                btn.textContent = `US Area Code: ${item.text}`;  // show full code
                btn.className = "block w-full text-left px-4 py-2 hover:bg-blue-100";
                btn.onclick = () => {
                    inputEl.value = item.text;  // show user the full code
                    inputEl.setAttribute("data-value", item.value); // save suffix as value
                    inputEl.setAttribute("data-label", item.text);  // save full code as label
                    listEl.classList.add("hidden");
                };
                listEl.appendChild(btn);
            });

            listEl.classList.remove("hidden");
        }

        // Initial render
        renderAreaCodes();

        // Bind once for live search
        inputEl.addEventListener("input", () => {
            renderAreaCodes(inputEl.value);
        });

    } catch (err) {
        listEl.innerHTML = `<p class="px-4 py-2 text-red-500">Error loading US area code</p>`;
        console.error("Error fetching US area code:", err);
    }
}





async function getUsNumber(service_code, amount) {
    try {
        let url = "";

        if (!amount) {
            url = `api/services/us/numbers/${service_code}`;
        } else {
            url = `api/services/us/numbers/${service_code}/${amount}`;
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error("Number not available");

        const data = await response.json();
        const parts = data.number_info.split(":");

        const activationId = parts[1];   // e.g. 352585969
        const phoneNumber = parts[2];    // e.g. 17577154078

        return { activationId, phoneNumber };
    } catch (err) {
        console.error("Error fetching US number:", err);
        return null;
    }
}

async function rent(service_code, amount) {
    const number = await getUsNumber(service_code, amount);

    if (!number) {
        alert("Error: Could not fetch number.");
        return;
    }

    if (!number.phoneNumber) {
        alert("No number available for this selection.");
        return;
    }

    try {
        const res = await fetch(`api/services/us/numbers/rent/request/${number.activationId}`);
        if (!res.ok) {
            console.error("Failed to rent number");
            alert("Failed to rent number. Try again.");
        } else {
            alert(`Request successful! Hold on for the code. \n\nPhone: ${number.phoneNumber}`);
        }
    } catch (err) {
        console.error("Error renting number:", err);
        alert("Unexpected error while renting number.");
    }
}

const rent_button = document.getElementById("rent-us-number");
rent_button.addEventListener("click", () => {
    const searchInput = document.getElementById("us-service-search");
    const costInput = document.getElementById("max-cost");

    const service_code = searchInput.getAttribute("data-label"); // ✅ service_code
    const amount = costInput.value; // price/amount

    if (!service_code) {
        alert("Please select a service first.");
        return;
    }

    rent(service_code, amount);
});
