document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('apply-filters');
    if (!btn) return;

    btn.addEventListener('click', () => {
        let serviceName = '', serviceCode = '';
        if (selectedCountry === 'US') serviceName = selectedUSService;
        else if (selectedCountry === 'DE') serviceName = selectedGermanService;
        else if (selectedCountry === 'OTHER') { serviceName = selectedOtherServiceName; serviceCode = selectedOtherServiceCode; }

        if (!serviceName) {
            alert('Please select a service.');
            return;
        }

        const countryCode = document.getElementById('code').value;
        const maxCost = document.getElementById('max-cost').value;

        console.log({ country: selectedCountry, service: serviceName, service_code: serviceCode, countryCode, maxCost });
        alert(`Purchasing ${serviceName} for ${selectedCountry}`);
    });
});
