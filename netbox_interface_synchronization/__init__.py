from netbox.plugins import PluginConfig


class NCSConfig(PluginConfig):
    name = 'netbox_interface_synchronization'
    verbose_name = 'NetBox Component Synchronization'
    description = 'Syncing existing component names and types with those from a new device type in NetBox'
    version = '4.5.1'
    author = 'Keith Knowles, Bastian Leicht, Chris Russell, Antoine Keranflech'
    author_email = 'NetTech2001@github.com'
    default_settings = {
        'exclude_virtual_interfaces': True,
        'include_interfaces_panel': False,
        # Compare description during diff
        # If compare is true, description will also be synced to device
        # Otherwise not.
        'compare_description': True
    }


config = NCSConfig
