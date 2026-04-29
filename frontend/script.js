const API_URL = "http://127.0.0.1:8000/notes";

async function fetchNotes() {
    const response = await fetch(API_URL);
    const notes = await response.json();
    const grid = document.getElementById('notes-grid');
    grid.innerHTML = '';
    notes.forEach(note => {
        grid.innerHTML += `
            <div class="note-card">
                <h3>${note.title}</h3>
                <p>${note.content}</p>
                <button onclick="editNote(${note.id}, '${note.title}', '${note.content}')">Edit</button>
                <button onclick="deleteNote(${note.id})">Delete</button>
            </div>
        `;
    });
}

async function createNote() {
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
    });
    fetchNotes();
}

async function deleteNote(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchNotes();
}

async function editNote(id, oldTitle, oldContent) {
    const newTitle = prompt("Edit Title:", oldTitle);
    const newContent = prompt("Edit Content:", oldContent);
    if (newTitle !== null && newContent !== null) {
        await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: newTitle, content: newContent })
        });
        fetchNotes();
    }
}

fetchNotes();
// Replace your existing notes.forEach loop with this:
notes.forEach(note => {
    grid.innerHTML += `
        <div class="note-card">
            <h3>${note.title}</h3>
            <p>${note.content}</p>
            <button onclick="editNote(${note.id}, '${note.title}', '${note.content}')">Edit</button>
            <button onclick="deleteNote(${note.id})">Delete</button>
        </div>
    `;
});