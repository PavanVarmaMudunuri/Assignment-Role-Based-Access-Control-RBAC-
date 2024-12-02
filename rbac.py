from django.conf import settings
from django.core.management import call_command
from django.core.management.utils import get_random_secret_key
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import django
import os
import json

# Django Settings Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY=get_random_secret_key(),
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
    )

# Setup Django
django.setup()

# Run migrations
call_command('migrate', verbosity=0)

# Helper function for token generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Setup roles and permissions
def setup_roles_and_permissions():
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    user_group, _ = Group.objects.get_or_create(name='User')
    moderator_group, _ = Group.objects.get_or_create(name='Moderator')

    content_type = ContentType.objects.get_for_model(User)

    manage_users_permission, _ = Permission.objects.get_or_create(
        codename='manage_users',
        name='Can manage users',
        content_type=content_type,
    )

    view_dashboard_permission, _ = Permission.objects.get_or_create(
        codename='view_dashboard',
        name='Can view dashboard',
        content_type=content_type,
    )

    admin_group.permissions.add(manage_users_permission, view_dashboard_permission)
    moderator_group.permissions.add(view_dashboard_permission)

# REST API views
@csrf_exempt
@api_view(['POST'])
def register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if role not in ['Admin', 'User', 'Moderator']:
        return JsonResponse({'error': 'Invalid role'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    group = Group.objects.get(name=role)
    user.groups.add(group)
    user.save()

    return JsonResponse({'message': 'User registered successfully'}, status=201)

@csrf_exempt
@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

    tokens = get_tokens_for_user(user)
    return JsonResponse(tokens)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.user.groups.filter(name__in=['Admin', 'Moderator']).exists():
        return JsonResponse({'message': 'Welcome to the dashboard!'}, status=200)
    return JsonResponse({'error': 'Access Denied'}, status=403)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manage_users(request):
    if request.user.groups.filter(name='Admin').exists():
        return JsonResponse({'message': 'User management access granted.'}, status=200)
    return JsonResponse({'error': 'Access Denied'}, status=403)

# Initialize roles and permissions
setup_roles_and_permissions()

# URL routing
from django.urls import path
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('dashboard/', dashboard),
    path('admin/manage/', manage_users),
]

# Run Django server
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
