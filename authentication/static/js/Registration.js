document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
  

    form.addEventListener("submit", function (event) {
        let valid = true;
        let errorMessage = "";

        // Validate name
        if (nameInput.value.trim() === "") {
            valid = false;
            errorMessage += "Name is required.\n";
        }

        // Validate email
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value.trim())) {
            valid = false;
            errorMessage += "Enter a valid email address.\n";
        }

        // Validate password
        if (passwordInput.value.trim().length < 8) {
            valid = false;
            errorMessage += "Password must be at least 8 characters long.\n";
        }

        // If validation fails, show an alert and prevent form submission
        if (!valid) {
            alert(errorMessage);
            event.preventDefault();
        }
    });
});

