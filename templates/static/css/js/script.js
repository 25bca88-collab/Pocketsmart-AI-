// PocketSmart AI - Main JavaScript

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // Form Loading Effect
    // -----------------------------
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {

            const submitButton = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;

                if (submitButton.tagName === "BUTTON") {
                    submitButton.innerHTML =
                        '<span class="spinner"></span> Generating...';
                } else {
                    submitButton.value = "Generating...";
                }
            }
        });
    });


    // -----------------------------
    // Image Preview
    // -----------------------------
    const imageInput = document.getElementById("image");

    if (imageInput) {
        imageInput.addEventListener("change", function () {

            const file = this.files[0];

            if (!file) {
                return;
            }

            if (!file.type.startsWith("image/")) {
                alert("Please select a valid image file.");
                this.value = "";
                return;
            }

            const maxSize = 5 * 1024 * 1024;

            if (file.size > maxSize) {
                alert("Image size must be less than 5 MB.");
                this.value = "";
                return;
            }

            const preview = document.getElementById("image-preview");

            if (preview) {
                preview.src = URL.createObjectURL(file);
                preview.style.display = "block";
            }
        });
    }


    // -----------------------------
    // Password Confirmation
    // -----------------------------
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");

    if (password && confirmPassword) {

        confirmPassword.addEventListener("input", function () {

            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity(
                    "Passwords do not match."
                );
            } else {
                confirmPassword.setCustomValidity("");
            }

        });
    }


    // -----------------------------
    // Mobile Menu
    // -----------------------------
    const menuButton = document.getElementById("menu-button");
    const navigation = document.getElementById("navigation");

    if (menuButton && navigation) {

        menuButton.addEventListener("click", function () {
            navigation.classList.toggle("active");
        });

    }


    // -----------------------------
    // Auto Hide Messages
    // -----------------------------
    const messages = document.querySelectorAll(
        ".alert, .success-message, .error-message"
    );

    messages.forEach(function (message) {

       