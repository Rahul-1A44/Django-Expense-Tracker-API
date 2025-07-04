from rest_framework import viewsets, status, generics 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ExpenseIncome
from .serializers import ExpenseIncomeSerializer, ExpenseIncomeListSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse 


def api_root_view(request):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expense/Income Tracker API</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background-color: #f4f4f4; color: #333; }}
            .container {{ max-width: 800px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }}
            h2 {{ color: #0056b3; margin-top: 25px; margin-bottom: 15px; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 8px; }}
            a {{ color: #007bff; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            code {{ background-color: #e9e9e9; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Expense/Income Tracker API!</h1>
            <p>This is the root endpoint for your personal finance tracking API.</p>

            <h2>Authentication Endpoints:</h2>
            <ul>
                <li><strong>Register:</strong> <code>POST</code> <a href="{request.build_absolute_uri('api/auth/register/')}" target="_blank">{request.build_absolute_uri('api/auth/register/')}</a></li>
                <li><strong>Login:</strong> <code>POST</code> <a href="{request.build_absolute_uri('api/auth/login/')}" target="_blank">{request.build_absolute_uri('api/auth/login/')}</a> (Returns JWT access and refresh tokens)</li>
                <li><strong>Refresh Token:</strong> <code>POST</code> <a href="{request.build_absolute_uri('api/auth/refresh/')}" target="_blank">{request.build_absolute_uri('api/auth/refresh/')}</a></li>
            </ul>

            <h2>Expense/Income Records Endpoints:</h2>
            <p>These endpoints require authentication (JWT Bearer token in 'Authorization' header).</p>
            <ul>
                <li><strong>List/Create Records:</strong> <code>GET</code>/<code>POST</code> <a href="{request.build_absolute_uri('api/expenses/')}" target="_blank">{request.build_absolute_uri('api/expenses/')}</a></li>
                <li><strong>Retrieve/Update/Delete Specific Record:</strong> <code>GET</code>/<code>PUT</code>/<code>PATCH</code>/<code>DELETE</code> <a href="{request.build_absolute_uri('api/expenses/{id}/')}" target="_blank">{request.build_absolute_uri('api/expenses/{id}/')}</a></li>
            </ul>

            <p>For API interaction, use tools like Postman or curl.</p>
            <p>Access the <a href="{request.build_absolute_uri('admin/')}" target="_blank">Django Admin Panel</a> to manage users and data directly.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows creation of new user accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully.",
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)


class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    queryset = ExpenseIncome.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ExpenseIncomeListSerializer
        return ExpenseIncomeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-date', '-created_at')
        else:
            return ExpenseIncome.objects.filter(user=user).order_by('-date', '-created_at')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_superuser or instance.user == user:
            instance.delete()
        else:
            self.permission_denied(
                self.request,
                message="You do not have permission to delete this record."
            )