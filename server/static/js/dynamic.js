// Global selected variables
let selectedCountry = '';
let selectedUSService = '';
let selectedGermanService = '';
let selectedOtherServiceName = '';
let selectedOtherServiceCode = '';

// Toggle dropdown helper
function toggleDropdown(id) {
    const el = document.getElementById(id);
    if (!el) return;
    const isHidden = el.classList.contains('dropdown-hidden');

    // Close any open dropdowns
    document.querySelectorAll('.dropdown-visible').forEach(d => {
        d.classList.add('dropdown-hidden');
        d.classList.remove('dropdown-visible');
    });

    if (isHidden) {
        el.classList.remove('dropdown-hidden');
        el.classList.add('dropdown-visible');
    } else {
        el.classList.add('dropdown-hidden');
        el.classList.remove('dropdown-visible');
    }
}

// Country selection
function selectCountry(code, name) {
    selectedCountry = code;
    document.getElementById('selectedCountry').textContent = name;

    // Hide all service sections
    document.getElementById('us-service').classList.add('dropdown-hidden');
    document.getElementById('german-service').classList.add('dropdown-hidden');
    document.getElementById('other-service').classList.add('dropdown-hidden');

    if (code === 'US') {
        document.getElementById('us-service').classList.remove('dropdown-hidden');
        populateUSServices(); // ✅ FIXED: call US services, not "other"
    } 
    else if (code === 'DE') {
        document.getElementById('german-service').classList.remove('dropdown-hidden');
        populateGermanServices(); // ✅ Add this function similar to populateUSServices
    } 
    else if (code === 'OTHER') {
        document.getElementById('other-service').classList.remove('dropdown-hidden');
        populateOtherServices();
    }

    toggleDropdown('countryList'); // ✅ Close the dropdown after selecting
}




