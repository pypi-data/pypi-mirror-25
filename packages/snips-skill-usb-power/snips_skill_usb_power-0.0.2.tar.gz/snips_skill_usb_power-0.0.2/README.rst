USB Power skill for Snips
======================================

|MIT License|

snips-skill-usbpower allows you to turn on and off power to individual USB ports on supported hubs.
the skill will look at the devices descriptions to allow matching by device name as well as port number

NOTE
The hub built into a raspberry pi only allows switching power for the whole hub which disables the usb microphone and crashes snips :(
A list of supported hubs -> https://github.com/mvp/uhubctl

Installation
------------

The fastest way to get going is to use the prebuilt assistant and Snipsfile at  https://github.com/syntithenai/snips_skill_maths


Usage
-----
Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

pip: snips-skill-usbpower
package_name: usbpowerskill
class_name: UsbPowerSkill
requires_tts: True
intents:
  - intent: UsbPowerOnPort
    action: |
      {%
      skill.usb_power_on_say(intent.usbPortIdentifier,skill.usb_load_devices(skill.usb_get_devices()))
      %}
  - intent: UsbPowerOffPort
    action: |
      {%
      skill.usb_power_off_say(intent.usbPortIdentifier,skill.usb_load_devices(skill.usb_get_devices()))
      %}
  - intent: UsbListPorts
    action: |
      {%
      skill.usb_list_devices_say(skill.usb_load_devices(skill.usb_get_devices()))
      %}

Contributing
------------

Please see the `Contribution Guidelines`_.

.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
:target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt
:alt: MIT License

.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt
.. _`Contribution Guidelines`: https://github.com/snipsco/snips-skill-hue/blob/master/CONTRIBUTING.rst
.. _snipsskills: https://github.com/snipsco/snipsskills
