// Global variables
let usServicesData = [];
let currentPhoneNumber = ''; // Store the phone number for modal display
let currentActivationId = ''; // Store activation ID for renting

// Enhanced Modal and Button Loading Script
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('rentModal');
    const successToast = document.getElementById('successToast');

    // Button loading function
    function setButtonLoading(button, loading) {
        if (loading) {
            button.disabled = true;
            button.classList.add('btn-loading');
            button.setAttribute('data-original-text', button.textContent);
            button.textContent = 'Processing...';
        } else {
            button.disabled = false;
            button.classList.remove('btn-loading');
            const originalText = button.getAttribute('data-original-text');
            if (originalText) {
                button.textContent = originalText;
            }
        }
    }

    // Show modal with phone number and Rent/Cancel options
    function showPhoneNumberModal(phoneNumber, message = "Number found! Do you want to rent this number?") {
        const modalMessage = document.getElementById('modalMessage');
        modalMessage.innerHTML = `
            <div class="text-center">
                <p class="text-lg font-semibold text-green-600 mb-4">${message}</p>
                <div class="bg-gray-100 p-4 rounded-lg mb-4">
                    <p class="text-sm text-gray-600 mb-2">Your phone number:</p>
                    <p class="text-2xl font-bold text-blue-700">${phoneNumber}</p>
                </div>
                <div class="flex justify-center gap-4 mt-4">
                    <button id="confirmRentBtn" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                        Rent Now
                    </button>
                    <button id="cancelModalBtn" class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">
                        Cancel
                    </button>
                </div>
            </div>
        `;

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';

        // Attach handlers dynamically
        document.getElementById('confirmRentBtn').addEventListener('click', async () => {
            setButtonLoading(document.getElementById('confirmRentBtn'), true);
            try {
                const res = await fetch(`/api/services/us/numbers/rent/request/${currentActivationId}`);
                if (!res.ok) throw new Error("Failed to rent number");
                showSuccessToast();
                hideModal();
            } catch (err) {
                showErrorModal("Failed to complete rent. Please try again.");
            } finally {
                setButtonLoading(document.getElementById('confirmRentBtn'), false);
            }
        });

        document.getElementById('cancelModalBtn').addEventListener('click', hideModal);
    }

    // Show error modal
    function showErrorModal(message) {
        const modalMessage = document.getElementById('modalMessage');
        modalMessage.innerHTML = `
            <div class="text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                    <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </div>
                <p class="text-lg font-semibold text-red-600 mb-4">Error</p>
                <p class="text-gray-600">${message}</p>
            </div>
        `;

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    // Hide modal
    function hideModal() {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }

    // Show success toast
    function showSuccessToast() {
        successToast.classList.add('show');
        setTimeout(() => {
            successToast.classList.remove('show');
        }, 3000);
    }

    // Make functions globally available
    window.showPhoneNumberModal = showPhoneNumberModal;
    window.showErrorModal = showErrorModal;
    window.hideModal = hideModal;
    window.setButtonLoading = setButtonLoading;
    window.showSuccessToast = showSuccessToast;
});

async function populateUSServices() {
    const listEl = document.getElementById("us-service-list");
    listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>Loading...</p>";
    listEl.classList.remove("hidden");

    try {
        const res = await fetch("/api/services/us/numbers");
        if (!res.ok) throw new Error("Failed to fetch US services");

        usServicesData = await res.json();
        renderUSServices(usServicesData);

    } catch (err) {
        listEl.innerHTML = `<p class='px-4 py-2 text-red-500'>Error loading services</p>`;
        console.error(err);
    }
}

function renderUSServices(data, searchVal = "", costVal = "") {
    const listEl = document.getElementById("us-service-list");
    const search = searchVal.toLowerCase().trim();
    const costFilter = costVal ? parseInt(costVal, 10) : null;

    listEl.innerHTML = "";

    const filtered = data.filter(s => {
        const matchName = s.service_name.toLowerCase().includes(search) || 
                         s.cost.toString().includes(search);
        const matchCost = costFilter ? s.cost <= costFilter : true;
        return matchName && matchCost;
    });

    if (filtered.length === 0) {
        listEl.innerHTML = "<p class='px-4 py-2 text-gray-500'>No matching services</p>";
        return;
    }

    filtered.forEach(service => {
        const btn = document.createElement("button");
        btn.textContent = `${service.service_name} - ₦${service.cost}`;
        btn.className = "block w-full text-left px-4 py-2 hover:bg-blue-100";
        btn.onclick = () => {
            const searchInput = document.getElementById("us-service-search");
            searchInput.value = service.service_name;
            searchInput.dataset.serviceCode = service.service_code;
            searchInput.dataset.serviceCost = service.cost;
            listEl.classList.add("hidden");
        };
        listEl.appendChild(btn);
    });

    listEl.classList.remove("hidden");
}

async function getUsNumber(service_code, area_code, amount) {
    try {
        let url = `/api/services/us/numbers/${service_code}/`;
        const params = new URLSearchParams();
        if (amount) params.append("amount", amount);
        if (area_code) params.append("areas", area_code); 

        if ([...params].length > 0) {
            url += "?" + params.toString();
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error("Number not available");

        const data = await response.json();
        const parts = data.number_info.split(":");

        const activationId = parts[1];
        const phoneNumber = parts[2];

        return { activationId, phoneNumber };
    } catch (err) {
        console.error("Error fetching US number:", err);
        return null;
    }
}

async function rentUSNumber(service_code, amount, areaCodes) {
    const number = await getUsNumber(service_code, areaCodes, amount);

    if (!number) {
        window.showErrorModal("Error: Could not fetch number.");
        return false;
    }

    if (!number.phoneNumber) {
        window.showErrorModal("No number available for this selection.");
        return false;
    }

    // Store number & activationId, then show modal
    currentPhoneNumber = number.phoneNumber;
    currentActivationId = number.activationId;
    window.showPhoneNumberModal(number.phoneNumber, "Number found! Do you want to rent this number?");
    return true;
}

// Event listener for US rent button
document.addEventListener('DOMContentLoaded', function() {
    const rentButton = document.getElementById("rent-us-number");
    const spinner = document.getElementById("us-loginSpinner");

    if (rentButton) {
        rentButton.addEventListener("click", async () => {
            const serviceInput = document.getElementById("us-service-search");
            const service_code = serviceInput.dataset.serviceCode;
            const costInput = document.getElementById("us-max-cost");
            const areaCodesHidden = document.getElementById("area-codes-hidden");

            const amount = costInput.value.trim() || serviceInput.dataset.serviceCost;
            const areaCodes = areaCodesHidden.value; 

            if (!service_code) {
                window.showErrorModal("Please select a service first.");
                return;
            }

            // Show spinner and disable button
            spinner.classList.remove("hidden");
            rentButton.disabled = true;

            try {
                await rentUSNumber(service_code, amount, areaCodes);
            } catch (error) {
                console.error("Error in rental process:", error);
                window.showErrorModal("An unexpected error occurred.");
            } finally {
                spinner.classList.add("hidden");
                rentButton.disabled = false;
            }
        });
    }

    // Search functionality
    const searchInput = document.getElementById("us-service-search");
    const costInput = document.getElementById("us-max-cost");

    if (searchInput && costInput) {
        searchInput.addEventListener("input", () => {
            renderUSServices(usServicesData, searchInput.value, costInput.value);
        });

        costInput.addEventListener("input", () => {
            renderUSServices(usServicesData, searchInput.value, costInput.value);
        });
    }
});
