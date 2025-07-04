Expense/Income Tracker REST API
This is a robust RESTful API built with Django and Django REST Framework (DRF) for tracking personal expenses and income. It includes a complete user authentication system using JWT (JSON Web Tokens), role-based access control, and automatic tax calculation.

Table of Contents
Features

Approach

Setup Instructions

API Endpoints

API Response Formats

Testing

Features
User Authentication: Secure user registration and login system using JWT (JSON Web Tokens) for all API operations.

Token Management: Endpoints for obtaining and refreshing JWT access tokens.

Personal Expense/Income Tracking: Users can create, retrieve, update, and delete their own financial records.

Automatic Tax Calculation: Records include fields for tax and tax_type (flat or percentage), with tax_amount_calculated and total_amount automatically computed and stored.

Role-Based Access Control:

Regular Users: Can only manage (CRUD) their own expense/income records.

Superusers: Have full access to manage all users' records across the system.

Paginated API Responses: List endpoints provide paginated results for efficient data retrieval.

Clear API Structure: Well-defined endpoints and consistent response formats.

Informative API Root: A user-friendly HTML welcome page at the base URL (/) guiding users to the API documentation.

Approach
This API is built following best practices for Django and Django REST Framework:

Django's Built-in User Model: Leverages Django's robust User model for authentication, simplifying user management.

Django REST Framework (DRF): Provides powerful tools for building REST APIs, including serializers, class-based views (like ModelViewSet), and authentication/permission classes.

djangorestframework-simplejwt: Implements JWT authentication, offering secure and stateless token-based authentication.

Model-Level Business Logic: The tax calculation logic (flat vs. percentage) is encapsulated within the ExpenseIncome model's save() method. This ensures that tax_amount_calculated and total_amount are always consistent and correctly derived, regardless of how the model instance is saved (via API, admin, or shell).

Serializer Customization:

UserRegistrationSerializer: Handles password confirmation and proper user creation (create_user).

ExpenseIncomeSerializer: Manages the detailed CRUD operations, including user assignment based on permissions and mapping total_amount to total in the API output.

ExpenseIncomeListSerializer: Provides a simplified JSON format for list views, adhering to the specified response requirements.

Permission Handling: DRF's IsAuthenticated permission class is used, coupled with custom get_queryset and perform_destroy methods in the ViewSet to enforce regular user/superuser access rules.

Clear URL Structure: API endpoints are logically grouped under /api/auth/ for authentication and /api/expenses/ for financial records.

Setup Instructions
Follow these steps to get the project up and running on your local machine.

Clone the Repository (or create project manually):
If you have the project files in a repository, clone it:

git clone <repository-url>
cd expense_tracker_api # Navigate into your project directory

If you're building from scratch using the provided code, ensure you are in your expense_tracker_api directory.

Create and Activate a Python Virtual Environment:

python -m venv venv

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install Dependencies:

pip install Django djangorestframework djangorestframework-simplejwt

Configure Project Files:
Ensure your project files (expense_tracker_project/settings.py, transactions/models.py, transactions/serializers.py, transactions/views.py, expense_tracker_project/urls.py) contain the complete and latest code provided in the previous steps.

Run Database Migrations:

python manage.py makemigrations
python manage.py migrate

Note: If you're upgrading from a previous version, makemigrations might prompt you about model renames (e.g., Transaction to ExpenseIncome). Confirm these changes.

Create a Superuser:
This account will allow you to access the Django admin panel and test superuser permissions.

python manage.py createsuperuser

Follow the prompts to set a username, email, and password.

Run the Development Server:

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
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/expenses/?page=2",
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

curl -X POST "http://127.0.0.1:8000/api/auth/login/" -H "Content-Type: application/json" -d "{\"username\": \"your_username\", \"password\": \"your_password\"}"

This command will return access and refresh tokens. Use the access token in the Authorization header for protected endpoints:

Example: Creating a Record with curl (Windows Command Prompt syntax)

curl -X POST "http://127.0.0.1:8000/api/expenses/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{\"title\": \"First Expense\", \"amount\": 5.50, \"transaction_type\": \"debit\", \"tax\": 0.00, \"tax_type\": \"flat\", \"date\": \"2025-07-04\"}"

Key HTTP Status Codes to Expect:

200 OK: Successful GET, PUT, PATCH

201 Created: Successful POST (resource creation)

204 No Content: Successful DELETE

400 Bad Request: Invalid data provided

401 Unauthorized: Authentication required or invalid/missing token

403 Forbidden: Authenticated user lacks permission

404 Not Found: Resource not found


### curl operation

Microsoft Windows [Version 10.0.19045.5965]
(c) Microsoft Corporation. All rights reserved.

