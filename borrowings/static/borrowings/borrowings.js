const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".return").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.id;

      const confirmReservation = confirm(`Did user return books?`);
      if (!confirmReservation) return;

      fetch(`/borrowings/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ id: id }),
      });
    });
  });
});
function changeBtn(btn) {
  if (btn.innerText === "Close") {
    btn.innerText = "Borrow";
  } else {
    btn.innerText = "Close";
  }
}

const borrowBtn = document.querySelector(".borrow-button");
const borrowForm = document.querySelector(".borrow-form");
borrowBtn.addEventListener("click", () => {
  borrowForm.classList.toggle("hidden");
  changeBtn(borrowBtn);
});

const inputUser = document.getElementById("autocomplete");
const suggestionBox = document.getElementById("suggestions");

inputUser.addEventListener("input", () => {
  const query = inputUser.value;
  if (query.length === 0) {
    suggestionBox.innerHTML = "";
    return;
  }
  fetch(`/borrowings/autocomplete/?q=${encodeURIComponent(query)}`)
    .then((res) => res.json())
    .then((data) => {
      suggestionBox.innerHTML = "";
      data.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item.username;
        li.onclick = () => {
          inputUser.value = item.username;
          suggestionBox.innerHTML = "";
        };
        suggestionBox.appendChild(li);
      });
    });
});

const inputBook = document.getElementById("book-autocomplete");
const bookSuggestions = document.getElementById("suggestion-books");
const selectedBooks = new Map();

inputBook.addEventListener("input", () => {
  const query = inputBook.value;
  if (query.length === 0) {
    suggestionBox.innerHTML = "";
    return;
  }
  fetch(`/borrowings/autocomplete_books/?q=${encodeURIComponent(query)}`)
    .then((res) => res.json())
    .then((data) => {
      bookSuggestions.innerHTML = "";
      data.forEach((book) => {
        const li = document.createElement("li");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = book.id;

        checkbox.checked = selectedBooks.has(book.id);

        checkbox.addEventListener("change", () => {
          if (checkbox.checked) {
            selectedBooks.set(book.id, book.title);
          } else {
            selectedBooks.delete(book.id);
          }
          renderSelectedBooks();
        });

        const label = document.createElement("label");
        label.textContent = `${book.id}: ${book.title}`;

        li.appendChild(checkbox);
        li.appendChild(label);
        bookSuggestions.appendChild(li);
      });
    });
});

function renderSelectedBooks() {
  const selectedDiv = document.getElementById("selected-books");
  if (!selectedDiv) return;
  selectedDiv.innerHTML = "";

  selectedBooks.forEach((title, id) => {
    const div = document.createElement("div");
    div.textContent = `${id}: ${title}`;
    selectedDiv.appendChild(div);
  });

  // Optional: update hidden input if submitting form
  const hiddenInput = document.getElementById("selected-book-ids");
  if (hiddenInput) {
    hiddenInput.value = [...selectedBooks.keys()].join(",");
  }
}

const submitBorrow = document.getElementById("submit-borrow");

submitBorrow.addEventListener("click", () => {
  const selectedUser = inputUser.value.trim();
  const selectedBookIds = [...selectedBooks.keys()];
  fetch("/borrowings/borrow_man/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      user: selectedUser,
      books: selectedBookIds,
    }),
  }).then(() => {
    borrowForm.classList.toggle("hidden");
    changeBtn(borrowBtn);
  });
});
