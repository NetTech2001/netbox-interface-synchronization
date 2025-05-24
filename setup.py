from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netbox-interface-synchronization',
    version='4.1.7',
    description='Syncing existing interfaces with the interfaces from a device type template in NetBox 4+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Keith Knowles',
    author_email='mkknowles@outlook.com',
    license='GPL-3.0',
    packages=["netbox_interface_synchronization"],
    package_data={"netbox_interface_synchronization": ["templates/netbox_interface_synchronization/*.html"]},
    zip_safe=False
)
