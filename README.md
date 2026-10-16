# Student Registration Form

This project is a Flask-based student registration form for **Level 1: Frontend Form + Basic Logic**.

## 🔹 Level 1: Frontend Form + Basic Logic

### Objective

Build a responsive frontend student registration form with basic client-side validation.

### Tasks

1. Create a responsive HTML form to collect:
   - Full Name
   - Email
   - Age
   - Gender
   - Course
   - Password
2. Add CSS styling for the form layout and responsiveness.
3. Use JavaScript/jQuery to validate:
   - Required fields
   - Numeric age
   - Password length of at least 6 characters
4. Show alerts or messages using conditional logic.

## Achieved: Current Implementation

- Responsive registration form created in `templates/index.html`.
- Form fields added for full name, email, age, gender, course, and password.
- Tailwind CSS is loaded through the CDN for responsive layout and styling.
- Additional form styles are defined in `static/css/style.css`.
- JavaScript validation is implemented in `static/js/app.js`.
- Required-field validation is included.
- Email format validation is included.
- Age validation checks for a whole number between 1 and 120.
- Password validation requires at least 6 characters.
- Inline validation messages are shown below invalid fields.
- Alert messages are shown for valid and invalid submissions.
- Flask server-side validation is also included in `app.py`.
- Submitted registrations are stored in the SQLite database `app.db`.
- Passwords are stored as secure password hashes rather than plain text.
- Duplicate email addresses are rejected with an error message.

## Project Structure

```text
flask_project/
├── app.py
├── app.db
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## How to Run

From the `flask_project` directory, activate the virtual environment and start Flask:

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

Open the application in a browser at:

```text
http://127.0.0.1:5000
```

## Validation

The application has been checked with:

- Python syntax compilation
- A successful `GET /` request
- An invalid registration request returning HTTP `400`
- A valid registration request returning HTTP `200`
- SQLite database and registration table initialization

