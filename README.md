# Expense/Income Tracker REST API

This is a robust RESTful API built with Django and Django REST Framework (DRF) for tracking personal expenses and income. It includes a complete user authentication system using JWT (JSON Web Tokens), role-based access control, and automatic tax calculation.

## Table of Contents

* [Features](#features)

* [Approach](#approach)

* [Setup Instructions](#setup-instructions)

* [API Endpoints](#api-endpoints)

* [API Response Formats](#api-response-formats)

* [Testing](#testing)

## Features

* **User Authentication:** Secure user registration and login system using JWT (JSON Web Tokens) for all API operations.

* **Token Management:** Endpoints for obtaining and refreshing JWT access tokens.

* **Personal Expense/Income Tracking:** Users can create, retrieve, update, and delete their own financial records.

* **Automatic Tax Calculation:** Records include fields for `tax` and `tax_type` (`flat` or `percentage`), with `tax_amount_calculated` and `total_amount` automatically computed and stored.

* **Role-Based Access Control:**

  * **Regular Users:** Can only manage (CRUD) their own expense/income records.

  * **Superusers:** Have full access to manage all users' records across the system.

* **Paginated API Responses:** List endpoints provide paginated results for efficient data retrieval.

* **Clear API Structure:** Well-defined endpoints and consistent response formats.

* **Informative API Root:** A user-friendly HTML welcome page at the base URL (`/`) guiding users to the API documentation.

## Approach

This API is built following best practices for Django and Django REST Framework:

* **Django's Built-in User Model:** Leverages Django's robust `User` model for authentication, simplifying user management.

* **Django REST Framework (`DRF`):** Provides powerful tools for building REST APIs, including serializers, class-based views (like `ModelViewSet`), and authentication/permission classes.

* **`djangorestframework-simplejwt`:** Implements JWT authentication, offering secure and stateless token-based authentication.

* **Model-Level Business Logic:** The tax calculation logic (`flat` vs. `percentage`) is encapsulated within the `ExpenseIncome` model's `save()` method. This ensures that `tax_amount_calculated` and `total_amount` are always consistent and correctly derived, regardless of how the model instance is saved (via API, admin, or shell).

* **Serializer Customization:**

  * `UserRegistrationSerializer`: Handles password confirmation and proper user creation (`create_user`).

  * `ExpenseIncomeSerializer`: Manages the detailed CRUD operations, including user assignment based on permissions and mapping `total_amount` to `total` in the API output.

  * `ExpenseIncomeListSerializer`: Provides a simplified JSON format for list views, adhering to the specified response requirements.

* **Permission Handling:** DRF's `IsAuthenticated` permission class is used, coupled with custom `get_queryset` and `perform_destroy` methods in the `ViewSet` to enforce regular user/superuser access rules.

* **Clear URL Structure:** API endpoints are logically grouped under `/api/auth/` for authentication and `/api/expenses/` for financial records.

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

1. **Clone the Repository (or create project manually):**
   If you have the project files in a repository, clone it:

   ```bash
   git clone <repository-url>
   cd expense_tracker_api # Navigate into your project directory
If you're building from scratch using the provided code, ensure you are in your expense_tracker_api directory.

Create and Activate a Python Virtual Environment:

Bash

python -m venv venv
On Windows:

Bash

.\venv\Scripts\activate
On macOS/Linux:

Bash

source venv/bin/activate
Install Dependencies:

Bash

pip install Django djangorestframework djangorestframework-simplejwt
Configure Project Files:
Ensure your project files (expense_tracker_project/settings.py, transactions/models.py, transactions/serializers.py, transactions/views.py, expense_tracker_project/urls.py) contain the complete and latest code provided in the previous steps.

Run Database Migrations:

Bash

python manage.py makemigrations
python manage.py migrate
Note: If you're upgrading from a previous version, makemigrations might prompt you about model renames (e.g., Transaction to ExpenseIncome). Confirm these changes.

Create a Superuser:
This account will allow you to access the Django admin panel and test superuser permissions.

Bash

python manage.py createsuperuser
Follow the prompts to set a username, email, and password.

Run the Development Server:

Bash

python manage.py runserver
The API will now be running, typically accessible at http://127.0.0.1:8000/.

API Endpoints
All endpoints are relative to your base API URL (e.g., http://127.0.0.1:8000/).

Authentication Endpoints
These endpoints are used for managing user accounts and obtaining/refreshing JWT tokens.

User Registration

Method: POST

URL: /api/auth/register/

Purpose: Create a new user account.

User Login

Method: POST

URL: /api/auth/login/

Purpose: Authenticate a user and receive access (short-lived) and refresh (long-lived) JWT tokens.

Refresh Token

Method: POST

URL: /api/auth/refresh/

Purpose: Obtain a new access token using a valid refresh token.

Expense/Income Records Endpoints
These endpoints are used for managing individual expense and income records. All requests to these endpoints require authentication by including a JWT Bearer token in the Authorization header (e.g., Authorization: Bearer YOUR_ACCESS_TOKEN).

List All Records (for the authenticated user)

Method: GET

URL: /api/expenses/

Purpose: Retrieve a paginated list of expense/income records belonging to the authenticated user. (Superusers can list all records in the system).

Create a New Record

Method: POST

URL: /api/expenses/

Purpose: Add a new expense or income record.

Retrieve a Specific Record

Method: GET

URL: /api/expenses/{id}/

Purpose: Get the detailed information for a single expense/income record by its unique {id}.

Update an Existing Record

Method: PUT / PATCH

URL: /api/expenses/{id}/

Purpose:

PUT: Replace an entire existing record with new data (requires all fields).

PATCH: Partially update an existing record with new data for specific fields.

Delete a Record

Method: DELETE

URL: /api/expenses/{id}/

Purpose: Remove an expense/income record from the system.

API Response Formats
Single Record Response (e.g., GET /api/expenses/{id}/ or POST /api/expenses/)
JSON

{
    "id": 1,
    "title": "Grocery Shopping",
    "description": "Weekly groceries",
    "amount": 100.00,
    "transaction_type": "debit",
    "tax": 10.00,
    "tax_type": "flat",
    "total": 110.00,
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-01T10:00:00Z"
}
List Response (Paginated) (e.g., GET /api/expenses/)
JSON

{
    "count": 25,
    "next": "[http://127.0.0.1:8000/api/expenses/?page=2](http://127.0.0.1:8000/api/expenses/?page=2)",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Grocery Shopping",
            "amount": 100.00,
            "transaction_type": "debit",
            "total": 110.00,
            "created_at": "2025-01-01T10:00:00Z"
        },
        // ... more records ...
    ]
}
Testing
You can use curl (command-line tool) or Postman (graphical interface) to interact with and test these API endpoints.

Using curl for Testing:

curl commands are powerful for quick testing. Remember to adjust the syntax based on your operating system's terminal (e.g., Windows Command Prompt requires double quotes and escaped inner double quotes for JSON data).

Example: User Login with curl (Windows Command Prompt syntax)

Bash

curl -X POST "[http://127.0.0.1:8000/api/auth/login/](http://127.0.0.1:8000/api/auth/login/)" -H "Content-Type: application/json" -d "{\"username\": \"your_username\", \"password\": \"your_password\"}"
This command will return access and refresh tokens. Use the access token in the Authorization header for protected endpoints:

Example: Creating a Record with curl (Windows Command Prompt syntax)

Bash

curl -X POST "[http://127.0.0.1:8000/api/expenses/](http://127.0.0.1:8000/api/expenses/)" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{\"title\": \"First Expense\", \"amount\": 5.50, \"transaction_type\": \"debit\", \"tax\": 0.00, \"tax_type\": \"flat\", \"date\": \"2025-07-04\"}"
Key HTTP Status Codes to Expect:

200 OK: Successful GET, PUT, PATCH

201 Created: Successful POST (resource creation)

204 No Content: Successful DELETE

400 Bad Request: Invalid data provided

401 Unauthorized: Authentication required or invalid/missing token

403 Forbidden: Authenticated user lacks permission

404 Not Found: Resource not found
