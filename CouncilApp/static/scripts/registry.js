async function loadRecords() {
    const search = document.getElementById('regSearch').value;
    const res = await fetch(`/api/records?search=${encodeURIComponent(search)}`);
    const data = await res.json();
    
    const body = document.getElementById('tableBody');
    body.innerHTML = '';

    data.forEach(row => {
        body.innerHTML += `
            <tr>
                <td class="row-actions">
                    <button class="btn-edit" onclick='editRecord(${JSON.stringify(row)})'>Edit</button>
                    <button class="btn-del" onclick="deleteRecord(${row.id})">Delete</button>
                </td>
                <td style="font-weight:800; color:var(--primary);">${row.Ref_No}</td>
                <td>${row.Date_Received}</td>
                <td>${row.Proponent}</td>
                <td title="${row.Subject}">${row.Subject.substring(0, 50)}...</td>
                <td>${row.Type}</td>
            </tr>
        `;
    });
}

function openAddModal() {
    document.getElementById('recordForm').reset();
    document.getElementById('record_id').value = '';
    document.getElementById('modalTitle').innerText = "Add New Record";
    document.getElementById('recordModal').showModal();
}

async function saveRecord(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.from_timestamp(formData.entries());
    const recordId = document.getElementById('record_id').value;
    if(recordId) data.id = recordId;

    await fetch('/api/records', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    document.getElementById('recordModal').close();
    loadRecords();
}

async function deleteRecord(id) {
    if(confirm("Delete this record permanently?")) {
        await fetch(`/api/records/${id}`, { method: 'DELETE' });
        loadRecords();
    }
}

// Initial Load
document.addEventListener('DOMContentLoaded', loadRecords);