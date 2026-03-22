from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netbox-interface-synchronization',
    version='4.5.1',
    description='Syncing existing components with the components from a device type template in NetBox 4.3+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Keith Knowles',
    author_email='NetTech2001#github.com',
    license='GPL-3.0',
    packages=["netbox_interface_synchronization"],
    package_data={"netbox_interface_synchronization": ["templates/netbox_interface_synchronization/*.html"]},
    zip_safe=False
)