C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/auth/register/" -H "Content-Type: application/json" -d "{\"username\": \"curluser\", \"email\": \"curl@example.com\", \"password\": \"CurlPass123!\", \"password2\": \"CurlPass123!\"}"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="robots" content="NONE,NOARCHIVE">
  <title>TypeError
          at /api/auth/register/</title>
  <style>
    html * { padding:0; margin:0; }
    body * { padding:10px 20px; }
    body * * { padding:0; }
    body { font-family: sans-serif; background-color:#fff; color:#000; }
    body > :where(header, main, footer) { border-bottom:1px solid #ddd; }
    h1 { font-weight:normal; }
    h2 { margin-bottom:.8em; }
    h3 { margin:1em 0 .5em 0; }
    h4 { margin:0 0 .5em 0; font-weight: normal; }
    code, pre { font-size: 100%; white-space: pre-wrap; word-break: break-word; }
    summary { cursor: pointer; }
    table { border:1px solid #ccc; border-collapse: collapse; width:100%; background:white; }
    tbody td, tbody th { vertical-align:top; padding:2px 3px; }
    thead th {
      padding:1px 6px 1px 3px; background:#fefefe; text-align:left;
      font-weight:normal; font-size: 0.6875rem; border:1px solid #ddd;
    }
    tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; }
    table.vars { margin:5px 10px 2px 40px; width: auto; }
    table.vars td, table.req td { font-family:monospace; }
    table td.code { width:100%; }
    table td.code pre { overflow:hidden; }
    table.source th { color:#666; }
    table.source td { font-family:monospace; white-space:pre; border-bottom:1px solid #eee; }
    ul.traceback { list-style-type:none; color: #222; }
    ul.traceback li.cause { word-break: break-word; }
    ul.traceback li.frame { padding-bottom:1em; color:#4f4f4f; }
    ul.traceback li.user { background-color:#e0e0e0; color:#000 }
    div.context { padding:10px 0; overflow:hidden; }
    div.context ol { padding-left:30px; margin:0 10px; list-style-position: inside; }
    div.context ol li { font-family:monospace; white-space:pre; color:#777; cursor:pointer; padding-left: 2px; }
    div.context ol li pre { display:inline; }
    div.context ol.context-line li { color:#464646; background-color:#dfdfdf; padding: 3px 2px; }
    div.context ol.context-line li span { position:absolute; right:32px; }
    .user div.context ol.context-line li { background-color:#bbb; color:#000; }
    .user div.context ol li { color:#666; }
    div.commands, summary.commands { margin-left: 40px; }
    div.commands a, summary.commands { color:#555; text-decoration:none; }
    .user div.commands a { color: black; }
    #summary { background: #ffc; }
    #summary h2 { font-weight: normal; color: #666; }
    #info { padding: 0; }
    #info > * { padding:10px 20px; }
    #explanation { background:#eee; }
    #template, #template-not-exist { background:#f6f6f6; }
    #template-not-exist ul { margin: 0 0 10px 20px; }
    #template-not-exist .postmortem-section { margin-bottom: 3px; }
    #unicode-hint { background:#eee; }
    #traceback { background:#eee; }
    #requestinfo { background:#f6f6f6; padding-left:120px; }
    #summary table { border:none; background:transparent; }
    #requestinfo h2, #requestinfo h3 { position:relative; margin-left:-100px; }
    #requestinfo h3 { margin-bottom:-1em; }
    .error { background: #ffc; }
    .specific { color:#cc3300; font-weight:bold; }
    h2 span.commands { font-size: 0.7rem; font-weight:normal; }
    span.commands a:link {color:#5E5694;}
    pre.exception_value { font-family: sans-serif; color: #575757; font-size: 1.5rem; margin: 10px 0 10px 0; }
    .append-bottom { margin-bottom: 10px; }
    .fname { user-select: all; }
  </style>

  <script>
    function hideAll(elems) {
      for (var e = 0; e < elems.length; e++) {
        elems[e].style.display = 'none';
      }
    }
    window.onload = function() {
      hideAll(document.querySelectorAll('ol.pre-context'));
      hideAll(document.querySelectorAll('ol.post-context'));
      hideAll(document.querySelectorAll('div.pastebin'));
    }
    function toggle() {
      for (var i = 0; i < arguments.length; i++) {
        var e = document.getElementById(arguments[i]);
        if (e) {
          e.style.display = e.style.display == 'none' ? 'block': 'none';
        }
      }
      return false;
    }
    function switchPastebinFriendly(link) {
      s1 = "Switch to copy-and-paste view";
      s2 = "Switch back to interactive view";
      link.textContent = link.textContent.trim() == s1 ? s2: s1;
      toggle('browserTraceback', 'pastebinTraceback');
      return false;
    }
  </script>

</head>
<body>
<header id="summary">
  <h1>TypeError
       at /api/auth/register/</h1>
  <pre class="exception_value">User() got unexpected keyword arguments: &#x27;password2&#x27;</pre>
  <table class="meta">

    <tr>
      <th scope="row">Request Method:</th>
      <td>POST</td>
    </tr>
    <tr>
      <th scope="row">Request URL:</th>
      <td>http://127.0.0.1:8000/api/auth/register/</td>
    </tr>

    <tr>
      <th scope="row">Django Version:</th>
      <td>5.2.4</td>
    </tr>

    <tr>
      <th scope="row">Exception Type:</th>
      <td>TypeError</td>
    </tr>


    <tr>
      <th scope="row">Exception Value:</th>
      <td><pre>User() got unexpected keyword arguments: &#x27;password2&#x27;</pre></td>
    </tr>


    <tr>
      <th scope="row">Exception Location:</th>
      <td><span class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\db\models\base.py</span>, line 569, in __init__</td>
    </tr>


    <tr>
      <th scope="row">Raised during:</th>
      <td>transactions.views.UserRegistrationView</td>
    </tr>

    <tr>
      <th scope="row">Python Executable:</th>
      <td>C:\Users\DELL\OneDrive\Desktop\tracker\venv\Scripts\python.exe</td>
    </tr>
    <tr>
      <th scope="row">Python Version:</th>
      <td>3.12.3</td>
    </tr>
    <tr>
      <th scope="row">Python Path:</th>
      <td><pre><code>[&#x27;C:\\Users\\DELL\\OneDrive\\Desktop\\tracker&#x27;,
 &#x27;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\python312.zip&#x27;,
 &#x27;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\DLLs&#x27;,
 &#x27;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\Lib&#x27;,
 &#x27;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312&#x27;,
 &#x27;C:\\Users\\DELL\\OneDrive\\Desktop\\tracker\\venv&#x27;,
 &#x27;C:\\Users\\DELL\\OneDrive\\Desktop\\tracker\\venv\\Lib\\site-packages&#x27;]</code></pre></td>
    </tr>
    <tr>
      <th scope="row">Server time:</th>
      <td>Fri, 04 Jul 2025 16:29:02 +0000</td>
    </tr>
  </table>
</header>

<main id="info">




<div id="traceback">
  <h2>Traceback <span class="commands"><a href="#" role="button" onclick="return switchPastebinFriendly(this);">
    Switch to copy-and-paste view</a></span>
  </h2>
  <div id="browserTraceback">
    <ul class="traceback">


        <li class="frame django">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\core\handlers\exception.py</code>, line 55, in inner



            <div class="context" id="c2346530178816">

                <ol start="48" class="pre-context" id="pre2346530178816">

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre></pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>        return inner</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>    else:</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre></pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>        @wraps(get_response)</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>        def inner(request):</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>            try:</pre></li>

                </ol>

              <ol start="55" class="context-line">
                <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>                response = get_response(request)
                               ^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='56' class="post-context" id="post2346530178816">

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>            except Exception as exc:</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>                response = response_for_exception(request, exc)</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>            return response</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre></pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre>        return inner</pre></li>

                  <li onclick="toggle('pre2346530178816', 'post2346530178816')"><pre></pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530178816">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>exc</td>
                    <td class="code"><pre>TypeError(&quot;User() got unexpected keyword arguments: &#x27;password2&#x27;&quot;)</pre></td>
                  </tr>

                  <tr>
                    <td>get_response</td>
                    <td class="code"><pre>&lt;bound method BaseHandler._get_response of &lt;django.core.handlers.wsgi.WSGIHandler object at 0x000002225448E690&gt;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;WSGIRequest: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame django">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\core\handlers\base.py</code>, line 197, in _get_response



            <div class="context" id="c2346530181248">

                <ol start="190" class="pre-context" id="pre2346530181248">

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>        if response is None:</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>            wrapped_callback = self.make_view_atomic(callback)</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>            # If it is an asynchronous view, run it in a subthread.</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>            if iscoroutinefunction(wrapped_callback):</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>                wrapped_callback = async_to_sync(wrapped_callback)</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>            try:</pre></li>

                </ol>

              <ol start="197" class="context-line">
                <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>                response = wrapped_callback(request, *callback_args, **callback_kwargs)
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='198' class="post-context" id="post2346530181248">

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>            except Exception as e:</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>                response = self.process_exception_by_middleware(e, request)</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>                if response is None:</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>                    raise</pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181248', 'post2346530181248')"><pre>        # Complain if the view returned None (a common error).</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530181248">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>callback</td>
                    <td class="code"><pre>&lt;function View.as_view.&lt;locals&gt;.view at 0x0000022257B58860&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>callback_args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>callback_kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>middleware_method</td>
                    <td class="code"><pre>&lt;bound method CsrfViewMiddleware.process_view of &lt;CsrfViewMiddleware get_response=convert_exception_to_response.&lt;locals&gt;.inner&gt;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;WSGIRequest: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>response</td>
                    <td class="code"><pre>None</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;django.core.handlers.wsgi.WSGIHandler object at 0x000002225448E690&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>wrapped_callback</td>
                    <td class="code"><pre>&lt;function View.as_view.&lt;locals&gt;.view at 0x0000022257B58860&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame django">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\views\decorators\csrf.py</code>, line 65, in _view_wrapper



            <div class="context" id="c2346530181120">

                <ol start="58" class="pre-context" id="pre2346530181120">

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>        async def _view_wrapper(request, *args, **kwargs):</pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>            return await view_func(request, *args, **kwargs)</pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>    else:</pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>        def _view_wrapper(request, *args, **kwargs):</pre></li>

                </ol>

              <ol start="65" class="context-line">
                <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>            return view_func(request, *args, **kwargs)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='66' class="post-context" id="post2346530181120">

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>    _view_wrapper.csrf_exempt = True</pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181120', 'post2346530181120')"><pre>    return wraps(view_func)(_view_wrapper)</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530181120">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;WSGIRequest: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>view_func</td>
                    <td class="code"><pre>&lt;function View.as_view.&lt;locals&gt;.view at 0x0000022257B587C0&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame django">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\views\generic\base.py</code>, line 105, in view



            <div class="context" id="c2346530178240">

                <ol start="98" class="pre-context" id="pre2346530178240">

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>            self = cls(**initkwargs)</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>            self.setup(request, *args, **kwargs)</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>            if not hasattr(self, &quot;request&quot;):</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>                raise AttributeError(</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>                    &quot;%s instance has no &#x27;request&#x27; attribute. Did you override &quot;</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>                    &quot;setup() and forget to call super()?&quot; % cls.__name__</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>                )</pre></li>

                </ol>

              <ol start="105" class="context-line">
                <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>            return self.dispatch(request, *args, **kwargs)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='106' class="post-context" id="post2346530178240">

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre></pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>        view.view_class = cls</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>        view.view_initkwargs = initkwargs</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre></pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>        # __name__ and __qualname__ are intentionally left unchanged as</pre></li>

                  <li onclick="toggle('pre2346530178240', 'post2346530178240')"><pre>        # view_class should be used to robustly determine the name of the view</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530178240">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>cls</td>
                    <td class="code"><pre>&lt;class &#x27;transactions.views.UserRegistrationView&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>initkwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;WSGIRequest: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py</code>, line 515, in dispatch



            <div class="context" id="c2346530180864">

                <ol start="508" class="pre-context" id="pre2346530180864">

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>                                  self.http_method_not_allowed)</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>            else:</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>                handler = self.http_method_not_allowed</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>            response = handler(request, *args, **kwargs)</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>        except Exception as exc:</pre></li>

                </ol>

              <ol start="515" class="context-line">
                <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>            response = self.handle_exception(exc)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='516' class="post-context" id="post2346530180864">

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>        self.response = self.finalize_response(request, response, *args, **kwargs)</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>        return self.response</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>    def options(self, request, *args, **kwargs):</pre></li>

                  <li onclick="toggle('pre2346530180864', 'post2346530180864')"><pre>        &quot;&quot;&quot;</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530180864">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>handler</td>
                    <td class="code"><pre>&lt;bound method UserRegistrationView.post of &lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py</code>, line 475, in handle_exception



            <div class="context" id="c2346530180928">

                <ol start="468" class="pre-context" id="pre2346530180928">

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        exception_handler = self.get_exception_handler()</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        context = self.get_exception_handler_context()</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        response = exception_handler(exc, context)</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        if response is None:</pre></li>

                </ol>

              <ol start="475" class="context-line">
                <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>            self.raise_uncaught_exception(exc)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='476' class="post-context" id="post2346530180928">

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        response.exception = True</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        return response</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>    def raise_uncaught_exception(self, exc):</pre></li>

                  <li onclick="toggle('pre2346530180928', 'post2346530180928')"><pre>        if settings.DEBUG:</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530180928">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>context</td>
                    <td class="code"><pre>{&#x27;args&#x27;: (),
 &#x27;kwargs&#x27;: {},
 &#x27;request&#x27;: &lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;,
 &#x27;view&#x27;: &lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;}</pre></td>
                  </tr>

                  <tr>
                    <td>exc</td>
                    <td class="code"><pre>TypeError(&quot;User() got unexpected keyword arguments: &#x27;password2&#x27;&quot;)</pre></td>
                  </tr>

                  <tr>
                    <td>exception_handler</td>
                    <td class="code"><pre>&lt;function exception_handler at 0x0000022257AF9EE0&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>response</td>
                    <td class="code"><pre>None</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py</code>, line 486, in raise_uncaught_exception



            <div class="context" id="c2346530193280">

                <ol start="479" class="pre-context" id="pre2346530193280">

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre></pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>    def raise_uncaught_exception(self, exc):</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>        if settings.DEBUG:</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>            request = self.request</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>            renderer_format = getattr(request.accepted_renderer, &#x27;format&#x27;)</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>            use_plaintext_traceback = renderer_format not in (&#x27;html&#x27;, &#x27;api&#x27;, &#x27;admin&#x27;)</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>            request.force_plaintext_errors(use_plaintext_traceback)</pre></li>

                </ol>

              <ol start="486" class="context-line">
                <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>        raise exc
             ^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='487' class="post-context" id="post2346530193280">

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre></pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>    # Note: Views are made CSRF exempt from within `as_view` as to prevent</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>    # accidental removal of this exemption in cases where `dispatch` needs to</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>    # be overridden.</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>    def dispatch(self, request, *args, **kwargs):</pre></li>

                  <li onclick="toggle('pre2346530193280', 'post2346530193280')"><pre>        &quot;&quot;&quot;</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530193280">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>exc</td>
                    <td class="code"><pre>TypeError(&quot;User() got unexpected keyword arguments: &#x27;password2&#x27;&quot;)</pre></td>
                  </tr>

                  <tr>
                    <td>renderer_format</td>
                    <td class="code"><pre>&#x27;json&#x27;</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>use_plaintext_traceback</td>
                    <td class="code"><pre>True</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py</code>, line 512, in dispatch



            <div class="context" id="c2346530181696">

                <ol start="505" class="pre-context" id="pre2346530181696">

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>            # Get the appropriate handler method</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>            if request.method.lower() in self.http_method_names:</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>                handler = getattr(self, request.method.lower(),</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>                                  self.http_method_not_allowed)</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>            else:</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>                handler = self.http_method_not_allowed</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre></pre></li>

                </ol>

              <ol start="512" class="context-line">
                <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>            response = handler(request, *args, **kwargs)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='513' class="post-context" id="post2346530181696">

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>        except Exception as exc:</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>            response = self.handle_exception(exc)</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre></pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>        self.response = self.finalize_response(request, response, *args, **kwargs)</pre></li>

                  <li onclick="toggle('pre2346530181696', 'post2346530181696')"><pre>        return self.response</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530181696">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>handler</td>
                    <td class="code"><pre>&lt;bound method UserRegistrationView.post of &lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\transactions\views.py</code>, line 19, in post



            <div class="context" id="c2346530179392">

                <ol start="12" class="pre-context" id="pre2346530179392">

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>    &quot;&quot;&quot;</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>    queryset = User.objects.all()</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>    serializer_class = UserRegistrationSerializer</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>    permission_classes = [AllowAny]</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre></pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>    def post(self, request, *args, **kwargs):</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>        serializer = self.get_serializer(data=request.data)</pre></li>

                </ol>

              <ol start="19" class="context-line">
                <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>        serializer.is_valid(raise_exception=True)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='20' class="post-context" id="post2346530179392">

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>        user = serializer.save()</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>        return Response({</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>            &quot;message&quot;: &quot;User registered successfully.&quot;,</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>            &quot;username&quot;: user.username,</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>            &quot;email&quot;: user.email</pre></li>

                  <li onclick="toggle('pre2346530179392', 'post2346530179392')"><pre>        }, status=status.HTTP_201_CREATED)</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530179392">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{}</pre></td>
                  </tr>

                  <tr>
                    <td>request</td>
                    <td class="code"><pre>&lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;transactions.views.UserRegistrationView object at 0x0000022257F7B8C0&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>serializer</td>
                    <td class="code"><pre>UserRegistrationSerializer(context={&#x27;request&#x27;: &lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;, &#x27;format&#x27;: None, &#x27;view&#x27;: &lt;transactions.views.UserRegistrationView object&gt;}, data={&#x27;username&#x27;: &#x27;curluser&#x27;, &#x27;email&#x27;: &#x27;curl@example.com&#x27;, &#x27;password&#x27;: &#x27;CurlPass123!&#x27;, &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;}):
    username = CharField(help_text=&#x27;Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.&#x27;, max_length=150, validators=[&lt;django.contrib.auth.validators.UnicodeUsernameValidator object&gt;, &lt;UniqueValidator(queryset=User.objects.all())&gt;])
    email = EmailField(allow_blank=True, label=&#x27;Email address&#x27;, max_length=254, required=True)
    password = CharField(required=True, validators=[&lt;function validate_password&gt;], write_only=True)
    password2 = CharField(required=True, write_only=True)</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\serializers.py</code>, line 225, in is_valid



            <div class="context" id="c2346530192704">

                <ol start="218" class="pre-context" id="pre2346530192704">

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>        assert hasattr(self, &#x27;initial_data&#x27;), (</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>            &#x27;Cannot call `.is_valid()` as no `data=` keyword argument was &#x27;</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>            &#x27;passed when instantiating the serializer instance.&#x27;</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>        )</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre></pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>        if not hasattr(self, &#x27;_validated_data&#x27;):</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>            try:</pre></li>

                </ol>

              <ol start="225" class="context-line">
                <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>                self._validated_data = self.run_validation(self.initial_data)
                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='226' class="post-context" id="post2346530192704">

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>            except ValidationError as exc:</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>                self._validated_data = {}</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>                self._errors = exc.detail</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>            else:</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre>                self._errors = {}</pre></li>

                  <li onclick="toggle('pre2346530192704', 'post2346530192704')"><pre></pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530192704">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>raise_exception</td>
                    <td class="code"><pre>True</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>UserRegistrationSerializer(context={&#x27;request&#x27;: &lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;, &#x27;format&#x27;: None, &#x27;view&#x27;: &lt;transactions.views.UserRegistrationView object&gt;}, data={&#x27;username&#x27;: &#x27;curluser&#x27;, &#x27;email&#x27;: &#x27;curl@example.com&#x27;, &#x27;password&#x27;: &#x27;CurlPass123!&#x27;, &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;}):
    username = CharField(help_text=&#x27;Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.&#x27;, max_length=150, validators=[&lt;django.contrib.auth.validators.UnicodeUsernameValidator object&gt;, &lt;UniqueValidator(queryset=User.objects.all())&gt;])
    email = EmailField(allow_blank=True, label=&#x27;Email address&#x27;, max_length=254, required=True)
    password = CharField(required=True, validators=[&lt;function validate_password&gt;], write_only=True)
    password2 = CharField(required=True, write_only=True)</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\serializers.py</code>, line 447, in run_validation



            <div class="context" id="c2346530180224">

                <ol start="440" class="pre-context" id="pre2346530180224">

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        (is_empty_value, data) = self.validate_empty_values(data)</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        if is_empty_value:</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>            return data</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        value = self.to_internal_value(data)</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        try:</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>            self.run_validators(value)</pre></li>

                </ol>

              <ol start="447" class="context-line">
                <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>            value = self.validate(value)
                         ^^^^^^^^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='448' class="post-context" id="post2346530180224">

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>            assert value is not None, &#x27;.validate() should return the validated data&#x27;</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        except (ValidationError, DjangoValidationError) as exc:</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>            raise ValidationError(detail=as_serializer_error(exc))</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre></pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre>        return value</pre></li>

                  <li onclick="toggle('pre2346530180224', 'post2346530180224')"><pre></pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530180224">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>data</td>
                    <td class="code"><pre>{&#x27;email&#x27;: &#x27;curl@example.com&#x27;,
 &#x27;password&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;username&#x27;: &#x27;curluser&#x27;}</pre></td>
                  </tr>

                  <tr>
                    <td>is_empty_value</td>
                    <td class="code"><pre>False</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>UserRegistrationSerializer(context={&#x27;request&#x27;: &lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;, &#x27;format&#x27;: None, &#x27;view&#x27;: &lt;transactions.views.UserRegistrationView object&gt;}, data={&#x27;username&#x27;: &#x27;curluser&#x27;, &#x27;email&#x27;: &#x27;curl@example.com&#x27;, &#x27;password&#x27;: &#x27;CurlPass123!&#x27;, &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;}):
    username = CharField(help_text=&#x27;Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.&#x27;, max_length=150, validators=[&lt;django.contrib.auth.validators.UnicodeUsernameValidator object&gt;, &lt;UniqueValidator(queryset=User.objects.all())&gt;])
    email = EmailField(allow_blank=True, label=&#x27;Email address&#x27;, max_length=254, required=True)
    password = CharField(required=True, validators=[&lt;function validate_password&gt;], write_only=True)
    password2 = CharField(required=True, write_only=True)</pre></td>
                  </tr>

                  <tr>
                    <td>value</td>
                    <td class="code"><pre>{&#x27;email&#x27;: &#x27;curl@example.com&#x27;,
 &#x27;password&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;username&#x27;: &#x27;curluser&#x27;}</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame user">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\transactions\serializers.py</code>, line 29, in validate



            <div class="context" id="c2346530184320">

                <ol start="22" class="pre-context" id="pre2346530184320">

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>        }</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre></pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>    def validate(self, attrs):</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>        if attrs[&#x27;password&#x27;] != attrs[&#x27;password2&#x27;]:</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>            raise serializers.ValidationError({&quot;password&quot;: &quot;Password fields didn&#x27;t match.&quot;})</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre></pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>        try:</pre></li>

                </ol>

              <ol start="29" class="context-line">
                <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>            validate_password(attrs[&#x27;password&#x27;], user=User(**attrs))
                                                          ^^^^^^^^^^^^^</pre> <span>…</span></li>
              </ol>

                <ol start='30' class="post-context" id="post2346530184320">

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>        except DjangoValidationError as e:</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>            raise serializers.ValidationError({&quot;password&quot;: list(e.messages)})</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre></pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>        return attrs</pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre></pre></li>

                  <li onclick="toggle('pre2346530184320', 'post2346530184320')"><pre>    def create(self, validated_data):</pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530184320">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>attrs</td>
                    <td class="code"><pre>{&#x27;email&#x27;: &#x27;curl@example.com&#x27;,
 &#x27;password&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;,
 &#x27;username&#x27;: &#x27;curluser&#x27;}</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>UserRegistrationSerializer(context={&#x27;request&#x27;: &lt;rest_framework.request.Request: POST &#x27;/api/auth/register/&#x27;&gt;, &#x27;format&#x27;: None, &#x27;view&#x27;: &lt;transactions.views.UserRegistrationView object&gt;}, data={&#x27;username&#x27;: &#x27;curluser&#x27;, &#x27;email&#x27;: &#x27;curl@example.com&#x27;, &#x27;password&#x27;: &#x27;CurlPass123!&#x27;, &#x27;password2&#x27;: &#x27;CurlPass123!&#x27;}):
    username = CharField(help_text=&#x27;Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.&#x27;, max_length=150, validators=[&lt;django.contrib.auth.validators.UnicodeUsernameValidator object&gt;, &lt;UniqueValidator(queryset=User.objects.all())&gt;])
    email = EmailField(allow_blank=True, label=&#x27;Email address&#x27;, max_length=254, required=True)
    password = CharField(required=True, validators=[&lt;function validate_password&gt;], write_only=True)
    password2 = CharField(required=True, write_only=True)</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>


        <li class="frame django">

            <code class="fname">C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\db\models\base.py</code>, line 569, in __init__



            <div class="context" id="c2346530177920">

                <ol start="562" class="pre-context" id="pre2346530177920">

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                    except FieldDoesNotExist:</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                        unexpected += (prop,)</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                    else:</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                        if value is not _DEFERRED:</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                            _setattr(self, prop, value)</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>            if unexpected:</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                unexpected_names = &quot;, &quot;.join(repr(n) for n in unexpected)</pre></li>

                </ol>

              <ol start="569" class="context-line">
                <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                raise TypeError(
                     ^</pre> <span>…</span></li>
              </ol>

                <ol start='570' class="post-context" id="post2346530177920">

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                    f&quot;{cls.__name__}() got unexpected keyword arguments: &quot;</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                    f&quot;{unexpected_names}&quot;</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>                )</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>        super().__init__()</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre>        post_init.send(sender=cls, instance=self)</pre></li>

                  <li onclick="toggle('pre2346530177920', 'post2346530177920')"><pre></pre></li>

              </ol>

            </div>




              <details>
                <summary class="commands">Local vars</summary>

            <table class="vars" id="v2346530177920">
              <thead>
                <tr>
                  <th scope="col">Variable</th>
                  <th scope="col">Value</th>
                </tr>
              </thead>
              <tbody>

                  <tr>
                    <td>_DEFERRED</td>
                    <td class="code"><pre>&lt;Deferred field&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>__class__</td>
                    <td class="code"><pre>&lt;class &#x27;django.db.models.base.Model&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>_setattr</td>
                    <td class="code"><pre>&lt;built-in function setattr&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>args</td>
                    <td class="code"><pre>()</pre></td>
                  </tr>

                  <tr>
                    <td>cls</td>
                    <td class="code"><pre>&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>field</td>
                    <td class="code"><pre>&lt;django.db.models.fields.DateTimeField: date_joined&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>fields_iter</td>
                    <td class="code"><pre>&lt;tuple_iterator object at 0x0000022257D8BA30&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>is_related_object</td>
                    <td class="code"><pre>False</pre></td>
                  </tr>

                  <tr>
                    <td>kwargs</td>
                    <td class="code"><pre>{&#x27;password2&#x27;: &#x27;CurlPass123!&#x27;}</pre></td>
                  </tr>

                  <tr>
                    <td>opts</td>
                    <td class="code"><pre>&lt;Options for User&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>prop</td>
                    <td class="code"><pre>&#x27;password2&#x27;</pre></td>
                  </tr>

                  <tr>
                    <td>property_names</td>
                    <td class="code"><pre>frozenset({&#x27;pk&#x27;, &#x27;is_authenticated&#x27;, &#x27;is_anonymous&#x27;})</pre></td>
                  </tr>

                  <tr>
                    <td>self</td>
                    <td class="code"><pre>&lt;User: curluser&gt;</pre></td>
                  </tr>

                  <tr>
                    <td>unexpected</td>
                    <td class="code"><pre>(&#x27;password2&#x27;,)</pre></td>
                  </tr>

                  <tr>
                    <td>unexpected_names</td>
                    <td class="code"><pre>&quot;&#x27;password2&#x27;&quot;</pre></td>
                  </tr>

                  <tr>
                    <td>val</td>
                    <td class="code"><pre>datetime.datetime(2025, 7, 4, 16, 29, 2, 31962, tzinfo=datetime.timezone.utc)</pre></td>
                  </tr>

                  <tr>
                    <td>value</td>
                    <td class="code"><pre>&#x27;CurlPass123!&#x27;</pre></td>
                  </tr>

              </tbody>
            </table>
            </details>

        </li>

    </ul>
  </div>

  <form action="https://dpaste.com/" name="pasteform" id="pasteform" method="post">
  <div id="pastebinTraceback" class="pastebin">
    <input type="hidden" name="language" value="PythonConsole">
    <input type="hidden" name="title"
      value="TypeError at /api/auth/register/">
    <input type="hidden" name="source" value="Django Dpaste Agent">
    <input type="hidden" name="poster" value="Django">
    <textarea name="content" id="traceback_area" cols="140" rows="25">
Environment:


Request Method: POST
Request URL: http://127.0.0.1:8000/api/auth/register/

Django Version: 5.2.4
Python Version: 3.12.3
Installed Applications:
[&#x27;django.contrib.admin&#x27;,
 &#x27;django.contrib.auth&#x27;,
 &#x27;django.contrib.contenttypes&#x27;,
 &#x27;django.contrib.sessions&#x27;,
 &#x27;django.contrib.messages&#x27;,
 &#x27;django.contrib.staticfiles&#x27;,
 &#x27;rest_framework&#x27;,
 &#x27;rest_framework_simplejwt&#x27;,
 &#x27;transactions&#x27;]
Installed Middleware:
[&#x27;django.middleware.security.SecurityMiddleware&#x27;,
 &#x27;django.contrib.sessions.middleware.SessionMiddleware&#x27;,
 &#x27;django.middleware.common.CommonMiddleware&#x27;,
 &#x27;django.middleware.csrf.CsrfViewMiddleware&#x27;,
 &#x27;django.contrib.auth.middleware.AuthenticationMiddleware&#x27;,
 &#x27;django.contrib.messages.middleware.MessageMiddleware&#x27;,
 &#x27;django.middleware.clickjacking.XFrameOptionsMiddleware&#x27;]



Traceback (most recent call last):
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\core\handlers\base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\views\decorators\csrf.py", line 65, in _view_wrapper
    return view_func(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\views\generic\base.py", line 105, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py", line 515, in dispatch
    response = self.handle_exception(exc)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py", line 475, in handle_exception
    self.raise_uncaught_exception(exc)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py", line 486, in raise_uncaught_exception
    raise exc
    ^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\views.py", line 512, in dispatch
    response = handler(request, *args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\transactions\views.py", line 19, in post
    serializer.is_valid(raise_exception=True)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\serializers.py", line 225, in is_valid
    self._validated_data = self.run_validation(self.initial_data)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\rest_framework\serializers.py", line 447, in run_validation
    value = self.validate(value)
            ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\transactions\serializers.py", line 29, in validate
    validate_password(attrs[&#x27;password&#x27;], user=User(**attrs))
                                              ^^^^^^^^^^^^^
  File "C:\Users\DELL\OneDrive\Desktop\tracker\venv\Lib\site-packages\django\db\models\base.py", line 569, in __init__
    raise TypeError(
    ^

Exception Type: TypeError at /api/auth/register/
Exception Value: User() got unexpected keyword arguments: &#x27;password2&#x27;
</textarea>
  <br><br>
  <input type="submit" value="Share this traceback on a public website">
  </div>
</form>

</div>


<div id="requestinfo">
  <h2>Request information</h2>



    <h3 id="user-info">USER</h3>
    <p>AnonymousUser</p>


  <h3 id="get-info">GET</h3>

    <p>No GET data</p>


  <h3 id="post-info">POST</h3>

    <p>No POST data</p>


  <h3 id="files-info">FILES</h3>

    <p>No FILES data</p>


  <h3 id="cookie-info">COOKIES</h3>

    <p>No cookie data</p>


  <h3 id="meta-info">META</h3>
  <table class="req">
    <thead>
      <tr>
        <th scope="col">Variable</th>
        <th scope="col">Value</th>
      </tr>
    </thead>
    <tbody>

        <tr>
          <td>ALLUSERSPROFILE</td>
          <td class="code"><pre>&#x27;C:\\ProgramData&#x27;</pre></td>
        </tr>

        <tr>
          <td>APPDATA</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\AppData\\Roaming&#x27;</pre></td>
        </tr>

        <tr>
          <td>CHROME_CRASHPAD_PIPE_NAME</td>
          <td class="code"><pre>&#x27;\\\\.\\pipe\\crashpad_1396_EJFMBTTWZBYFEKGQ&#x27;</pre></td>
        </tr>

        <tr>
          <td>COLORTERM</td>
          <td class="code"><pre>&#x27;truecolor&#x27;</pre></td>
        </tr>

        <tr>
          <td>COMMONPROGRAMFILES</td>
          <td class="code"><pre>&#x27;C:\\Program Files\\Common Files&#x27;</pre></td>
        </tr>

        <tr>
          <td>COMMONPROGRAMFILES(X86)</td>
          <td class="code"><pre>&#x27;C:\\Program Files (x86)\\Common Files&#x27;</pre></td>
        </tr>

        <tr>
          <td>COMMONPROGRAMW6432</td>
          <td class="code"><pre>&#x27;C:\\Program Files\\Common Files&#x27;</pre></td>
        </tr>

        <tr>
          <td>COMPUTERNAME</td>
          <td class="code"><pre>&#x27;DESKTOP-NC9GP8S&#x27;</pre></td>
        </tr>

        <tr>
          <td>COMSPEC</td>
          <td class="code"><pre>&#x27;C:\\WINDOWS\\system32\\cmd.exe&#x27;</pre></td>
        </tr>

        <tr>
          <td>CONTENT_LENGTH</td>
          <td class="code"><pre>&#x27;110&#x27;</pre></td>
        </tr>

        <tr>
          <td>CONTENT_TYPE</td>
          <td class="code"><pre>&#x27;application/json&#x27;</pre></td>
        </tr>

        <tr>
          <td>DJANGO_SETTINGS_MODULE</td>
          <td class="code"><pre>&#x27;expense_tracker_project.settings&#x27;</pre></td>
        </tr>

        <tr>
          <td>DRIVERDATA</td>
          <td class="code"><pre>&#x27;C:\\Windows\\System32\\Drivers\\DriverData&#x27;</pre></td>
        </tr>

        <tr>
          <td>GATEWAY_INTERFACE</td>
          <td class="code"><pre>&#x27;CGI/1.1&#x27;</pre></td>
        </tr>

        <tr>
          <td>GIT_ASKPASS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>HOMEDRIVE</td>
          <td class="code"><pre>&#x27;C:&#x27;</pre></td>
        </tr>

        <tr>
          <td>HOMEPATH</td>
          <td class="code"><pre>&#x27;\\Users\\DELL&#x27;</pre></td>
        </tr>

        <tr>
          <td>HTTP_ACCEPT</td>
          <td class="code"><pre>&#x27;*/*&#x27;</pre></td>
        </tr>

        <tr>
          <td>HTTP_HOST</td>
          <td class="code"><pre>&#x27;127.0.0.1:8000&#x27;</pre></td>
        </tr>

        <tr>
          <td>HTTP_USER_AGENT</td>
          <td class="code"><pre>&#x27;curl/8.9.1&#x27;</pre></td>
        </tr>

        <tr>
          <td>LANG</td>
          <td class="code"><pre>&#x27;en_US.UTF-8&#x27;</pre></td>
        </tr>

        <tr>
          <td>LOCALAPPDATA</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\AppData\\Local&#x27;</pre></td>
        </tr>

        <tr>
          <td>LOGONSERVER</td>
          <td class="code"><pre>&#x27;\\\\DESKTOP-NC9GP8S&#x27;</pre></td>
        </tr>

        <tr>
          <td>NUMBER_OF_PROCESSORS</td>
          <td class="code"><pre>&#x27;4&#x27;</pre></td>
        </tr>

        <tr>
          <td>ONEDRIVE</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\OneDrive&#x27;</pre></td>
        </tr>

        <tr>
          <td>ONEDRIVECONSUMER</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\OneDrive&#x27;</pre></td>
        </tr>

        <tr>
          <td>ORIGINAL_XDG_CURRENT_DESKTOP</td>
          <td class="code"><pre>&#x27;undefined&#x27;</pre></td>
        </tr>

        <tr>
          <td>OS</td>
          <td class="code"><pre>&#x27;Windows_NT&#x27;</pre></td>
        </tr>

        <tr>
          <td>PATH</td>
          <td class="code"><pre>(&#x27;C:\\Users\\DELL\\OneDrive\\Desktop\\tracker\\venv\\Scripts;c:\\Users\\DELL\\AppData\\Local\\Programs\\cursor\\resources\\app\\bin;C:\\Program &#x27;
 &#x27;Files\\Common Files\\Oracle\\Java\\javapath;C:\\Program Files (x86)\\Common &#x27;
 &#x27;Files\\Oracle\\Java\\java8path;C:\\Program Files (x86)\\Common &#x27;
 &#x27;Files\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;C:\\Program &#x27;
 &#x27;Files\\nodejs\\;C:\\Program Files\\Git\\cmd;C:\\Program Files\\Microsoft SQL &#x27;
 &#x27;Server\\150\\Tools\\Binn\\;C:\\Program Files (x86)\\Windows &#x27;
 &#x27;Kits\\10\\Windows Performance &#x27;
 &#x27;Toolkit\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\DELL\\AppData\\Roaming\\npm;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Program &#x27;
 &#x27;Files\\MySQL\\MySQL Server &#x27;
 &#x27;9.3\\bin;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\;C:\\Users\\DELL\\scoop\\shims;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WindowsApps;F:\\Microsoft &#x27;
 &#x27;VS &#x27;
 &#x27;Code\\bin;C:\\Users\\DELL\\AppData\\Roaming\\npm;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Schniz.fnm_Microsoft.Winget.Source_8wekyb3d8bbwe;C:\\Users\\DELL\\AppData\\Local\\Programs\\cursor\\resources\\app\\bin;C:\\Users\\DELL\\Downloads\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin;C:\\Program &#x27;
 &#x27;Files\\Tesseract-OCR\\tesseract.exe;C:\\Program Files\\MySQL\\MySQL Server &#x27;
 &#x27;9.3\\bin;C:\\Program &#x27;
 &#x27;Files\\poppler-24.08.0\\Library\\bin;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\python.exe;&#x27;)</pre></td>
        </tr>

        <tr>
          <td>PATHEXT</td>
          <td class="code"><pre>&#x27;.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL&#x27;</pre></td>
        </tr>

        <tr>
          <td>PATH_INFO</td>
          <td class="code"><pre>&#x27;/api/auth/register/&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROCESSOR_ARCHITECTURE</td>
          <td class="code"><pre>&#x27;AMD64&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROCESSOR_IDENTIFIER</td>
          <td class="code"><pre>&#x27;Intel64 Family 6 Model 142 Stepping 9, GenuineIntel&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROCESSOR_LEVEL</td>
          <td class="code"><pre>&#x27;6&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROCESSOR_REVISION</td>
          <td class="code"><pre>&#x27;8e09&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROGRAMDATA</td>
          <td class="code"><pre>&#x27;C:\\ProgramData&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROGRAMFILES</td>
          <td class="code"><pre>&#x27;C:\\Program Files&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROGRAMFILES(X86)</td>
          <td class="code"><pre>&#x27;C:\\Program Files (x86)&#x27;</pre></td>
        </tr>

        <tr>
          <td>PROGRAMW6432</td>
          <td class="code"><pre>&#x27;C:\\Program Files&#x27;</pre></td>
        </tr>

        <tr>
          <td>PSMODULEPATH</td>
          <td class="code"><pre>(&#x27;C:\\Users\\DELL\\OneDrive\\Documents\\WindowsPowerShell\\Modules;C:\\Program &#x27;
 &#x27;Files\\WindowsPowerShell\\Modules;C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\Modules&#x27;)</pre></td>
        </tr>

        <tr>
          <td>PUBLIC</td>
          <td class="code"><pre>&#x27;C:\\Users\\Public&#x27;</pre></td>
        </tr>

        <tr>
          <td>QUERY_STRING</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>REMOTE_ADDR</td>
          <td class="code"><pre>&#x27;127.0.0.1&#x27;</pre></td>
        </tr>

        <tr>
          <td>REMOTE_HOST</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>REQUEST_METHOD</td>
          <td class="code"><pre>&#x27;POST&#x27;</pre></td>
        </tr>

        <tr>
          <td>RUN_MAIN</td>
          <td class="code"><pre>&#x27;true&#x27;</pre></td>
        </tr>

        <tr>
          <td>SCRIPT_NAME</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>SERVER_NAME</td>
          <td class="code"><pre>&#x27;DESKTOP-NC9GP8S&#x27;</pre></td>
        </tr>

        <tr>
          <td>SERVER_PORT</td>
          <td class="code"><pre>&#x27;8000&#x27;</pre></td>
        </tr>

        <tr>
          <td>SERVER_PROTOCOL</td>
          <td class="code"><pre>&#x27;HTTP/1.1&#x27;</pre></td>
        </tr>

        <tr>
          <td>SERVER_SOFTWARE</td>
          <td class="code"><pre>&#x27;WSGIServer/0.2&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSIONNAME</td>
          <td class="code"><pre>&#x27;Console&#x27;</pre></td>
        </tr>

        <tr>
          <td>SYSTEMDRIVE</td>
          <td class="code"><pre>&#x27;C:&#x27;</pre></td>
        </tr>

        <tr>
          <td>SYSTEMROOT</td>
          <td class="code"><pre>&#x27;C:\\WINDOWS&#x27;</pre></td>
        </tr>

        <tr>
          <td>TEMP</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\AppData\\Local\\Temp&#x27;</pre></td>
        </tr>

        <tr>
          <td>TERM_PROGRAM</td>
          <td class="code"><pre>&#x27;vscode&#x27;</pre></td>
        </tr>

        <tr>
          <td>TERM_PROGRAM_VERSION</td>
          <td class="code"><pre>&#x27;1.101.2&#x27;</pre></td>
        </tr>

        <tr>
          <td>TMP</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\AppData\\Local\\Temp&#x27;</pre></td>
        </tr>

        <tr>
          <td>USERDOMAIN</td>
          <td class="code"><pre>&#x27;DESKTOP-NC9GP8S&#x27;</pre></td>
        </tr>

        <tr>
          <td>USERDOMAIN_ROAMINGPROFILE</td>
          <td class="code"><pre>&#x27;DESKTOP-NC9GP8S&#x27;</pre></td>
        </tr>

        <tr>
          <td>USERNAME</td>
          <td class="code"><pre>&#x27;DELL&#x27;</pre></td>
        </tr>

        <tr>
          <td>USERPROFILE</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL&#x27;</pre></td>
        </tr>

        <tr>
          <td>VIRTUAL_ENV</td>
          <td class="code"><pre>&#x27;C:\\Users\\DELL\\OneDrive\\Desktop\\tracker\\venv&#x27;</pre></td>
        </tr>

        <tr>
          <td>VIRTUAL_ENV_PROMPT</td>
          <td class="code"><pre>&#x27;venv&#x27;</pre></td>
        </tr>

        <tr>
          <td>VSCODE_GIT_ASKPASS_EXTRA_ARGS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>VSCODE_GIT_ASKPASS_MAIN</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>VSCODE_GIT_ASKPASS_NODE</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>VSCODE_GIT_IPC_HANDLE</td>
          <td class="code"><pre>&#x27;\\\\.\\pipe\\vscode-git-b2863e8a38-sock&#x27;</pre></td>
        </tr>

        <tr>
          <td>VSCODE_INJECTION</td>
          <td class="code"><pre>&#x27;1&#x27;</pre></td>
        </tr>

        <tr>
          <td>WINDIR</td>
          <td class="code"><pre>&#x27;C:\\WINDOWS&#x27;</pre></td>
        </tr>

        <tr>
          <td>ZES_ENABLE_SYSMAN</td>
          <td class="code"><pre>&#x27;1&#x27;</pre></td>
        </tr>

        <tr>
          <td>_OLD_VIRTUAL_PATH</td>
          <td class="code"><pre>(&#x27;c:\\Users\\DELL\\AppData\\Local\\Programs\\cursor\\resources\\app\\bin;C:\\Program &#x27;
 &#x27;Files\\Common Files\\Oracle\\Java\\javapath;C:\\Program Files (x86)\\Common &#x27;
 &#x27;Files\\Oracle\\Java\\java8path;C:\\Program Files (x86)\\Common &#x27;
 &#x27;Files\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;C:\\Program &#x27;
 &#x27;Files\\nodejs\\;C:\\Program Files\\Git\\cmd;C:\\Program Files\\Microsoft SQL &#x27;
 &#x27;Server\\150\\Tools\\Binn\\;C:\\Program Files (x86)\\Windows &#x27;
 &#x27;Kits\\10\\Windows Performance &#x27;
 &#x27;Toolkit\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\DELL\\AppData\\Roaming\\npm;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Program &#x27;
 &#x27;Files\\MySQL\\MySQL Server &#x27;
 &#x27;9.3\\bin;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\;C:\\Users\\DELL\\scoop\\shims;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python312\\;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WindowsApps;F:\\Microsoft &#x27;
 &#x27;VS &#x27;
 &#x27;Code\\bin;C:\\Users\\DELL\\AppData\\Roaming\\npm;C:\\Users\\DELL\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Schniz.fnm_Microsoft.Winget.Source_8wekyb3d8bbwe;C:\\Users\\DELL\\AppData\\Local\\Programs\\cursor\\resources\\app\\bin;C:\\Users\\DELL\\Downloads\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin;C:\\Program &#x27;
 &#x27;Files\\Tesseract-OCR\\tesseract.exe;C:\\Program Files\\MySQL\\MySQL Server &#x27;
 &#x27;9.3\\bin;C:\\Program &#x27;
 &#x27;Files\\poppler-24.08.0\\Library\\bin;C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python311\\python.exe;&#x27;)</pre></td>
        </tr>

        <tr>
          <td>wsgi.errors</td>
          <td class="code"><pre>&lt;_io.TextIOWrapper name=&#x27;&lt;stderr&gt;&#x27; mode=&#x27;w&#x27; encoding=&#x27;utf-8&#x27;&gt;</pre></td>
        </tr>

        <tr>
          <td>wsgi.file_wrapper</td>
          <td class="code"><pre>&lt;class &#x27;wsgiref.util.FileWrapper&#x27;&gt;</pre></td>
        </tr>

        <tr>
          <td>wsgi.input</td>
          <td class="code"><pre>&lt;django.core.handlers.wsgi.LimitedStream object at 0x0000022257E9B9D0&gt;</pre></td>
        </tr>

        <tr>
          <td>wsgi.multiprocess</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>wsgi.multithread</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>wsgi.run_once</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>wsgi.url_scheme</td>
          <td class="code"><pre>&#x27;http&#x27;</pre></td>
        </tr>

        <tr>
          <td>wsgi.version</td>
          <td class="code"><pre>(1, 0)</pre></td>
        </tr>

    </tbody>
  </table>


  <h3 id="settings-info">Settings</h3>
  <h4>Using settings module <code>expense_tracker_project.settings</code></h4>
  <table class="req">
    <thead>
      <tr>
        <th scope="col">Setting</th>
        <th scope="col">Value</th>
      </tr>
    </thead>
    <tbody>

        <tr>
          <td>ABSOLUTE_URL_OVERRIDES</td>
          <td class="code"><pre>{}</pre></td>
        </tr>

        <tr>
          <td>ADMINS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>ALLOWED_HOSTS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>APPEND_SLASH</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>AUTHENTICATION_BACKENDS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>AUTH_PASSWORD_VALIDATORS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>AUTH_USER_MODEL</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>BASE_DIR</td>
          <td class="code"><pre>WindowsPath(&#x27;C:/Users/DELL/OneDrive/Desktop/tracker&#x27;)</pre></td>
        </tr>

        <tr>
          <td>CACHES</td>
          <td class="code"><pre>{&#x27;default&#x27;: {&#x27;BACKEND&#x27;: &#x27;django.core.cache.backends.locmem.LocMemCache&#x27;}}</pre></td>
        </tr>

        <tr>
          <td>CACHE_MIDDLEWARE_ALIAS</td>
          <td class="code"><pre>&#x27;default&#x27;</pre></td>
        </tr>

        <tr>
          <td>CACHE_MIDDLEWARE_KEY_PREFIX</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>CACHE_MIDDLEWARE_SECONDS</td>
          <td class="code"><pre>600</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_AGE</td>
          <td class="code"><pre>31449600</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_DOMAIN</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_HTTPONLY</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_NAME</td>
          <td class="code"><pre>&#x27;csrftoken&#x27;</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_PATH</td>
          <td class="code"><pre>&#x27;/&#x27;</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_SAMESITE</td>
          <td class="code"><pre>&#x27;Lax&#x27;</pre></td>
        </tr>

        <tr>
          <td>CSRF_COOKIE_SECURE</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>CSRF_FAILURE_VIEW</td>
          <td class="code"><pre>&#x27;django.views.csrf.csrf_failure&#x27;</pre></td>
        </tr>

        <tr>
          <td>CSRF_HEADER_NAME</td>
          <td class="code"><pre>&#x27;HTTP_X_CSRFTOKEN&#x27;</pre></td>
        </tr>

        <tr>
          <td>CSRF_TRUSTED_ORIGINS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>CSRF_USE_SESSIONS</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>DATABASES</td>
          <td class="code"><pre>{&#x27;default&#x27;: {&#x27;ATOMIC_REQUESTS&#x27;: False,
             &#x27;AUTOCOMMIT&#x27;: True,
             &#x27;CONN_HEALTH_CHECKS&#x27;: False,
             &#x27;CONN_MAX_AGE&#x27;: 0,
             &#x27;ENGINE&#x27;: &#x27;django.db.backends.sqlite3&#x27;,
             &#x27;HOST&#x27;: &#x27;&#x27;,
             &#x27;NAME&#x27;: WindowsPath(&#x27;C:/Users/DELL/OneDrive/Desktop/tracker/db.sqlite3&#x27;),
             &#x27;OPTIONS&#x27;: {},
             &#x27;PASSWORD&#x27;: &#x27;********************&#x27;,
             &#x27;PORT&#x27;: &#x27;&#x27;,
             &#x27;TEST&#x27;: {&#x27;CHARSET&#x27;: None,
                      &#x27;COLLATION&#x27;: None,
                      &#x27;MIGRATE&#x27;: True,
                      &#x27;MIRROR&#x27;: None,
                      &#x27;NAME&#x27;: None},
             &#x27;TIME_ZONE&#x27;: None,
             &#x27;USER&#x27;: &#x27;&#x27;}}</pre></td>
        </tr>

        <tr>
          <td>DATABASE_ROUTERS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>DATA_UPLOAD_MAX_MEMORY_SIZE</td>
          <td class="code"><pre>2621440</pre></td>
        </tr>

        <tr>
          <td>DATA_UPLOAD_MAX_NUMBER_FIELDS</td>
          <td class="code"><pre>1000</pre></td>
        </tr>

        <tr>
          <td>DATA_UPLOAD_MAX_NUMBER_FILES</td>
          <td class="code"><pre>100</pre></td>
        </tr>

        <tr>
          <td>DATETIME_FORMAT</td>
          <td class="code"><pre>&#x27;N j, Y, P&#x27;</pre></td>
        </tr>

        <tr>
          <td>DATETIME_INPUT_FORMATS</td>
          <td class="code"><pre>[&#x27;%Y-%m-%d %H:%M:%S&#x27;,
 &#x27;%Y-%m-%d %H:%M:%S.%f&#x27;,
 &#x27;%Y-%m-%d %H:%M&#x27;,
 &#x27;%m/%d/%Y %H:%M:%S&#x27;,
 &#x27;%m/%d/%Y %H:%M:%S.%f&#x27;,
 &#x27;%m/%d/%Y %H:%M&#x27;,
 &#x27;%m/%d/%y %H:%M:%S&#x27;,
 &#x27;%m/%d/%y %H:%M:%S.%f&#x27;,
 &#x27;%m/%d/%y %H:%M&#x27;]</pre></td>
        </tr>

        <tr>
          <td>DATE_FORMAT</td>
          <td class="code"><pre>&#x27;N j, Y&#x27;</pre></td>
        </tr>

        <tr>
          <td>DATE_INPUT_FORMATS</td>
          <td class="code"><pre>[&#x27;%Y-%m-%d&#x27;,
 &#x27;%m/%d/%Y&#x27;,
 &#x27;%m/%d/%y&#x27;,
 &#x27;%b %d %Y&#x27;,
 &#x27;%b %d, %Y&#x27;,
 &#x27;%d %b %Y&#x27;,
 &#x27;%d %b, %Y&#x27;,
 &#x27;%B %d %Y&#x27;,
 &#x27;%B %d, %Y&#x27;,
 &#x27;%d %B %Y&#x27;,
 &#x27;%d %B, %Y&#x27;]</pre></td>
        </tr>

        <tr>
          <td>DEBUG</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>DEBUG_PROPAGATE_EXCEPTIONS</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>DECIMAL_SEPARATOR</td>
          <td class="code"><pre>&#x27;.&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_AUTO_FIELD</td>
          <td class="code"><pre>&#x27;django.db.models.BigAutoField&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_CHARSET</td>
          <td class="code"><pre>&#x27;utf-8&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_EXCEPTION_REPORTER</td>
          <td class="code"><pre>&#x27;django.views.debug.ExceptionReporter&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_EXCEPTION_REPORTER_FILTER</td>
          <td class="code"><pre>&#x27;django.views.debug.SafeExceptionReporterFilter&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_FROM_EMAIL</td>
          <td class="code"><pre>&#x27;webmaster@localhost&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_INDEX_TABLESPACE</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>DEFAULT_TABLESPACE</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>DISALLOWED_USER_AGENTS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>EMAIL_BACKEND</td>
          <td class="code"><pre>&#x27;django.core.mail.backends.smtp.EmailBackend&#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_HOST</td>
          <td class="code"><pre>&#x27;localhost&#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_HOST_PASSWORD</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_HOST_USER</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_PORT</td>
          <td class="code"><pre>25</pre></td>
        </tr>

        <tr>
          <td>EMAIL_SSL_CERTFILE</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>EMAIL_SSL_KEYFILE</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_SUBJECT_PREFIX</td>
          <td class="code"><pre>&#x27;[Django] &#x27;</pre></td>
        </tr>

        <tr>
          <td>EMAIL_TIMEOUT</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>EMAIL_USE_LOCALTIME</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>EMAIL_USE_SSL</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>EMAIL_USE_TLS</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>FILE_UPLOAD_DIRECTORY_PERMISSIONS</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>FILE_UPLOAD_HANDLERS</td>
          <td class="code"><pre>[&#x27;django.core.files.uploadhandler.MemoryFileUploadHandler&#x27;,
 &#x27;django.core.files.uploadhandler.TemporaryFileUploadHandler&#x27;]</pre></td>
        </tr>

        <tr>
          <td>FILE_UPLOAD_MAX_MEMORY_SIZE</td>
          <td class="code"><pre>2621440</pre></td>
        </tr>

        <tr>
          <td>FILE_UPLOAD_PERMISSIONS</td>
          <td class="code"><pre>420</pre></td>
        </tr>

        <tr>
          <td>FILE_UPLOAD_TEMP_DIR</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>FIRST_DAY_OF_WEEK</td>
          <td class="code"><pre>0</pre></td>
        </tr>

        <tr>
          <td>FIXTURE_DIRS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>FORCE_SCRIPT_NAME</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>FORMAT_MODULE_PATH</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>FORMS_URLFIELD_ASSUME_HTTPS</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>FORM_RENDERER</td>
          <td class="code"><pre>&#x27;django.forms.renderers.DjangoTemplates&#x27;</pre></td>
        </tr>

        <tr>
          <td>IGNORABLE_404_URLS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>INSTALLED_APPS</td>
          <td class="code"><pre>[&#x27;django.contrib.admin&#x27;,
 &#x27;django.contrib.auth&#x27;,
 &#x27;django.contrib.contenttypes&#x27;,
 &#x27;django.contrib.sessions&#x27;,
 &#x27;django.contrib.messages&#x27;,
 &#x27;django.contrib.staticfiles&#x27;,
 &#x27;rest_framework&#x27;,
 &#x27;rest_framework_simplejwt&#x27;,
 &#x27;transactions&#x27;]</pre></td>
        </tr>

        <tr>
          <td>INTERNAL_IPS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>LANGUAGES</td>
          <td class="code"><pre>[(&#x27;af&#x27;, &#x27;Afrikaans&#x27;),
 (&#x27;ar&#x27;, &#x27;Arabic&#x27;),
 (&#x27;ar-dz&#x27;, &#x27;Algerian Arabic&#x27;),
 (&#x27;ast&#x27;, &#x27;Asturian&#x27;),
 (&#x27;az&#x27;, &#x27;Azerbaijani&#x27;),
 (&#x27;bg&#x27;, &#x27;Bulgarian&#x27;),
 (&#x27;be&#x27;, &#x27;Belarusian&#x27;),
 (&#x27;bn&#x27;, &#x27;Bengali&#x27;),
 (&#x27;br&#x27;, &#x27;Breton&#x27;),
 (&#x27;bs&#x27;, &#x27;Bosnian&#x27;),
 (&#x27;ca&#x27;, &#x27;Catalan&#x27;),
 (&#x27;ckb&#x27;, &#x27;Central Kurdish (Sorani)&#x27;),
 (&#x27;cs&#x27;, &#x27;Czech&#x27;),
 (&#x27;cy&#x27;, &#x27;Welsh&#x27;),
 (&#x27;da&#x27;, &#x27;Danish&#x27;),
 (&#x27;de&#x27;, &#x27;German&#x27;),
 (&#x27;dsb&#x27;, &#x27;Lower Sorbian&#x27;),
 (&#x27;el&#x27;, &#x27;Greek&#x27;),
 (&#x27;en&#x27;, &#x27;English&#x27;),
 (&#x27;en-au&#x27;, &#x27;Australian English&#x27;),
 (&#x27;en-gb&#x27;, &#x27;British English&#x27;),
 (&#x27;eo&#x27;, &#x27;Esperanto&#x27;),
 (&#x27;es&#x27;, &#x27;Spanish&#x27;),
 (&#x27;es-ar&#x27;, &#x27;Argentinian Spanish&#x27;),
 (&#x27;es-co&#x27;, &#x27;Colombian Spanish&#x27;),
 (&#x27;es-mx&#x27;, &#x27;Mexican Spanish&#x27;),
 (&#x27;es-ni&#x27;, &#x27;Nicaraguan Spanish&#x27;),
 (&#x27;es-ve&#x27;, &#x27;Venezuelan Spanish&#x27;),
 (&#x27;et&#x27;, &#x27;Estonian&#x27;),
 (&#x27;eu&#x27;, &#x27;Basque&#x27;),
 (&#x27;fa&#x27;, &#x27;Persian&#x27;),
 (&#x27;fi&#x27;, &#x27;Finnish&#x27;),
 (&#x27;fr&#x27;, &#x27;French&#x27;),
 (&#x27;fy&#x27;, &#x27;Frisian&#x27;),
 (&#x27;ga&#x27;, &#x27;Irish&#x27;),
 (&#x27;gd&#x27;, &#x27;Scottish Gaelic&#x27;),
 (&#x27;gl&#x27;, &#x27;Galician&#x27;),
 (&#x27;he&#x27;, &#x27;Hebrew&#x27;),
 (&#x27;hi&#x27;, &#x27;Hindi&#x27;),
 (&#x27;hr&#x27;, &#x27;Croatian&#x27;),
 (&#x27;hsb&#x27;, &#x27;Upper Sorbian&#x27;),
 (&#x27;hu&#x27;, &#x27;Hungarian&#x27;),
 (&#x27;hy&#x27;, &#x27;Armenian&#x27;),
 (&#x27;ia&#x27;, &#x27;Interlingua&#x27;),
 (&#x27;id&#x27;, &#x27;Indonesian&#x27;),
 (&#x27;ig&#x27;, &#x27;Igbo&#x27;),
 (&#x27;io&#x27;, &#x27;Ido&#x27;),
 (&#x27;is&#x27;, &#x27;Icelandic&#x27;),
 (&#x27;it&#x27;, &#x27;Italian&#x27;),
 (&#x27;ja&#x27;, &#x27;Japanese&#x27;),
 (&#x27;ka&#x27;, &#x27;Georgian&#x27;),
 (&#x27;kab&#x27;, &#x27;Kabyle&#x27;),
 (&#x27;kk&#x27;, &#x27;Kazakh&#x27;),
 (&#x27;km&#x27;, &#x27;Khmer&#x27;),
 (&#x27;kn&#x27;, &#x27;Kannada&#x27;),
 (&#x27;ko&#x27;, &#x27;Korean&#x27;),
 (&#x27;ky&#x27;, &#x27;Kyrgyz&#x27;),
 (&#x27;lb&#x27;, &#x27;Luxembourgish&#x27;),
 (&#x27;lt&#x27;, &#x27;Lithuanian&#x27;),
 (&#x27;lv&#x27;, &#x27;Latvian&#x27;),
 (&#x27;mk&#x27;, &#x27;Macedonian&#x27;),
 (&#x27;ml&#x27;, &#x27;Malayalam&#x27;),
 (&#x27;mn&#x27;, &#x27;Mongolian&#x27;),
 (&#x27;mr&#x27;, &#x27;Marathi&#x27;),
 (&#x27;ms&#x27;, &#x27;Malay&#x27;),
 (&#x27;my&#x27;, &#x27;Burmese&#x27;),
 (&#x27;nb&#x27;, &#x27;Norwegian Bokmål&#x27;),
 (&#x27;ne&#x27;, &#x27;Nepali&#x27;),
 (&#x27;nl&#x27;, &#x27;Dutch&#x27;),
 (&#x27;nn&#x27;, &#x27;Norwegian Nynorsk&#x27;),
 (&#x27;os&#x27;, &#x27;Ossetic&#x27;),
 (&#x27;pa&#x27;, &#x27;Punjabi&#x27;),
 (&#x27;pl&#x27;, &#x27;Polish&#x27;),
 (&#x27;pt&#x27;, &#x27;Portuguese&#x27;),
 (&#x27;pt-br&#x27;, &#x27;Brazilian Portuguese&#x27;),
 (&#x27;ro&#x27;, &#x27;Romanian&#x27;),
 (&#x27;ru&#x27;, &#x27;Russian&#x27;),
 (&#x27;sk&#x27;, &#x27;Slovak&#x27;),
 (&#x27;sl&#x27;, &#x27;Slovenian&#x27;),
 (&#x27;sq&#x27;, &#x27;Albanian&#x27;),
 (&#x27;sr&#x27;, &#x27;Serbian&#x27;),
 (&#x27;sr-latn&#x27;, &#x27;Serbian Latin&#x27;),
 (&#x27;sv&#x27;, &#x27;Swedish&#x27;),
 (&#x27;sw&#x27;, &#x27;Swahili&#x27;),
 (&#x27;ta&#x27;, &#x27;Tamil&#x27;),
 (&#x27;te&#x27;, &#x27;Telugu&#x27;),
 (&#x27;tg&#x27;, &#x27;Tajik&#x27;),
 (&#x27;th&#x27;, &#x27;Thai&#x27;),
 (&#x27;tk&#x27;, &#x27;Turkmen&#x27;),
 (&#x27;tr&#x27;, &#x27;Turkish&#x27;),
 (&#x27;tt&#x27;, &#x27;Tatar&#x27;),
 (&#x27;udm&#x27;, &#x27;Udmurt&#x27;),
 (&#x27;ug&#x27;, &#x27;Uyghur&#x27;),
 (&#x27;uk&#x27;, &#x27;Ukrainian&#x27;),
 (&#x27;ur&#x27;, &#x27;Urdu&#x27;),
 (&#x27;uz&#x27;, &#x27;Uzbek&#x27;),
 (&#x27;vi&#x27;, &#x27;Vietnamese&#x27;),
 (&#x27;zh-hans&#x27;, &#x27;Simplified Chinese&#x27;),
 (&#x27;zh-hant&#x27;, &#x27;Traditional Chinese&#x27;)]</pre></td>
        </tr>

        <tr>
          <td>LANGUAGES_BIDI</td>
          <td class="code"><pre>[&#x27;he&#x27;, &#x27;ar&#x27;, &#x27;ar-dz&#x27;, &#x27;ckb&#x27;, &#x27;fa&#x27;, &#x27;ug&#x27;, &#x27;ur&#x27;]</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_CODE</td>
          <td class="code"><pre>&#x27;en-us&#x27;</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_AGE</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_DOMAIN</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_HTTPONLY</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_NAME</td>
          <td class="code"><pre>&#x27;django_language&#x27;</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_PATH</td>
          <td class="code"><pre>&#x27;/&#x27;</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_SAMESITE</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>LANGUAGE_COOKIE_SECURE</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>LOCALE_PATHS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>LOGGING</td>
          <td class="code"><pre>{}</pre></td>
        </tr>

        <tr>
          <td>LOGGING_CONFIG</td>
          <td class="code"><pre>&#x27;logging.config.dictConfig&#x27;</pre></td>
        </tr>

        <tr>
          <td>LOGIN_REDIRECT_URL</td>
          <td class="code"><pre>&#x27;/accounts/profile/&#x27;</pre></td>
        </tr>

        <tr>
          <td>LOGIN_URL</td>
          <td class="code"><pre>&#x27;/accounts/login/&#x27;</pre></td>
        </tr>

        <tr>
          <td>LOGOUT_REDIRECT_URL</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>MANAGERS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>MEDIA_ROOT</td>
          <td class="code"><pre>&#x27;&#x27;</pre></td>
        </tr>

        <tr>
          <td>MEDIA_URL</td>
          <td class="code"><pre>&#x27;/&#x27;</pre></td>
        </tr>

        <tr>
          <td>MESSAGE_STORAGE</td>
          <td class="code"><pre>&#x27;django.contrib.messages.storage.fallback.FallbackStorage&#x27;</pre></td>
        </tr>

        <tr>
          <td>MIDDLEWARE</td>
          <td class="code"><pre>[&#x27;django.middleware.security.SecurityMiddleware&#x27;,
 &#x27;django.contrib.sessions.middleware.SessionMiddleware&#x27;,
 &#x27;django.middleware.common.CommonMiddleware&#x27;,
 &#x27;django.middleware.csrf.CsrfViewMiddleware&#x27;,
 &#x27;django.contrib.auth.middleware.AuthenticationMiddleware&#x27;,
 &#x27;django.contrib.messages.middleware.MessageMiddleware&#x27;,
 &#x27;django.middleware.clickjacking.XFrameOptionsMiddleware&#x27;]</pre></td>
        </tr>

        <tr>
          <td>MIGRATION_MODULES</td>
          <td class="code"><pre>{}</pre></td>
        </tr>

        <tr>
          <td>MONTH_DAY_FORMAT</td>
          <td class="code"><pre>&#x27;F j&#x27;</pre></td>
        </tr>

        <tr>
          <td>NUMBER_GROUPING</td>
          <td class="code"><pre>0</pre></td>
        </tr>

        <tr>
          <td>PASSWORD_HASHERS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>PASSWORD_RESET_TIMEOUT</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>PREPEND_WWW</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>REST_FRAMEWORK</td>
          <td class="code"><pre>{&#x27;DEFAULT_AUTHENTICATION_CLASSES&#x27;: &#x27;********************&#x27;,
 &#x27;DEFAULT_PAGINATION_CLASS&#x27;: &#x27;rest_framework.pagination.PageNumberPagination&#x27;,
 &#x27;DEFAULT_PERMISSION_CLASSES&#x27;: [&#x27;rest_framework.permissions.IsAuthenticated&#x27;],
 &#x27;PAGE_SIZE&#x27;: 10}</pre></td>
        </tr>

        <tr>
          <td>ROOT_URLCONF</td>
          <td class="code"><pre>&#x27;expense_tracker_project.urls&#x27;</pre></td>
        </tr>

        <tr>
          <td>SECRET_KEY</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>SECRET_KEY_FALLBACKS</td>
          <td class="code"><pre>&#x27;********************&#x27;</pre></td>
        </tr>

        <tr>
          <td>SECURE_CONTENT_TYPE_NOSNIFF</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>SECURE_CROSS_ORIGIN_OPENER_POLICY</td>
          <td class="code"><pre>&#x27;same-origin&#x27;</pre></td>
        </tr>

        <tr>
          <td>SECURE_HSTS_INCLUDE_SUBDOMAINS</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SECURE_HSTS_PRELOAD</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SECURE_HSTS_SECONDS</td>
          <td class="code"><pre>0</pre></td>
        </tr>

        <tr>
          <td>SECURE_PROXY_SSL_HEADER</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>SECURE_REDIRECT_EXEMPT</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>SECURE_REFERRER_POLICY</td>
          <td class="code"><pre>&#x27;same-origin&#x27;</pre></td>
        </tr>

        <tr>
          <td>SECURE_SSL_HOST</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>SECURE_SSL_REDIRECT</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SERVER_EMAIL</td>
          <td class="code"><pre>&#x27;root@localhost&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_CACHE_ALIAS</td>
          <td class="code"><pre>&#x27;default&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_AGE</td>
          <td class="code"><pre>1209600</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_DOMAIN</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_HTTPONLY</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_NAME</td>
          <td class="code"><pre>&#x27;sessionid&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_PATH</td>
          <td class="code"><pre>&#x27;/&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_SAMESITE</td>
          <td class="code"><pre>&#x27;Lax&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_COOKIE_SECURE</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SESSION_ENGINE</td>
          <td class="code"><pre>&#x27;django.contrib.sessions.backends.db&#x27;</pre></td>
        </tr>

        <tr>
          <td>SESSION_EXPIRE_AT_BROWSER_CLOSE</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SESSION_FILE_PATH</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>SESSION_SAVE_EVERY_REQUEST</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>SESSION_SERIALIZER</td>
          <td class="code"><pre>&#x27;django.contrib.sessions.serializers.JSONSerializer&#x27;</pre></td>
        </tr>

        <tr>
          <td>SETTINGS_MODULE</td>
          <td class="code"><pre>&#x27;expense_tracker_project.settings&#x27;</pre></td>
        </tr>

        <tr>
          <td>SHORT_DATETIME_FORMAT</td>
          <td class="code"><pre>&#x27;m/d/Y P&#x27;</pre></td>
        </tr>

        <tr>
          <td>SHORT_DATE_FORMAT</td>
          <td class="code"><pre>&#x27;m/d/Y&#x27;</pre></td>
        </tr>

        <tr>
          <td>SIGNING_BACKEND</td>
          <td class="code"><pre>&#x27;django.core.signing.TimestampSigner&#x27;</pre></td>
        </tr>

        <tr>
          <td>SILENCED_SYSTEM_CHECKS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>SIMPLE_JWT</td>
          <td class="code"><pre>{&#x27;ACCESS_TOKEN_LIFETIME&#x27;: &#x27;********************&#x27;,
 &#x27;ALGORITHM&#x27;: &#x27;HS256&#x27;,
 &#x27;AUDIENCE&#x27;: None,
 &#x27;AUTH_HEADER_NAME&#x27;: &#x27;********************&#x27;,
 &#x27;AUTH_HEADER_TYPES&#x27;: &#x27;********************&#x27;,
 &#x27;AUTH_TOKEN_CLASSES&#x27;: &#x27;********************&#x27;,
 &#x27;BLACKLIST_AFTER_ROTATION&#x27;: True,
 &#x27;ISSUER&#x27;: None,
 &#x27;JTI_CLAIM&#x27;: &#x27;jti&#x27;,
 &#x27;JTI_TOKEN_TYPE&#x27;: &#x27;********************&#x27;,
 &#x27;JWK_URL&#x27;: None,
 &#x27;LEEWAY&#x27;: 0,
 &#x27;REFRESH_TOKEN_LIFETIME&#x27;: &#x27;********************&#x27;,
 &#x27;ROTATE_REFRESH_TOKENS&#x27;: &#x27;********************&#x27;,
 &#x27;SIGNING_KEY&#x27;: &#x27;********************&#x27;,
 &#x27;SLIDING_TOKEN_LIFETIME&#x27;: &#x27;********************&#x27;,
 &#x27;SLIDING_TOKEN_REFRESH_EXP_CLAIM&#x27;: &#x27;********************&#x27;,
 &#x27;SLIDING_TOKEN_REFRESH_LIFETIME&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_BLACKLIST_SERIALIZER&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_OBTAIN_SERIALIZER&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_REFRESH_SERIALIZER&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_TYPE_CLAIM&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_USER_CLASS&#x27;: &#x27;********************&#x27;,
 &#x27;TOKEN_VERIFY_SERIALIZER&#x27;: &#x27;********************&#x27;,
 &#x27;UPDATE_LAST_LOGIN&#x27;: False,
 &#x27;USER_AUTHENTICATION_RULE&#x27;: &#x27;********************&#x27;,
 &#x27;USER_ID_CLAIM&#x27;: &#x27;user_id&#x27;,
 &#x27;USER_ID_FIELD&#x27;: &#x27;id&#x27;,
 &#x27;VERIFYING_KEY&#x27;: &#x27;********************&#x27;}</pre></td>
        </tr>

        <tr>
          <td>STATICFILES_DIRS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>STATICFILES_FINDERS</td>
          <td class="code"><pre>[&#x27;django.contrib.staticfiles.finders.FileSystemFinder&#x27;,
 &#x27;django.contrib.staticfiles.finders.AppDirectoriesFinder&#x27;]</pre></td>
        </tr>

        <tr>
          <td>STATIC_ROOT</td>
          <td class="code"><pre>None</pre></td>
        </tr>

        <tr>
          <td>STATIC_URL</td>
          <td class="code"><pre>&#x27;/static/&#x27;</pre></td>
        </tr>

        <tr>
          <td>STORAGES</td>
          <td class="code"><pre>{&#x27;default&#x27;: {&#x27;BACKEND&#x27;: &#x27;django.core.files.storage.FileSystemStorage&#x27;},
 &#x27;staticfiles&#x27;: {&#x27;BACKEND&#x27;: &#x27;django.contrib.staticfiles.storage.StaticFilesStorage&#x27;}}</pre></td>
        </tr>

        <tr>
          <td>TEMPLATES</td>
          <td class="code"><pre>[{&#x27;APP_DIRS&#x27;: True,
  &#x27;BACKEND&#x27;: &#x27;django.template.backends.django.DjangoTemplates&#x27;,
  &#x27;DIRS&#x27;: [],
  &#x27;OPTIONS&#x27;: {&#x27;context_processors&#x27;: [&#x27;django.template.context_processors.debug&#x27;,
                                     &#x27;django.template.context_processors.request&#x27;,
                                     &#x27;django.contrib.auth.context_processors.auth&#x27;,
                                     &#x27;django.contrib.messages.context_processors.messages&#x27;]}}]</pre></td>
        </tr>

        <tr>
          <td>TEST_NON_SERIALIZED_APPS</td>
          <td class="code"><pre>[]</pre></td>
        </tr>

        <tr>
          <td>TEST_RUNNER</td>
          <td class="code"><pre>&#x27;django.test.runner.DiscoverRunner&#x27;</pre></td>
        </tr>

        <tr>
          <td>THOUSAND_SEPARATOR</td>
          <td class="code"><pre>&#x27;,&#x27;</pre></td>
        </tr>

        <tr>
          <td>TIME_FORMAT</td>
          <td class="code"><pre>&#x27;P&#x27;</pre></td>
        </tr>

        <tr>
          <td>TIME_INPUT_FORMATS</td>
          <td class="code"><pre>[&#x27;%H:%M:%S&#x27;, &#x27;%H:%M:%S.%f&#x27;, &#x27;%H:%M&#x27;]</pre></td>
        </tr>

        <tr>
          <td>TIME_ZONE</td>
          <td class="code"><pre>&#x27;UTC&#x27;</pre></td>
        </tr>

        <tr>
          <td>USE_I18N</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>USE_THOUSAND_SEPARATOR</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>USE_TZ</td>
          <td class="code"><pre>True</pre></td>
        </tr>

        <tr>
          <td>USE_X_FORWARDED_HOST</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>USE_X_FORWARDED_PORT</td>
          <td class="code"><pre>False</pre></td>
        </tr>

        <tr>
          <td>WSGI_APPLICATION</td>
          <td class="code"><pre>&#x27;expense_tracker_project.wsgi.application&#x27;</pre></td>
        </tr>

        <tr>
          <td>X_FRAME_OPTIONS</td>
          <td class="code"><pre>&#x27;DENY&#x27;</pre></td>
        </tr>

        <tr>
          <td>YEAR_MONTH_FORMAT</td>
          <td class="code"><pre>&#x27;F Y&#x27;</pre></td>
        </tr>

    </tbody>
  </table>

</div>
</main>


  <footer id="explanation">
    <p>
      You’re seeing this error because you have <code>DEBUG = True</code> in your
      Django settings file. Change that to <code>False</code>, and Django will
      display a standard page generated by the handler for this status code.
    </p>
  </footer>

</body>
</html>

C:\Users\DELL>cd ..

C:\Users>cd Dell.

C:\Users\DELL>cd .

C:\Users\DELL>cd
C:\Users\DELL

C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/auth/register/" -H "Content-Type: application/json" -d "{\"username\": \"curluser\", \"email\": \"curl@example.com\", \"password\": \"CurlPass123!\", \"password2\": \"CurlPass123!\"}"
{"message":"User registered successfully.","username":"curluser","email":"curl@example.com"}
C:\Users\DELL>curl -X POST \  http://127.0.0.1:8000/api/auth/login/ \  -H 'Content-Type: application/json' \  -d '{    "username": "testuser",    "password": "securepassword123"  }'
curl: (3) URL rejected: Bad hostname
{"username":["This field is required."],"password":["This field is required."]}curl: (3) URL rejected: Bad hostname
curl: (6) Could not resolve host: application
curl: (3) URL rejected: Bad hostname
curl: (3) URL rejected: Port number was not a decimal number between 0 and 65535
curl: (3) URL rejected: Bad hostname
curl: (3) URL rejected: Port number was not a decimal number between 0 and 65535
curl: (6) Could not resolve host: securepassword123
curl: (3) unmatched close brace/bracket in URL position 1:
}'
 ^

C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/auth/login/" -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"securepassword123\"}"
{"detail":"No active account found with the given credentials"}
C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/expenses/" ^
More?   -H "Content-Type: application/json" ^
More?   -H "Authorization: Bearer YOUR_ACCESS_TOKEN" ^
More?
More?
{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is invalid"}]}curl: (3) URL rejected: Malformed input to a URL function

C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/expenses/" ^
More?   -H "Content-Type: application/json" ^
More?   -H "Authorization: Bearer YOUR_ACCESS_TOKEN" ^
More?   -H "Authorization: Bearer YOUR_ACCESS_TOKEN" ^
More?
More?
{"detail":"Authorization header must contain two space-delimited values","code":"bad_authorization_header"}curl: (3) URL rejected: Malformed input to a URL function

C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/expenses/" ^  -H "Content-Type: application/json" ^  -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjQ3MzM2LCJpYXQiOjE3NTE2NDcwMzYsImp0aSI6IjdhMWZlODRkNjM1MTQ5ODI4OGM5NDU5Njg0MDgzZGM0IiwidXNlcl9pZCI6NH0.C2dyzfUNwEFQwtJbIJjCoVA_opj-oKYmJvFcqTZ6qDk" ^  -d "{\"title\": \"First Expense\", \"description\": \"Bought coffee\", \"amount\": 5.50, \"transaction_type\": \"debit\", \"tax\": 0.00, \"tax_type\": \"flat\", \"date\": \"2025-07-04\"}"
{"detail":"Authentication credentials were not provided."}
C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/expenses/" ^
More?   -H "Content-Type: application/json" ^
More?   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjQ3MzM2LCJpYXQiOjE3NTE2NDcwMzYsImp0aSI6IjdhMWZlODRkNjM1MTQ5ODI4OGM5NDU5Njg0MDgzZGM0IiwidXNlcl9pZCI6NH0.C2dyzfUNwEFQwtJbIJjCoVA_opj-oKYmJvFcqTZ6qDk" ^
More?   -d "{\"title\": \"First Expense\", \"description\": \"Bought coffee\", \"amount\": 5.50, \"transaction_type\": \"debit\", \"tax\": 0.00, \"tax_type\": \"flat\", \"date\": \"2025-07-04\"}"
{"id":2,"title":"First Expense","description":"Bought coffee","amount":"5.50","transaction_type":"debit","tax":"0.00","tax_type":"flat","date":"2025-07-04","total":"5.50","created_at":"2025-07-04T16:41:40.690232Z","updated_at":"2025-07-04T16:41:40.690232Z"}
C:\Users\DELL>curl -X PATCH \
curl: (3) URL rejected: Bad hostname

C:\Users\DELL>  http://127.0.0.1:8000/api/expenses/1/ \
'http:' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>  -H 'Content-Type: application/json' \
'-H' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>  -H 'Authorization: Bearer eyJYOUR_ACCESS_TOKEN_HERE' \
'-H' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>  -d '{
'-d' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>    "description": "Updated description for laptop purchase",
'"description":' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>    "amount": 1550.00
'"amount":' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\DELL>curl -X PATCH "http://127.0.0.1:8000/api/expenses/RECORD_ID/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{\"description\": \"Updated description for laptop purchase\", \"amount\": 1550.00}"
{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is invalid"}]}
C:\Users\DELL>curl -X PATCH "http://127.0.0.1:8000/api/expenses/RECORD_ID/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjQ3MzM2LCJpYXQiOjE3NTE2NDcwMzYsImp0aSI6IjdhMWZlODRkNjM1MTQ5ODI4OGM5NDU5Njg0MDgzZGM0IiwidXNlcl9pZCI6NH0.C2dyzfUNwEFQwtJbIJjCoVA_opj-oKYmJvFcqTZ6qDk" -d "{\"description\": \"Updated description for laptop purchase\", \"amount\": 1550.00}"
{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is expired"}]}
C:\Users\DELL>curl -X PATCH "http://127.0.0.1:8000/api/expenses/RECORD_ID/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjQ3MzM2LCJpYXQiOjE3NTE2NDcwMzYsImp0aSI6IjdhMWZlODRkNjM1MTQ5ODI4OGM5NDU5Njg0MDgzZGM0IiwidXNlcl9pZCI6NH0.C2dyzfUNwEFQwtJbIJjCoVA_opj-oKYmJvFcqTZ6qDk" -d "{\"description\": \"Updated description for laptop purchase\", \"amount\": 1550.00}"curl -X PATCH "http://127.0.0.1:8000/api/expenses/RECORD_ID/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjQ3MzM2LCJpYXQiOjE3NTE2NDcwMzYsImp0aSI6IjdhMWZlODRkNjM1MTQ5ODI4OGM5NDU5Njg0MDgzZGM0IiwidXNlcl9pZCI6NH0.C2dyzfUNwEFQwtJbIJjCoVA_opj-oKYmJvFcqTZ6qDk" -d "{\"description\": \"Updated description for laptop purchase\", \"amount\": 1550.00}"
{"detail":"Authorization header must contain two space-delimited values","code":"bad_authorization_header"}{"detail":"Authorization header must contain two space-delimited values","code":"bad_authorization_header"}
C:\Users\DELL>curl -X POST "http://127.0.0.1:8000/api/auth/login/" -H "Content-Type: application/json" -d "{\"username\": \"newuser\", \"password\": \"SecurePass123\"}"
{"detail":"No active account found with the given credentials"}
C:\Users\DELL>curl -X GET "http://127.0.0.1:8000/api/expenses/" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is invalid"}]}
C:\Users\DELL>
