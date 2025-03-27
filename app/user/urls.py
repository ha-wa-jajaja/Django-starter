"""
URL mappings for the user API.
"""

from django.urls import path
from user import views, views_admin

app_name = "user"

urlpatterns = [
    # NOTE: .as_view() converts a class-based view into a function that can be used in URL patterns.
    # NOTE: The name='create' parameter in the URL pattern allows referencing URLs by name rather than their actual path
    # Can be used to:
    # 1. Reverse URL lookups in Django templates using the {% url 'user:create' %} syntax
    # 2. Generate URLs in views using reverse('user:create')
    # 3. Create links in app without hardcoding URLs
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    # Admin only endpoints
    path(
        "admin/list/", views_admin.AdminListUsersView.as_view(), name="admin_user_list"
    ),
    path(
        # NOTE: In Django the angle brackets <> are used to capture parts of the URL as parameters
        # Here:
        # 1. Captures a numeric value from the URL
        # 2. Converts it to an integer
        # 3. Passes it to the view as a parameter named "pk" (primary key)
        "admin/user/<int:pk>/",
        views_admin.AdminUserDetailView.as_view(),
        name="admin_user_detail",
    ),
]
