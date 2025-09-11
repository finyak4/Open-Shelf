const id = document.getElementById("book-info").dataset.id;
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
document.addEventListener("DOMContentLoaded", () => {
  let editBtn = document.querySelector(".edit-book-button");
  if (editBtn) {
    const editForm = ` <div class="edit-book-form hidden">
            <button id="close">Close</button>
            <div class="edit-book-item">
                <input type="text" id="edit-title" name="title" placeholder=" ">
                <label for="edit-title">Title</label>
            </div>
            <div class="edit-book-item">
                <input type="text" id="edit-description" name="description" placeholder=" ">
                <label for="edit-description">Description</label>
            </div>
            <div class="edit-book-item">
                <input type="text" id="edit-author" name="author" placeholder=" ">
                <label for="edit-author">Author</label>
            </div>
            <div class="edit-book-item">
                <input type="number" id="edit-availability" name="availability" placeholder=" ">
                <label for="edit-availability">Availability</label>
            </div>
            <div class="edit-book-item">
                <input type="number" id="edit-year" name="year" placeholder=" ">
                <label for="edit-year">Year</label>
            </div>
            <div class="edit-book-item">
                <input type="url" id="edit-url" name="url" placeholder=" ">
                <label for="edit-url">Cover URL</label>
            </div>
            <div class="edit-book-item">
                <select id="edit-genre" name="genre" placeholder=" ">
                    <option value="fiction">Fiction</option>
                    <option value="non-fiction">Non-fiction</option>
                    <option value="mystery">Mystery</option>
                    <option value="fantasy">Fantasy</option>
                    <option value="biography">Biography</option>
                    <option value="science">Science</option>
                    <option value="history">History</option>
                    <option value="romance">Romance</option>
                    <option value="thriller">Thriller</option>
                    <option value="poetry">Poetry</option>
                    <option value="horror">Horror</option>
                    <option value="classic">Classic</option>
                    <option value="self-development">Self-development</option>
                    <option value="novel">Novel</option>
                </select>
                <label for="edit-genre">Genre</label>
            </div>
            <button id="save" type="submit">Save</button>`;
    document
      .querySelector(".edit-book-button-div")
      .insertAdjacentHTML("beforeend", editForm);
    const form = document.querySelector(".edit-book-form");
    editBtn.addEventListener("click", () => {
      form.classList.remove("hidden");
      document.querySelector("#close").addEventListener("click", () => {
        form.classList.add("hidden");
      });
      document.getElementById("edit-title").value = editBtn.dataset.title;
      document.getElementById("edit-author").value = editBtn.dataset.author;
      document.getElementById("edit-description").value =
        editBtn.dataset.description;
      document.getElementById("edit-year").value = editBtn.dataset.year;
      document.getElementById("edit-availability").value =
        editBtn.dataset.availability;
      document.getElementById("edit-url").value = editBtn.dataset.url;
      document.getElementById("edit-genre").value = editBtn.dataset.genre;
    });
    const saveBtn = document.querySelector("#save");
    saveBtn.addEventListener("click", () => {
      let title = document.getElementById("edit-title").value;
      let author = document.getElementById("edit-author").value;
      let description = document.getElementById("edit-description").value;
      let year = document.getElementById("edit-year").value;
      let availability = document.getElementById("edit-availability").value;
      let url = document.getElementById("edit-url").value;
      let genre = document.getElementById("edit-genre").value;
      updatedBook = {
        title: title,
        author: author,
        description: description,
        year: year,
        availability: availability,
        url: url,
        genre: genre,
      };
      fetch(`/library/book/${id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(updatedBook),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Failed to update");
        })
        .then(() => {
          form.classList.add("hidden");

          // Update DOM
          document.querySelector(".book-info-title").textContent = title;
          document.querySelector(".book-info-author").textContent = author;
          document.querySelector(".book-info-year").textContent = year;
          if (document.querySelector("#availability")) {
            document.querySelector("#availability").textContent =
              availability + " available";
          }
          document.querySelector(".book-info-genre").textContent =
            "Genre: " + genre;
          document.querySelector(".book-info-description").textContent =
            description;

          // Update data set
          editBtn.dataset.title = title;
          editBtn.dataset.author = author;
          editBtn.dataset.description = description;
          editBtn.dataset.year = year;
          editBtn.dataset.availability = availability;
          editBtn.dataset.url = url;
          editBtn.dataset.genre = genre;
        });
    });
  }
});

const reserveBtn = document.getElementById("reserve");
if (reserveBtn) {
  reserveBtn.addEventListener("click", () => {
    const confirmReservation =
      confirm(`Are you sure you want to reserve this book?
    You will have 3 hours to collect a book from library!`);
    if (!confirmReservation) return;

    fetch(`/library/reservation/${id}/reserve/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Reservation failed");
        return res.json();
      })
      .then((data) => {
        alert("Book reserved successfully!");
        const availabilityElem = document.querySelector("#availability");
        if (availabilityElem) {
          
          const match = availabilityElem.textContent.match(/\d+/);
          if (match) {
            let availability = parseInt(match[0]);
            availability--; 
            availabilityElem.textContent = `${availability} available`;
          }
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Something went wrong.");
      });
  });
}

