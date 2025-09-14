// Fetch Other services from backend
async function fetchAllOtherServices() {
    try {
        const res = await fetch('/api/services/others/numbers');
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        const arr = [];
        Object.keys(data).forEach(serviceCode => {
            Object.keys(data[serviceCode]).forEach(countryCode => {
                const s = data[serviceCode][countryCode];
                arr.push({ service_code: serviceCode, country_code: countryCode, name: s.name });
            });
        });
        return arr;
    } catch (e) { console.error(e); return []; }
}

// Populate Other services dropdown
async function populateOtherServices() {
    const listEl = document.getElementById('serviceList');
    listEl.innerHTML = '';
    const services = await fetchAllOtherServices();

    if (services.length === 0) {
        listEl.innerHTML = '<div class="px-4 py-2 text-gray-500">No services available</div>';
        return;
    }

    services.forEach(s => {
        const btn = document.createElement('button');
        btn.textContent = s.name;
        btn.className = 'block w-full text-left px-4 py-2 hover:bg-gray-100';
        btn.onclick = () => selectService('other', s.name, s.service_code);
        listEl.appendChild(btn);
    });
}

// Filter Other services
document.addEventListener('DOMContentLoaded', () => {
    const search = document.getElementById('service-search');
    const listEl = document.getElementById('serviceList');
    if (!search) return;

    search.addEventListener('input', () => {
        const val = search.value.toLowerCase();
        listEl.querySelectorAll('button').forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(val) ? 'block' : 'none';
        });

        const visible = Array.from(listEl.querySelectorAll('button')).some(b => b.style.display === 'block');
        if (visible) {
            listEl.classList.remove('dropdown-hidden');
            listEl.classList.add('dropdown-visible');
        } else {
            listEl.classList.add('dropdown-hidden');
            listEl.classList.remove('dropdown-visible');
        }
    });

    document.addEventListener('click', (e) => {
        if (!listEl.contains(e.target) && e.target !== search) {
            listEl.classList.add('dropdown-hidden');
            listEl.classList.remove('dropdown-visible');
        }
    });
});
