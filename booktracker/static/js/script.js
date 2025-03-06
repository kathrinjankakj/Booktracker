/*
const bookForm = document.getElementById('book-form');
if (bookForm) {
    bookForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const author = document.getElementById('author').value;
        const pages = document.getElementById('basic').value;

        if (title && author && pages) {
            const bookList = document.getElementById('book-list');
            const bookItem = document.createElement('div');
            bookItem.classList.add('book-item');
            bookItem.innerHTML = `<div>
                                    <strong>${title}</strong> by ${author} - ${pages} Seiten
                                  </div>
                                  <div>
                                    <button class="like-btn">👍</button>
                                    <button class="remove-btn">Entfernen</button>
                                  </div>`;

            bookList.appendChild(bookItem);

            // Like Funktion
            bookItem.querySelector('.like-btn').addEventListener('click', function () {
                this.classList.toggle('liked');
            });

            // Entfernen Funktion
            bookItem.querySelector('.remove-btn').addEventListener('click', function () {
                bookItem.remove();
            });

            bookForm.reset();
        }
    });
}
*/

/*// Profilseite speichern
const profileForm = document.getElementById('profile-form');
if (profileForm) {
    profileForm.addEventListener('submit', function (e) {
        e.preventDefault();
        alert('Profilinformationen gespeichert!');
    });
}*/

// Einstellungen speichern
const settingsForm = document.getElementById('settings-form');
if (settingsForm) {
    settingsForm.addEventListener('submit', function (e) {
        e.preventDefault();
        alert('Einstellungen gespeichert!');
    });
}

/*
// Suche und Sortieren
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', function () {
    const filter = searchInput.value.toLowerCase();
    const books = document.querySelectorAll('.book-item');
    books.forEach(book => {
        const text = book.textContent.toLowerCase();
        book.style.display = text.includes(filter) ? '' : 'none';
    });
});

const sortButton = document.getElementById('sort');
sortButton.addEventListener('click', function () {
    const books = Array.from(document.querySelectorAll('.book-item'));
    books.sort((a, b) => a.textContent.localeCompare(b.textContent));
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = '';
    books.forEach(book => bookList.appendChild(book));
});
*/
