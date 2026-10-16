document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registration-form");
    if (form) {
        initializeRegistrationValidation(form);
    }

    if (window.jQuery) {
        initializeProfileInteractions();
    }
});

function initializeRegistrationValidation(form) {
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
}

    function initializeProfileInteractions() {
        const $ = window.jQuery;
        const liveTime = document.getElementById("live-time");
        const details = $("#profile-details");
        const toggleButton = $("#toggle-details");
        const course = $("#course");

        if (!liveTime || details.length === 0 || toggleButton.length === 0 || course.length === 0) {
            return;
        }

        function updateTime() {
            const utcNow = new Date();
            const localTime = new Date(utcNow.getTime() + (5 * 60 + 30) * 60 * 1000);
            const utcTime = [
                localTime.getUTCHours(),
                localTime.getUTCMinutes(),
                localTime.getUTCSeconds(),
            ]
                .map((value) => String(value).padStart(2, "0"))
                .join(":");

            liveTime.textContent = utcTime;
        }

        updateTime();
        window.setInterval(updateTime, 1000);

        toggleButton.on("click", () => {
            details.slideToggle(200, () => {
                toggleButton.text(details.is(":visible") ? "Hide Details" : "Show Details");
            });
        });

        course.on("change", function () {
            const selectedCourse = $(this).val();
            $.post($(this).data("update-url"), { course: selectedCourse })
                .done((response) => {
                    if (response.success) {
                        alert(`Course updated to: ${response.course}`);
                    } else {
                        alert(response.message);
                    }
                })
                .fail((error) => {
                    const message = error.responseJSON?.message || "Course update failed.";
                    alert(message);
                });
        });
    }
