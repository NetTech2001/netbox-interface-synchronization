# netbox-interface-synchronization
## Overview
4.5.8 - MINOR UPDATE

Module Bays are now synchronizable. 

---------------------------------------

This plugin allows you to compare and synchronize component names and types between devices and device types in NetBox. 

It can be very useful for finding and correcting inconsistencies between components when changing the device type.

## Compatibility
Tested with Netbox 4.5.8  This plugin is not compatible with Netbox 2 or 3 but should work with any version of Netbox 4.3.1 or greater

## Installation
If your NetBox 4 installation uses virtualenv, activate it like this:
```
source /opt/netbox/venv/bin/activate
```
Install the plugin from PyPI:
```
pip install netbox-interface-synchronization
```
or clone this repository, then go to the folder with it and install the plugin:
```
pip install .
```
To enable to plugin, add the plugin's name to the `PLUGINS` list in `configuration.py` (it's usually located in `/opt/netbox/netbox/netbox/`) like so:
```
PLUGINS = [
    'netbox_interface_synchronization'
]
```
Don't forget to restart NetBox:
```
sudo systemctl restart netbox
```
## Usage
To sync the components, edit the device and set the new device type and save the device. Then find the "Sync Components" button at the bottom of the page:
![Device page](docs/images/1_device_page.png)
Mark the required actions with the checkboxes and click "Apply".
![Interface comparison](docs/images/2_interface_comparison.png)
### Plugin Settings
If you want to override the default values, configure the `PLUGINS_CONFIG` in your `configuration.py`:
```
PLUGINS_CONFIG = {
    'netbox_interface_synchronization': {
        'exclude_virtual_interfaces': True
    }
}
```
| Setting | Default value | Description |
| --- | --- | --- |
| exclude_virtual_interfaces | `True` | Exclude virtual interfaces (VLANs, LAGs) from comparison
