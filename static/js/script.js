// Enable Bootstrap dropdowns
document.addEventListener("DOMContentLoaded", function () {
    var dropdowns = document.querySelectorAll('.dropdown-toggle');

    dropdowns.forEach(function (dropdown) {
        dropdown.addEventListener('click', function (e) {
            e.preventDefault();
            this.nextElementSibling.classList.toggle('show');
        });
    });
});

// Auto-hide alert messages after 4 seconds
setTimeout(function () {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = "opacity 1s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 1500);
    });
}, 4000);

// Back to top button (optional)
let backToTop = document.getElementById("back-to-top");

if (backToTop) {
    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            backToTop.style.display = "block";
        } else {
            backToTop.style.display = "none";
        }
    });

    backToTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}
