from django.urls import path

from . import views


# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path("interface-comparison/<int:device_id>/", views.InterfaceComparisonView.as_view(), name="interface_comparison"),
)
