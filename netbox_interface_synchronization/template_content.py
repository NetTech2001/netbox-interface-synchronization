from netbox.plugins import PluginTemplateExtension
from dcim.models import Interface, InterfaceTemplate


class DeviceViewExtension(PluginTemplateExtension):
    model = "dcim.device"
    models = [model]

    def buttons(self):
        """Implements a compare interfaces button at the top of the page"""
        obj = self.context['object']
        return self.render("netbox_interface_synchronization/compare_interfaces_button.html", extra_context={
            "device": obj
        })

    def right_page(self):
        """Implements a panel with the number of interfaces on the right side of the page"""
        obj = self.context['object']
        interfaces = Interface.objects.filter(device=obj)
        real_interfaces = interfaces.exclude(type__in=["virtual", "lag"])
        interface_templates = InterfaceTemplate.objects.filter(device_type=obj.device_type)

        return self.render("netbox_interface_synchronization/number_of_interfaces_panel.html", extra_context={
            "interfaces": interfaces,
            "real_interfaces": real_interfaces,
            "interface_templates": interface_templates
        })


template_extensions = [DeviceViewExtension]
