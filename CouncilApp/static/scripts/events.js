async function loadEvents() {
    const res = await fetch('/api/events');
    const events = await res.json();
    const grid = document.getElementById('eventsGrid');
    
    if (events.length === 0) {
        grid.innerHTML = '<p style="text-align:center; grid-column: 1/-1; padding: 50px; color: #94a3b8;">No scheduled events found.</p>';
        return;
    }

    grid.innerHTML = '';
    events.forEach(ev => {
        const catClass = `cat-${ev.category.toLowerCase()}`;
        grid.innerHTML += `
            <div class="event-card">
                <span class="event-cat ${catClass}">${ev.category}</span>
                <h3>${ev.event_name}</h3>
                <div class="event-meta">
                    <div class="meta-item">📅 ${ev.event_date}</div>
                    <div class="meta-item">🕒 ${ev.event_time}</div>
                    <div class="meta-item">📍 ${ev.location}</div>
                </div>
                <div class="event-footer">
                    <span class="status-pending">● ${ev.status.toUpperCase()}</span>
                    <button class="btn-row-del" onclick="deleteEvent(${ev.id})">Remove</button>
                </div>
            </div>
        `;
    });
}

async function saveEvent(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    await fetch('/api/events', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    document.getElementById('eventModal').close();
    loadEvents();
}

document.addEventListener('DOMContentLoaded', loadEvents);