document.addEventListener('DOMContentLoaded', fetchRecords);

function fetchRecords() {
    const search = document.getElementById('searchInput').value;
    
    fetch(`/api/records?search=${encodeURIComponent(search)}`)
    .then(res => res.json())
    .then(data => {
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No records found in local database.</td></tr>';
            return;
        }

        data.forEach(row => {
            // Encode the row data into JSON string to pass it cleanly to the edit function
            const rowData = encodeURIComponent(JSON.stringify(row));
            
            tbody.innerHTML += `
                <tr>
                    <td style="font-weight:bold;">${row.Ref_No || 'N/A'}</td>
                    <td>${row.Date_Received || ''}</td>
                    <td>${row.Proponent || ''}</td>
                    <td>${row.Subject || ''}</td>
                    <td>${row.Type || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="openRecordModal('${rowData}')">Edit</button>
                        <button class="btn-del" onclick="deleteRecord(${row.id})">Delete</button>
                    </td>
                </tr>
            `;
        });
    });
}

function openRecordModal(rowData = null) {
    document.getElementById('recordModal').classList.add('active');
    
    if (rowData) {
        document.getElementById('modalTitle').innerText = "Edit Record";
        const data = JSON.parse(decodeURIComponent(rowData));
        document.getElementById('recordId').value = data.id;
        document.getElementById('Ref_No').value = data.Ref_No;
        document.getElementById('Date_Received').value = data.Date_Received;
        document.getElementById('Type').value = data.Type;
        document.getElementById('Proponent').value = data.Proponent;
        document.getElementById('Subject').value = data.Subject;
    } else {
        document.getElementById('modalTitle').innerText = "Add New Record";
        document.getElementById('recordForm').reset();
        document.getElementById('recordId').value = '';
    }
}

function closeRecordModal() {
    document.getElementById('recordModal').classList.remove('active');
}

function saveRecord() {
    const data = {
        id: document.getElementById('recordId').value || null,
        Ref_No: document.getElementById('Ref_No').value,
        Date_Received: document.getElementById('Date_Received').value,
        Type: document.getElementById('Type').value,
        Proponent: document.getElementById('Proponent').value,
        Subject: document.getElementById('Subject').value
    };

    fetch('/api/records', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        if (res.status === 'success') {
            closeRecordModal();
            fetchRecords(); // Refresh table
        }
    });
}

function deleteRecord(id) {
    if (confirm("Are you sure you want to delete this record locally?")) {
        fetch(`/api/records/${id}`, { method: 'DELETE' })
        .then(() => fetchRecords());
    }
}