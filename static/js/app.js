document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registration-form");
    const fields = ["full_name", "email", "age", "gender", "course", "password"];

    function showError(field, message) {
        const error = document.getElementById(`${field.id}-error`);
        error.textContent = message;
        field.classList.toggle("border-red-500", Boolean(message));
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        let isValid = true;
        const values = Object.fromEntries(
            fields.map((name) => [name, document.getElementById(name)])
        );

        fields.forEach((name) => showError(values[name], ""));

        if (!values.full_name.value.trim()) {
            showError(values.full_name, "Full name is required.");
            isValid = false;
        }
        if (!values.email.value.trim()) {
            showError(values.email, "Email is required.");
            isValid = false;
        } else if (!values.email.validity.valid) {
            showError(values.email, "Enter a valid email address.");
            isValid = false;
        }
        if (!values.age.value.trim()) {
            showError(values.age, "Age is required.");
            isValid = false;
        } else if (!Number.isInteger(Number(values.age.value)) ||
                   Number(values.age.value) < 1 || Number(values.age.value) > 120) {
            showError(values.age, "Age must be a whole number from 1 to 120.");
            isValid = false;
        }
        if (!values.gender.value) {
            showError(values.gender, "Please select your gender.");
            isValid = false;
        }
        if (!values.course.value) {
            showError(values.course, "Please select a course.");
            isValid = false;
        }
        if (!values.password.value) {
            showError(values.password, "Password is required.");
            isValid = false;
        } else if (values.password.value.length < 6) {
            showError(values.password, "Password must be at least 6 characters.");
            isValid = false;
        }

        if (isValid) {
            alert("Form submitted successfully.");
            form.submit();
        } else {
            alert("Please correct the highlighted fields.");
        }
    });
});
