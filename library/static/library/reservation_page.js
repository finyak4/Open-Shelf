const id = document.getElementById("book-info").dataset.id;
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

const timerDiv = document.getElementById("reservation-timer");
const createdTime = new Date(timerDiv.dataset.created); // parse ISO string
const deadline = new Date(createdTime.getTime() + 3 * 60 * 60 * 1000); // 3 hours later

function updateTimer() {
  const now = new Date();
  const diff = deadline - now;

  if (diff <= 0) {
    timerDiv.textContent = "Reservation expired";
    clearInterval(interval);
    fetch(`/library/reservation/${id}/reserve/`, {
      method: "DELETE",
      headers: {
        'X-CSRFToken': csrfToken,
        "Content-Type": "application/json",
      },
    });
  }

  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  timerDiv.textContent = `Time to colect: ${hours}h ${minutes}m ${seconds}s`;
}

updateTimer();
const interval = setInterval(updateTimer, 1000); // update every second


const dropdownBtn = document.querySelector(".dropdown-btn")
const dropdownContent = document.querySelector(".dropdown-content")

dropdownBtn.addEventListener("click", ()=>{
  dropdownContent.classList.toggle("drop-content")
})

document.addEventListener("click", (e) => {
  if (!dropdownContent.contains(e.target) && !dropdownBtn.contains(e.target)) {
    dropdownContent.classList.remove("drop-content");
  }
});