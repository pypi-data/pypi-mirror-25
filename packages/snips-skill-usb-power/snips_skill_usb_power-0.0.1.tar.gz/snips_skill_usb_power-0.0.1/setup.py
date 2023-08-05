from setuptools import setup

setup(
    name='snips_skill_usb_power',
    version='0.0.1',
    description='turn on/off power to usb ports',
    author='steve ryan',
    author_email='stever@syntithenai.com',
    download_url='',
    license='MIT',
    install_requires=[],
    setup_requires=['green'],
    keywords=['snips'],
    include_package_data=True,
    packages=[
        'usbpowerskill'
    ]
)
