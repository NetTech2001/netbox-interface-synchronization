from django.urls import path

from . import views


# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path(
        "interface-comparison/<int:device_id>/",
        views.InterfaceComparisonView.as_view(),
        name="interface_comparison",
    ),
    path(
        "powerport-comparison/<int:device_id>/",
        views.PowerPortComparisonView.as_view(),
        name="powerport_comparison",
    ),
    path(
        "consoleport-comparison/<int:device_id>/",
        views.ConsolePortComparisonView.as_view(),
        name="consoleport_comparison",
    ),
    path(
        "consoleserverport-comparison/<int:device_id>/",
        views.ConsoleServerPortComparisonView.as_view(),
        name="consoleserverport_comparison",
    ),
    path(
        "poweroutlet-comparison/<int:device_id>/",
        views.PowerOutletComparisonView.as_view(),
        name="poweroutlet_comparison",
    ),
    path(
        "frontport-comparison/<int:device_id>/",
        views.FrontPortComparisonView.as_view(),
        name="frontport_comparison",
    ),
    path(
        "rearport-comparison/<int:device_id>/",
        views.RearPortComparisonView.as_view(),
        name="rearport_comparison",
    ),
    path(
        "devicebay-comparison/<int:device_id>/",
        views.DeviceBayComparisonView.as_view(),
        name="devicebay_comparison",
    ),
    path(
        "modulebay-comparison/<int:device_id>/",
        views.ModuleBayComparisonView.as_view(),
        name="modulebay_comparison",
    ),
)
