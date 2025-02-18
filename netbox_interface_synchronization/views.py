from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from dcim.models import Device, Interface, InterfaceTemplate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.contrib import messages

from .utils import UnifiedInterface, natural_keys
from .forms import InterfaceComparisonForm

config = settings.PLUGINS_CONFIG['netbox_interface_synchronization']


class InterfaceComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of interfaces between a device and a device type and beautiful visualization"""
    permission_required = ("dcim.view_interface", "dcim.add_interface", "dcim.change_interface", "dcim.delete_interface")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))
        interfaces = device.vc_interfaces()
        if config["exclude_virtual_interfaces"]:
            interfaces = list(filter(lambda i: not i.is_virtual, interfaces))
        interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

        unified_interfaces = [UnifiedInterface(i.id, i.name, i.type, i.get_type_display()) for i in interfaces]
        unified_interface_templates = [
            UnifiedInterface(i.id, i.name, i.type, i.get_type_display(), i.mgmt_only, is_template=True) for i in interface_templates]

        # List of interfaces and interface templates presented in the unified format
        overall_interfaces = list(set(unified_interface_templates + unified_interfaces))
        overall_interfaces.sort(key=lambda o: natural_keys(o.name))

        comparison_templates = []
        comparison_interfaces = []
        for i in overall_interfaces:
            try:
                comparison_templates.append(unified_interface_templates[unified_interface_templates.index(i)])
            except ValueError:
                comparison_templates.append(None)

            try:
                comparison_interfaces.append(unified_interfaces[unified_interfaces.index(i)])
            except ValueError:
                comparison_interfaces.append(None)

        comparison_items = list(zip(comparison_templates, comparison_interfaces))
        return render(
            request, "netbox_interface_synchronization/interface_comparison.html",
            {
                "comparison_items": comparison_items,
                "templates_count": len(interface_templates),
                "interfaces_count": len(interfaces),
                "device": device
             }
        )

    def post(self, request, device_id):
        form = InterfaceComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))
            interfaces = device.vc_interfaces()
            if config["exclude_virtual_interfaces"]:
                interfaces = interfaces.exclude(type__in=["virtual", "lag"])
            interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

            # Manually validating interfaces and interface templates lists
            add_to_device = filter(
                lambda i: i in interface_templates.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("add_to_device")))
            )
            remove_from_device = filter(
                lambda i: i in interfaces.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("remove_from_device")))
            )

            # Remove selected interfaces from the device and count them
            interfaces_deleted = Interface.objects.filter(id__in=remove_from_device).delete()[0]

            # Add selected interfaces to the device and count them
            add_to_device_interfaces = InterfaceTemplate.objects.filter(id__in=add_to_device)

            interfaces_created = 0
            for i in add_to_device_interfaces:
                ni = Interface(device=device, name=i.name, type=i.type, mgmt_only=i.mgmt_only)
                ni.full_clean()
                ni.save()
                interfaces_created = interfaces_created + 1

            # Getting and validating a list of interfaces to rename
            fix_name_interfaces = filter(lambda i: str(i.id) in request.POST.getlist("fix_name"), interfaces)
            # Casting interface templates into UnifiedInterface objects for proper comparison with interfaces for renaming
            unified_interface_templates = [
                UnifiedInterface(i.id, i.name, i.type,i.mgmt_only, i.get_type_display()) for i in interface_templates]

            # Rename selected interfaces
            interfaces_fixed = 0
            for interface in fix_name_interfaces:
                unified_interface = UnifiedInterface(interface.id, interface.name, interface.type, interface.mgmt_only, interface.get_type_display())
                try:
                    # Try to extract an interface template with the corresponding name
                    corresponding_template = unified_interface_templates[unified_interface_templates.index(unified_interface)]
                    interface.name = corresponding_template.name
                    interface.save()
                    interfaces_fixed += 1
                except ValueError:
                    pass

            # Generating result message
            message = []
            if interfaces_created > 0:
                message.append(f"created {interfaces_created} interfaces")
            if interfaces_deleted > 0:
                message.append(f"deleted {interfaces_deleted} interfaces")
            if interfaces_fixed > 0:
                message.append(f"fixed {interfaces_fixed} interfaces")
            messages.success(request, "; ".join(message).capitalize())

            return redirect(request.path)
