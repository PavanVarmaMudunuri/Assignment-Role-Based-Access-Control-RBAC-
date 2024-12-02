# Assignment-Role-Based-Access-Control-RBAC-

This project demonstrates a simple Django setup with user authentication, role-based access control (RBAC), and RESTful API endpoints for user registration, login, and accessing protected resources. It uses SQLite as the database and supports JWT-based authentication via `djangorestframework-simplejwt`.

Features

- User registration with role assignment (Admin, Moderator, User).
- JWT-based authentication for secure login.
- Role-based access to different endpoints.
- Permissions management using Django's built-in groups and permissions.
- Lightweight setup with minimal dependencies.

 Prerequisites

- Python 3.8 or later
- `pip` for managing Python packages

Setup Instructions

 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```
 2. Install Dependencies

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install required packages:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

3. Run the Application

1. Apply database migrations:

   ```bash
   python from_djangocontribauth.py migrate
   ```

2. Start the server:

   ```bash
   python from_djangocontribauth.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`.

 API Endpoints

 1. User Registration

POST `/register/`

Registers a new user with the specified role.

Request Body:

```json
{
  "username": "example_user",
  "password": "example_password",
  "role": "Admin"  // Options: Admin, User, Moderator
}
```

Response:

```json
{
  "message": "User registered successfully"
}
```

2. User Login*

POST `/login/`

Authenticates a user and returns JWT tokens.

Request Body:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

**Response:**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

 3. Dashboard Access

GET `/dashboard/`

Accessible by users with `Admin` or `Moderator` roles.

Response:

```json
{
  "message": "Welcome to the dashboard!"
}
```

 4. Manage Users

POST`/admin/manage/`

Accessible only by users with the `Admin` role.

Response:

```json
{
  "message": "User management access granted."
}
```
Project Structure

```
myproject/
    from_djangocontribauth.py  # Main project file
    db.sqlite3                 # SQLite database file
```

Notes

- Ensure you replace `your_secret_key` in the script with a secure and random secret key.
- To add additional roles or permissions, modify the `setup_roles_and_permissions()` function in `from_djangocontribauth.py`.
- For production, configure settings like `DEBUG`, `ALLOWED_HOSTS`, and use a more robust database.

 License

This project is licensed under the MIT License. Feel free to use and modify it as per your needs.

Contributions

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.


