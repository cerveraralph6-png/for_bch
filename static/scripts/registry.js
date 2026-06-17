
let allRecords = [];
let currentPage = 1;
const rowsPerPage = 100; // Limit rendering to 100 rows per page

document.addEventListener("DOMContentLoaded", () => {
    loadRecords();
});

// Load records from the server API
function loadRecords() {
    const searchVal = document.getElementById("regSearch").value;
    const url = `/api/records?search=${encodeURIComponent(searchVal)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            allRecords = data;
            currentPage = 1; // Always reset to page 1 on new searches or reloads
            renderTable();
            updateBadges(data);
        })
        .catch(err => console.error("Error fetching records: ", err));
}
// Render dynamic table rows sliced to the current page view with numbered pagination
function renderTable() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = "";

    const totalRecords = allRecords.length;
    const totalPages = Math.ceil(totalRecords / rowsPerPage) || 1;

    // Bounds checking
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    // Slice array bounds based on current page
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, totalRecords);
    const pageData = allRecords.slice(startIndex, endIndex);

    pageData.forEach(record => {
        const tr = document.createElement("tr");
        
        tr.innerHTML = `
            <td><input type="checkbox" value="${record.id}"></td>
            <td class="clickable-cell">${record.Date_Received || 'N/A'}</td>
            <td class="clickable-cell">${record.Type || 'N/A'}</td>
            <td class="clickable-cell">${record.Proponent || 'N/A'}</td>
            <td class="clickable-cell">${record.Subject || 'N/A'}</td>
            <td class="clickable-cell">${record.Action_Taken || 'Pending'}</td>
            <td>
                <button onclick="openEditModal(${record.id})" style="background:none; border:none; color:#3498db; cursor:pointer; padding:0 4px;">Edit</button> | 
                <button onclick="deleteRecord(${record.id}, '${record.Proponent}')" style="background:none; border:none; color:#e74c3c; cursor:pointer; padding:0 4px;">Delete</button>
            </td>
        `;

        // Attach modal trigger click listener to content cells
        tr.querySelectorAll(".clickable-cell").forEach(cell => {
            cell.style.cursor = "pointer";
            cell.addEventListener("click", () => {
                openEditModal(record.id);
            });
        });

        tableBody.appendChild(tr);
    });

    // Update Pagination Info
    const infoText = totalRecords > 0 
        ? `Showing ${startIndex + 1}-${endIndex} of ${totalRecords} entries`
        : "Showing 0-0 of 0 entries";
    document.getElementById("paginationInfo").innerText = infoText;

    // Generate Dynamic Page Buttons
    renderPaginationButtons(totalPages, totalRecords);
}

// Generates << < 1 2 3 > >> buttons dynamically
function renderPaginationButtons(totalPages, totalRecords) {
    const container = document.getElementById("paginationButtons");
    container.innerHTML = "";

    if (totalRecords === 0) return;

    // Styling configuration helper
    const applyButtonStyles = (btn, isActive, isDisabled) => {
        btn.style.padding = "6px 12px";
        btn.style.border = "1px solid #ccc";
        btn.style.borderRadius = "4px";
        btn.style.fontSize = "13px";
        btn.style.fontWeight = "500";
        btn.style.transition = "all 0.1s ease";

        if (isActive) {
            btn.style.background = "#3498db";
            btn.style.color = "#fff";
            btn.style.borderColor = "#3498db";
            btn.style.cursor = "default";
        } else if (isDisabled) {
            btn.style.background = "#fafafa";
            btn.style.color = "#ccc";
            btn.style.cursor = "not-allowed";
            btn.style.opacity = "0.6";
        } else {
            btn.style.background = "#fff";
            btn.style.color = "#555";
            btn.style.cursor = "pointer";
            // Add simple hover effect dynamically
            btn.onmouseover = () => { btn.style.background = "#f1f2f6"; };
            btn.onmouseout = () => { btn.style.background = "#fff"; };
        }
    };

    // 1. First Page Button (<<)
    const btnFirst = document.createElement("button");
    btnFirst.innerText = "«";
    applyButtonStyles(btnFirst, false, currentPage === 1);
    if (currentPage !== 1) {
        btnFirst.onclick = () => jumpToPage(1);
    }
    container.appendChild(btnFirst);

    // 2. Previous Page Button (<)
    const btnPrev = document.createElement("button");
    btnPrev.innerText = "‹";
    applyButtonStyles(btnPrev, false, currentPage === 1);
    if (currentPage !== 1) {
        btnPrev.onclick = () => jumpToPage(currentPage - 1);
    }
    container.appendChild(btnPrev);

    // 3. Dynamic Numbered Buttons (Up to 5 numbers in a sliding window)
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);

    // Recalculate start page if end page is squeezed close to totalPages limit
    if (endPage - startPage < 4) {
        startPage = Math.max(1, endPage - 4);
    }

    for (let p = startPage; p <= endPage; p++) {
        const btnNum = document.createElement("button");
        btnNum.innerText = p;
        applyButtonStyles(btnNum, p === currentPage, false);
        if (p !== currentPage) {
            btnNum.onclick = () => jumpToPage(p);
        }
        container.appendChild(btnNum);
    }

    // 4. Next Page Button (>)
    const btnNext = document.createElement("button");
    btnNext.innerText = "›";
    applyButtonStyles(btnNext, false, currentPage === totalPages);
    if (currentPage !== totalPages) {
        btnNext.onclick = () => jumpToPage(currentPage + 1);
    }
    container.appendChild(btnNext);

    // 5. Last Page Button (>>)
    const btnLast = document.createElement("button");
    btnLast.innerText = "»";
    applyButtonStyles(btnLast, false, currentPage === totalPages);
    if (currentPage !== totalPages) {
        btnLast.onclick = () => jumpToPage(totalPages);
    }
    container.appendChild(btnLast);
}

// Executes page jumps and resets scroll position
function jumpToPage(pageNumber) {
    currentPage = pageNumber;
    renderTable();
    const tableScroll = document.querySelector(".table-scroll");
    if (tableScroll) tableScroll.scrollTop = 0;
}

// Navigation control
function changePage(direction) {
    currentPage += direction;
    renderTable();
    // Smooth scroll the table container back to top when navigating pages
    const tableScroll = document.querySelector(".table-scroll");
    if (tableScroll) tableScroll.scrollTop = 0;
}


// Update UI Badge Counters
function updateBadges(records) {
    document.getElementById("totalRecords").innerText = `Total: ${records.length}`;
    document.getElementById("filteredRecords").innerText = `Filtered: ${records.length}`;
}

// Modal control: Open blank form
function openAddModal() {
    document.getElementById("modalTitle").innerText = "New Record Entry";
    document.getElementById("recordForm").reset();
    document.getElementById("recordId").value = "";
    document.getElementById("recordModal").style.display = "flex";
}

// Modal control: Open populate form
function openEditModal(recordId) {
    const record = allRecords.find(r => r.id === recordId);
    if (!record) return;

    document.getElementById("modalTitle").innerText = "Edit Record";
    document.getElementById("recordId").value = record.id;

    // Define all 21 properties requested
    const fields = [
        'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
        'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
        'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
        'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
        'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
    ];

    // Bind fields to form inputs
    fields.forEach(field => {
        document.getElementById(field).value = record[field] || "";
    });

    document.getElementById("recordModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("recordModal").style.display = "none";
}

// Save Record Form Submit (supports Edit and Create)
function saveRecord(event) {
    event.preventDefault();

    const recordId = document.getElementById("recordId").value;
    const fields = [
        'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
        'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
        'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
        'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
        'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
    ];

    const payload = {};
    if (recordId) payload.id = parseInt(recordId);

    fields.forEach(field => {
        payload[field] = document.getElementById(field).value;
    });

    fetch("/api/records", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            closeModal();
            loadRecords();
        }
    })
    .catch(err => console.error("Error saving record: ", err));
}

// Delete Record functionality
function deleteRecord(id, proponent) {
    if (confirm(`Are you sure you want to delete the record submitted by "${proponent}"?`)) {
        fetch(`/api/delete-record/${id}`, {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                loadRecords();
            }
        })
        .catch(err => console.error("Error deleting record: ", err));
    }
}

// Add this helper function to the bottom of registry.js
function submitFormTrigger() {
    const form = document.getElementById("recordForm");
    if (form.checkValidity()) {
        form.requestSubmit(); // Triggers the standard saveRecord(event) function
    } else {
        form.reportValidity(); // Highlights missing required inputs
    }
}

// --- ADD THIS TO THE BOTTOM OF REGISTRY.JS ---

// Triggers the hidden file input
function triggerCSVUpload() {
    document.getElementById("csvFileInput").click();
}

// Packages the uploaded file and POSTs to the server API
function handleCSVUpload(inputElement) {
    const file = inputElement.files[0];
    if (!file) return;

    // Client-side verification
    if (!file.name.endsWith(".csv")) {
        alert("Please select a valid .csv file.");
        inputElement.value = ""; // Reset file path
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/api/import_csv", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            loadRecords(); // Reload table grid to show newly imported records
        } else {
            alert("Import failed: " + data.message);
        }
        inputElement.value = ""; // Reset the input to allow uploading same file if needed
    })
    .catch(err => {
        console.error("CSV upload error:", err);
        alert("An error occurred during the file import. Check the server console logs.");
        inputElement.value = ""; // Reset the input
    });
}