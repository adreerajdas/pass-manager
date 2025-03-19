document.addEventListener("DOMContentLoaded", function() {
    console.log("Dashboard Loaded!");
});

function togglePassword(index) {
    let passwordSpan = document.getElementById(`password-${index}`);
    let eyeButton = document.getElementById(`eye-btn-${index}`);

    if (passwordSpan.dataset.visible === "false") {
        passwordSpan.textContent = passwordSpan.dataset.password;
        passwordSpan.dataset.visible = "true";
        eyeButton.textContent = "👁️"; // Open Eye Icon
    } else {
        passwordSpan.textContent = "••••••";
        passwordSpan.dataset.visible = "false";
        eyeButton.textContent = "🙈"; // Closed Eye Icon
    }
}

