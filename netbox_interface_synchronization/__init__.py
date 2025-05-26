from netbox.plugins import PluginConfig


class Config(PluginConfig):
    name = 'netbox_interface_synchronization'
    verbose_name = 'NetBox Interface Synchronization'
    description = 'Syncing existing interface names and types with those from a new device type in NetBox'
    version = '5.0.0'
    author = 'Keith Knowles and Bastian Leicht'
    author_email = 'mkknowles@outlook.com'
    default_settings = {
        'exclude_virtual_interfaces': True,
        'include_interfaces_panel': False,
        # Compare description during diff
        # If compare is true, description will also be synced to device
        # Otherwise not.
        'compare_description': True
    }


config = Config
