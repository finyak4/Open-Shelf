document.addEventListener("DOMContentLoaded", () => {
  // New Book Button Toggle
  const newBookBtnDiv = document.querySelector(".new-book-button-div");
  const newBookForm = document.querySelector(".add-book-form");
  if (newBookBtnDiv && newBookForm) {
    const btn = newBookBtnDiv.querySelector("button");
    newBookBtnDiv.addEventListener("click", () => {
      newBookForm.classList.toggle("hidden");
      if (btn) {
        btn.innerText = btn.innerText === "Close" ? "New Book" : "Close";
      }
    });
  }

  // Dropdown
  const dropdownBtn = document.querySelector(".dropdown-btn");
  const dropdownContent = document.querySelector(".dropdown-content");
  if (dropdownBtn && dropdownContent) {
    dropdownBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      dropdownContent.classList.toggle("drop-content");
    });

    document.addEventListener("click", (e) => {
      if (!dropdownContent.contains(e.target) && !dropdownBtn.contains(e.target)) {
        dropdownContent.classList.remove("drop-content");
      }
    });
  }

  setTimeout(() => {
  document.querySelectorAll(".error-message").forEach(el => {
    el.classList.add("hide");
    el.addEventListener("transitionend", () => {
      el.style.display = "none";
    });
  });
  }, 2000);

  const scrollBtn = document.getElementById("scrollToTop");

  window.addEventListener("scroll", () => {
    if (window.scrollY > 500) {
      scrollBtn.style.display = "block";
    } else {
      scrollBtn.style.display = "none";
    }
  });

  scrollBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });

});