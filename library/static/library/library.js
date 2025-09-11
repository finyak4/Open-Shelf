document.addEventListener("DOMContentLoaded", () => {
  const newBookBtn = document.querySelector(".new-book-button-div");
  const newBookForm = document.querySelector(".add-book-form");
  const pageContent = document.querySelector("main");
  const body = document.body;
  let btn = newBookBtn.querySelector("button");

  newBookBtn.addEventListener("click", () => {
    newBookForm.classList.toggle("hidden");
    if (btn) {
      if (btn.innerText === "Close") {
        btn.innerText = "New Book";
      } else {
        btn.innerText = "Close";
      }
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const carouselDiv = document.querySelector(".carousel-div");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const container = document.querySelector(".carousel-container");
  const genres = [
    "Fiction",
    "Non-fiction",
    "Mystery",
    "Fantasy",
    "Biography",
    "Science",
    "History",
    "Romance",
    "Thriller",
    "Poetry",
    "Horror",
    "Classic",
    "Self-development",
    "Novel",
  ];
  let scrollPosition = 2;
  let autoScrollInterval = null;

  prevBtn.addEventListener("click", () => {
    if (scrollPosition > 2) scrollPosition--;
    if (scrollPosition == 2) scrollPosition = genres.length - 2;
    updateCarousel();
  });

  nextBtn.addEventListener("click", () => {
    if (scrollPosition < genres.length - 2) scrollPosition++;
    if (scrollPosition == genres.length - 2) scrollPosition = 2;
    updateCarousel();
  });

  function updateCarousel() {
    carouselDiv.innerHTML = "";
    for (let i = scrollPosition - 2; i < scrollPosition + 2; i++) {
      if (i >= 0 && i < genres.length) {
        const a = document.createElement("a");
        a.textContent = genres[i];
        a.href = "/library/?genre=" + encodeURIComponent(genres[i]);
        carouselDiv.appendChild(a);

        void a.offsetWidth;
        a.classList.add("show");
      }
    }
  }

  function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
      if (scrollPosition < genres.length - 2) {
        scrollPosition++;
      } else {
        scrollPosition = 2;
      }
      updateCarousel();
    }, 2000);
  }

  function stopAutoScroll() {
    clearInterval(autoScrollInterval);
  }

  carouselDiv.addEventListener("mouseenter", stopAutoScroll);
  carouselDiv.addEventListener("mouseleave", startAutoScroll);

  updateCarousel();
  startAutoScroll();
});




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


$(document).ready(function() {
  $('#id_genre').select2({
    tags: true,
    placeholder: "Select or type a genre",
    allowClear: true
  });
});
