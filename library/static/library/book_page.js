const id = document.getElementById("book-info").dataset.id;
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
document.addEventListener("DOMContentLoaded", () => {
  let editBtn = document.querySelector(".edit-book-button");
  if (editBtn) {
    const form = document.querySelector(".edit-book-form");
    editBtn.addEventListener("click", () => {
      form.classList.remove("hidden");
      document.querySelector("#close").addEventListener("click", () => {
        form.classList.add("hidden");
      });
    });
  }
});

// const reserveBtn = document.getElementById("reserve");
// if (reserveBtn) {
//   reserveBtn.addEventListener("click", () => {
//     const confirmReservation =
//       confirm(`Are you sure you want to reserve this book?
//     You will have 3 hours to collect a book from library!`);
//     if (!confirmReservation) return;

//     fetch(`/library/reservation/${id}/reserve/`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": csrfToken,
//       },
//     })
//       .then((res) => {
//         if (!res.ok) throw new Error("Reservation failed");
//         return res.json();
//       })
//       .then((data) => {
//         alert("Book reserved successfully!");
//         const availabilityElem = document.querySelector("#availability");
//         if (availabilityElem) {
          
//           const match = availabilityElem.textContent.match(/\d+/);
//           if (match) {
//             let availability = parseInt(match[0]);
//             availability--; 
//             availabilityElem.textContent = `${availability} available`;
//           }
//         }
//       })
//       .catch((err) => {
//         console.error(err);
//         alert("Something went wrong.");
//       });
//   });
// }

