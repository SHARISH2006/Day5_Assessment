# Student Registration Form

This project is a Flask-based student registration form. This README is a cumulative record of the tasks completed at each level. 

## Progress Summary

| Level | Topic | Status |
|---|---|---|
| Level 1 | Frontend Form + Basic Logic | Completed |
| Level 2 | Flask Setup + DB Interaction | Completed |
| Level 3 | Session Handling + Profile Page | Completed |

## 🔹 Level 1: Frontend Form + Basic Logic

### Objective

Build a responsive frontend student registration form with basic client-side validation.

### Tasks Completed

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

### Achieved

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

## 🔹 Level 2: Flask Setup + DB Interaction

### Objective

Set up Flask with SQLite and store submitted student registration data in the database.

### Tasks Completed

1. Initialize Flask with SQLite.
   - SQLite database configuration is defined in `app.py`.
2. Create a Student model with fields:
   - `id`
   - `name`
   - `email`
   - `age`
   - `gender`
   - `course`
   - `password`
3. On form submission:
   - Form data is inserted into the `students` table.
   - Database insert errors are handled with `try/except`.
4. Redirect to `/success` after registration.
   - The page displays: `Welcome, {{ name }}! You have successfully registered.`

### Achieved

- Flask server-side validation is also included in `app.py`.
- Flask is configured with the local SQLite database `app.db`.
- A `Student` model is defined with `name`, `email`, `age`, `gender`, `course`, and `password` fields.
- A `students` table is created automatically when the application starts.
- Submitted registrations are stored in the `students` table.
- Database insert errors are handled with `try/except`.
- Passwords are stored as secure password hashes rather than plain text.
- Duplicate email addresses are rejected with an error message.
- Successful submissions redirect to `/success`.
- The success page displays the required welcome message.

## 🔹 Level 3: Session Handling + Profile Page

### Objective

Use Flask sessions to manage student login and display the authenticated student's data.

### Tasks Completed

1. Implement a `/login` route using email and password.
   - Credentials are authenticated against the `students` table.
   - The authenticated `student_id` is saved in the Flask session.
2. Create a protected `/profile` route.
   - The student is fetched using the ID stored in the session.
   - The profile displays name, course, email, and age.
3. Add a logout option.
   - The session is cleared.
   - The user is redirected to `/login`.

### Achieved

- Login page added at `/login`.
- Passwords are checked against their stored secure hashes.
- Invalid or missing credentials show an error message.
- Unauthenticated users are redirected from `/profile` to `/login`.
- Profile data is loaded from SQLite using the session's `student_id`.
- Logout is implemented at `/logout`.

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
