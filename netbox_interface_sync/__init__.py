from netbox.plugins import PluginConfig


class Config(PluginConfig):
    name = 'netbox4_interface_sync'
    verbose_name = 'NetBox 4 Interface Synchronization'
    description = 'Syncing existing interfaces with the interfaces from a new device type in NetBox 4'
    version = '4.0.2'
    author = 'Keith Knowles'
    author_email = 'mkknowles@outlook.com'
    default_settings = {
        'exclude_virtual_interfaces': True
    }


config = Config
