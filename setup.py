from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netbox-interface-synchronization',
    version='4.0.0',
    description='Syncing existing interfaces with the interfaces from a new device type in NetBox 4',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Keith Knowles',
    author_email='mkknowles@outlook.com',
    license='GPL-3.0',
    install_requires=['attrs>=21.1.0'],
    packages=["netbox4_interface_sync"],
    package_data={"netbox4_interface_sync": ["templates/netbox4_interface_sync/*.html"]},
    zip_safe=False
)
