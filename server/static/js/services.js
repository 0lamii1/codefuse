

function selectService(country, name, serviceCode = '') {
    if (country === 'us') {
        selectedUSService = name;
        // put selected service name in search box
        document.getElementById('us-service-search').value = name;
        toggleDropdown('us-service-list');
    } else if (country === 'german') {
        selectedGermanService = name;
        document.getElementById('german-service-search').value = name;
        toggleDropdown('german-service-list');
    } else if (country === 'other') {
        selectedOtherServiceName = name;
        selectedOtherServiceCode = serviceCode;
        document.getElementById('other-service-search').value = name;
        toggleDropdown('other-service-list');
    }
}
