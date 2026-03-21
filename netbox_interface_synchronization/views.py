from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from dcim.models import Device, Interface, InterfaceTemplate, PowerPort, PowerPortTemplate, ConsolePort, \
    ConsolePortTemplate, ConsoleServerPort, ConsoleServerPortTemplate, DeviceBay, DeviceBayTemplate, FrontPort, \
    FrontPortTemplate, PowerOutlet, PowerOutletTemplate, RearPort, RearPortTemplate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.contrib import messages

from .utils import get_components, post_components
from .comparison import FrontPortComparison, PowerPortComparison, PowerOutletComparison, InterfaceComparison, \
    ConsolePortComparison, ConsoleServerPortComparison, DeviceBayComparison, RearPortComparison
from .forms import ComponentComparisonForm

config = settings.PLUGINS_CONFIG['netbox_interface_synchronization']


class InterfaceComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of interfaces between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_interface", "dcim.add_interface", "dcim.change_interface", "dcim.delete_interface")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))
        interfaces = device.vc_interfaces()
        if config["exclude_virtual_interfaces"]:
            interfaces = list(filter(lambda i: not i.is_virtual, interfaces))
        interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

        unified_interfaces = [
            InterfaceComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.mgmt_only) for i
            in interfaces]
        unified_interface_templates = [
            InterfaceComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.mgmt_only,
                                is_template=True) for i in interface_templates]

        return get_components(request, device, interfaces, unified_interfaces, unified_interface_templates,
                              "Interfaces")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))
            interfaces = device.vc_interfaces()
            if config["exclude_virtual_interfaces"]:
                interfaces = interfaces.exclude(type__in=["virtual", "lag"])
            interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of interfaces to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), interfaces
            )

            unified_interface_templates = [
                InterfaceComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.mgmt_only,
                                    is_template=True) for i in interface_templates]

            unified_interfaces = []

            for component in fix_name_components:
                unified_interfaces.append((component, InterfaceComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description,
                    component.type,
                    component.get_type_display(),
                    component.mgmt_only)))

            return post_components(request, device, interfaces, interface_templates, Interface, InterfaceTemplate,
                                   unified_interfaces, unified_interface_templates, "interfaces")


class PowerPortComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of power ports between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_powerport", "dcim.add_powerport", "dcim.change_powerport", "dcim.delete_powerport")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        powerports = device.powerports.all()
        powerports_templates = PowerPortTemplate.objects.filter(device_type=device.device_type)

        unified_powerports = [
            PowerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.maximum_draw,
                                i.allocated_draw) for i in powerports]
        unified_powerport_templates = [
            PowerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.maximum_draw,
                                i.allocated_draw, is_template=True) for i in powerports_templates]

        return get_components(request, device, powerports, unified_powerports, unified_powerport_templates,
                              "Power ports")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            powerports = device.powerports.all()
            powerports_templates = PowerPortTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of power ports to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), powerports
            )

            unified_powerport_templates = [
                PowerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.maximum_draw,
                                    i.allocated_draw, is_template=True) for i in powerports_templates]

            unified_powerports = []

            for component in fix_name_components:
                unified_powerports.append((component, PowerPortComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description,
                    component.type,
                    component.get_type_display(),
                    component.maximum_draw,
                    component.allocated_draw)))

            return post_components(request, device, powerports, powerports_templates, PowerPort, PowerPortTemplate,
                                   unified_powerports, unified_powerport_templates, "power ports")


class ConsolePortComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of console ports between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_consoleport", "dcim.add_consoleport", "dcim.change_consoleport", "dcim.delete_consoleport")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        consoleports = device.consoleports.all()
        consoleports_templates = ConsolePortTemplate.objects.filter(device_type=device.device_type)

        unified_consoleports = [
            ConsolePortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display()) for i in
            consoleports]
        unified_consoleport_templates = [
            ConsolePortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), is_template=True)
            for i in consoleports_templates]

        return get_components(request, device, consoleports, unified_consoleports, unified_consoleport_templates,
                              "Console ports")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            consoleports = device.consoleports.all()
            consoleports_templates = ConsolePortTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of console ports to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), consoleports
            )

            unified_consoleport_templates = [
                ConsolePortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                      is_template=True) for i in consoleports_templates]

            unified_consoleports = []

            for component in fix_name_components:
                unified_consoleports.append((component, ConsolePortComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description,
                    component.type,
                    component.get_type_display())))

            return post_components(request, device, consoleports, consoleports_templates, ConsolePort,
                                   ConsolePortTemplate, unified_consoleports, unified_consoleport_templates,
                                   "console ports")


class ConsoleServerPortComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of console server ports between a device and a device type and beautiful visualization"""
    permission_required = ("dcim.view_consoleserverport", "dcim.add_consoleserverport", "dcim.change_consoleserverport",
                           "dcim.delete_consoleserverport")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        consoleserverports = device.consoleserverports.all()
        consoleserverports_templates = ConsoleServerPortTemplate.objects.filter(device_type=device.device_type)

        unified_consoleserverports = [
            ConsoleServerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display()) for i in
            consoleserverports]
        unified_consoleserverport_templates = [
            ConsoleServerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                        is_template=True) for i in consoleserverports_templates]

        return get_components(request, device, consoleserverports, unified_consoleserverports,
                              unified_consoleserverport_templates, "Console server ports")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            consoleserverports = device.consoleserverports.all()
            consoleserverports_templates = ConsoleServerPortTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of console server ports to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), consoleserverports
            )

            unified_consoleserverport_templates = [
                ConsoleServerPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                            is_template=True) for i in consoleserverports_templates]

            unified_consoleserverports = []

            for component in fix_name_components:
                unified_consoleserverports.append((component, ConsoleServerPortComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description,
                    component.type,
                    component.get_type_display())))

            return post_components(request, device, consoleserverports, consoleserverports_templates, ConsoleServerPort,
                                   ConsoleServerPortTemplate, unified_consoleserverports,
                                   unified_consoleserverport_templates, "console server ports")


class PowerOutletComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of power outlets between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_poweroutlet", "dcim.add_poweroutlet", "dcim.change_poweroutlet", "dcim.delete_poweroutlet")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        poweroutlets = device.poweroutlets.all()
        poweroutlets_templates = PowerOutletTemplate.objects.filter(device_type=device.device_type)

        unified_poweroutlets = [
            PowerOutletComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                  power_port_name=PowerPort.objects.get(
                                      id=i.power_port_id).name if i.power_port_id is not None else "",
                                  feed_leg=i.feed_leg) for i in poweroutlets]
        unified_poweroutlet_templates = [
            PowerOutletComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                  power_port_name=PowerPortTemplate.objects.get(
                                      id=i.power_port_id).name if i.power_port_id is not None else "",
                                  feed_leg=i.feed_leg, is_template=True) for i in poweroutlets_templates]

        return get_components(request, device, poweroutlets, unified_poweroutlets, unified_poweroutlet_templates,
                              "Power outlets")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            poweroutlets = device.poweroutlets.all()
            poweroutlets_templates = PowerOutletTemplate.objects.filter(device_type=device.device_type)

            # Generating result message
            message = []
            created = 0
            updated = 0
            fixed = 0

            remove_from_device = filter(
                lambda i: i in poweroutlets.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("remove_from_device")))
            )

            # Remove selected power outlets from the device and count them
            deleted = PowerOutlet.objects.filter(id__in=remove_from_device).delete()[0]

            # Get device power ports to check dependency between power outlets
            device_pp = PowerPort.objects.filter(device_id=device.id)

            matching = {}
            mismatch = False
            for i in poweroutlets_templates:
                found = False
                if i.power_port_id is not None:
                    ppt = PowerPortTemplate.objects.get(id=i.power_port_id)
                    for pp in device_pp:
                        if pp.name == ppt.name:
                            # Save matching to add the correct power port later
                            matching[i.id] = pp.id
                            found = True

                    # If at least one power port is not found in device there is a dependency
                    # Better not to sync at all
                    if not found:
                        mismatch = True
                        break

            if not mismatch:
                add_to_device = filter(
                    lambda i: i in poweroutlets_templates.values_list("id", flat=True),
                    map(int, filter(lambda x: x.isdigit(), request.POST.getlist("add_to_device")))
                )

                # Add selected component to the device and count them
                add_to_device_component = PowerOutletTemplate.objects.filter(id__in=add_to_device)

                bulk_create = []
                updated = 0
                keys_to_avoid = ["id"]

                if not config["compare_description"]:
                    keys_to_avoid.append("description")

                for i in add_to_device_component.values():
                    to_create = False

                    try:
                        # If power outlets already exists, update and do not recreate
                        po = device.poweroutlets.get(name=i["name"])
                    except PowerOutlet.DoesNotExist:
                        po = PowerOutlet()
                        po.device = device
                        to_create = True

                    # Copy all fields from template
                    for k in i.keys():
                        if k not in keys_to_avoid:
                            setattr(po, k, i[k])
                    po.power_port_id = matching.get(i["id"], None)

                    if to_create:
                        bulk_create.append(po)
                    else:
                        po.save()
                        updated += 1

                created = len(PowerOutlet.objects.bulk_create(bulk_create))

                # Getting and validating a list of components to rename
                fix_name_components = filter(lambda i: str(i.id) in request.POST.getlist("fix_name"), poweroutlets)

                # Casting component templates into Unified objects for proper comparison with component for renaming
                unified_component_templates = [
                    PowerOutletComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(),
                                          power_port_name=PowerPortTemplate.objects.get(
                                              id=i.power_port_id).name if i.power_port_id is not None else "",
                                          feed_leg=i.feed_leg, is_template=True) for i in poweroutlets_templates]

                # Rename selected power outlets
                fixed = 0
                for component in fix_name_components:
                    unified_poweroutlet = PowerOutletComparison(component.id, component.name, component.label,
                                                                component.description, component.type,
                                                                component.get_type_display(),
                                                                power_port_name=PowerPort.objects.get(
                                                                    id=component.power_port_id).name if component.power_port_id is not None else "",
                                                                feed_leg=component.feed_leg)

                    try:
                        # Try to extract a component template with the corresponding name
                        corresponding_template = unified_component_templates[
                            unified_component_templates.index(unified_poweroutlet)]
                        component.name = corresponding_template.name
                        component.save()
                        fixed += 1
                    except ValueError:
                        pass
            else:
                messages.error(request, "Dependecy detected, sync power ports first!")

            if created > 0:
                message.append(f"created {created} power outlets")
            if updated > 0:
                message.append(f"updated {updated} power outlets")
            if deleted > 0:
                message.append(f"deleted {deleted} power outlets")
            if fixed > 0:
                message.append(f"fixed {fixed} power outlets")

            messages.info(request, "; ".join(message).capitalize())

            return redirect(request.path)


class FrontPortComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of front ports between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_frontport", "dcim.add_frontport", "dcim.change_frontport", "dcim.delete_frontport")

    def get(self, request, device_id):

        device = get_object_or_404(Device.objects.filter(id=device_id))

        frontports = device.frontports.all()
        frontports_templates = FrontPortTemplate.objects.filter(device_type=device.device_type)

        unified_frontports = [
            FrontPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color,
                                i.rear_port_position) for i in frontports]
        unified_frontports_templates = [
            FrontPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color,
                                i.rear_port_position, is_template=True) for i in frontports_templates]

        return get_components(request, device, frontports, unified_frontports, unified_frontports_templates,
                              "Front ports")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            frontports = device.frontports.all()
            frontports_templates = FrontPortTemplate.objects.filter(device_type=device.device_type)

            # Generating result message
            message = []
            created = 0
            updated = 0
            fixed = 0

            remove_from_device = filter(
                lambda i: i in frontports.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("remove_from_device")))
            )

            # Remove selected front ports from the device and count them
            deleted = FrontPort.objects.filter(id__in=remove_from_device).delete()[0]

            # Get device rear ports to check dependency between front ports
            device_rp = RearPort.objects.filter(device_id=device.id)

            matching = {}
            mismatch = False
            for i in frontports_templates:
                found = False
                if i.rear_port_id is not None:
                    rpt = RearPortTemplate.objects.get(id=i.rear_port_id)
                    for rp in device_rp:
                        if rp.name == rpt.name:
                            # Save matching to add the correct rear port later
                            matching[i.id] = rp.id
                            found = True

                    # If at least one rear port is not found in device there is a dependency
                    # Better not to sync at all
                    if not found:
                        mismatch = True
                        break

            if not mismatch:
                add_to_device = filter(
                    lambda i: i in frontports_templates.values_list("id", flat=True),
                    map(int, filter(lambda x: x.isdigit(), request.POST.getlist("add_to_device")))
                )

                # Add selected component to the device and count them
                add_to_device_component = FrontPortTemplate.objects.filter(id__in=add_to_device)

                bulk_create = []
                updated = 0
                keys_to_avoid = ["id"]

                if not config["compare_description"]:
                    keys_to_avoid.append("description")

                for i in add_to_device_component.values():
                    to_create = False

                    try:
                        # If fron port already exists, update and do not recreate
                        fp = device.frontports.get(name=i["name"])
                    except FrontPort.DoesNotExist:
                        fp = FrontPort()
                        fp.device = device
                        to_create = True

                    # Copy all fields from template
                    for k in i.keys():
                        if k not in keys_to_avoid:
                            setattr(fp, k, i[k])
                    fp.rear_port_id = matching.get(i["id"], None)

                    if to_create:
                        bulk_create.append(fp)
                    else:
                        fp.save()
                        updated += 1

                created = len(FrontPort.objects.bulk_create(bulk_create))

                # Getting and validating a list of components to rename
                fix_name_components = filter(lambda i: str(i.id) in request.POST.getlist("fix_name"), frontports)

                # Casting component templates into Unified objects for proper comparison with component for renaming
                unified_frontports_templates = [
                    FrontPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color,
                                        i.rear_port_position, is_template=True) for i in frontports_templates]
                # Rename selected front ports
                fixed = 0
                for component in fix_name_components:
                    unified_frontport = FrontPortComparison(component.id, component.name, component.label,
                                                            component.description, component.type,
                                                            component.get_type_display(), component.color,
                                                            component.rear_port_position)

                    try:
                        # Try to extract a component template with the corresponding name
                        corresponding_template = unified_frontports_templates[
                            unified_frontports_templates.index(unified_frontport)]
                        component.name = corresponding_template.name
                        component.save()
                        fixed += 1
                    except ValueError:
                        pass
            else:
                messages.error(request, "Dependecy detected, sync rear ports first!")

            if created > 0:
                message.append(f"created {created} front ports")
            if updated > 0:
                message.append(f"updated {updated} front ports")
            if deleted > 0:
                message.append(f"deleted {deleted} front ports")
            if fixed > 0:
                message.append(f"fixed {fixed} front ports")

            messages.info(request, "; ".join(message).capitalize())

            return redirect(request.path)


class RearPortComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of rear ports between a device and a device type and beautiful visualization"""
    permission_required = ("dcim.view_rearport", "dcim.add_rearport", "dcim.change_rearport", "dcim.delete_rearport")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        rearports = device.rearports.all()
        rearports_templates = RearPortTemplate.objects.filter(device_type=device.device_type)

        unified_rearports = [
            RearPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color, i.positions)
            for i in rearports]
        unified_rearports_templates = [
            RearPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color, i.positions,
                               is_template=True) for i in rearports_templates]

        return get_components(request, device, rearports, unified_rearports, unified_rearports_templates, "Rear ports")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            rearports = device.rearports.all()
            rearports_templates = RearPortTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of rear ports to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), rearports
            )

            unified_rearports_templates = [
                RearPortComparison(i.id, i.name, i.label, i.description, i.type, i.get_type_display(), i.color,
                                   i.positions, is_template=True) for i in rearports_templates]

            unified_rearports = []

            for component in fix_name_components:
                unified_rearports.append((component, RearPortComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description,
                    component.type,
                    component.get_type_display(),
                    component.color,
                    component.positions)))

            return post_components(request, device, rearports, rearports_templates, RearPort, RearPortTemplate,
                                   unified_rearports, unified_rearports_templates, "rear ports")

        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            rearports = device.rearports.all()
            rearports_templates = RearPortTemplate.objects.filter(device_type=device.device_type)

            return post_components(request, device, rearports, rearports_templates, RearPort, RearPortTemplate)


class DeviceBayComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of device bays between a device and a device type and beautiful visualization"""
    permission_required = (
    "dcim.view_devicebay", "dcim.add_devicebay", "dcim.change_devicebay", "dcim.delete_devicebay")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))

        devicebays = device.devicebays.all()
        devicebays_templates = DeviceBayTemplate.objects.filter(device_type=device.device_type)

        unified_devicebays = [DeviceBayComparison(i.id, i.name, i.label, i.description) for i in devicebays]
        unified_devicebay_templates = [
            DeviceBayComparison(i.id, i.name, i.label, i.description, is_template=True) for i in devicebays_templates]

        return get_components(request, device, devicebays, unified_devicebays, unified_devicebay_templates,
                              "Device bays")

    def post(self, request, device_id):
        form = ComponentComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))

            devicebays = device.devicebays.all()
            devicebays_templates = DeviceBayTemplate.objects.filter(device_type=device.device_type)

            # Getting and validating a list of devicebays to rename
            fix_name_components = filter(
                lambda i: str(i.id) in request.POST.getlist("fix_name"), devicebays
            )

            unified_devicebay_templates = [
                DeviceBayComparison(i.id, i.name, i.label, i.description, is_template=True) for i in
                devicebays_templates]

            unified_devicebays = []

            for component in fix_name_components:
                unified_devicebays.append((component, DeviceBayComparison(
                    component.id,
                    component.name,
                    component.label,
                    component.description
                )))

            return post_components(request, device, devicebays, devicebays_templates, DeviceBay, DeviceBayTemplate,
                                   unified_devicebays, unified_devicebay_templates, "device bays")