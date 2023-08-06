HDMI Monitor control skill for Snips
======================================

|MIT License|

snips-skill-monitorcontrol

Installation
------------

The fastest way to get going is to use the prebuilt assistant and Snipsfile at  https://github.com/syntithenai/snips_skill_maths

Usage
-----
Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

package_name: monitorcontrolskill
class_name: MonitorControlSkill
requires_tts: True
intents:
  - intent: MonitorSelectBrightness
    action: |
      {%
      skill.monitor_aselect_brightness(intent.monitorBrightness)
      %}
  - intent: MonitorSelectVolume
    action: |
      {%
      skill.monitor_bselect_volume(intent.monitorVolume)
      %}
  - intent: MonitorOn
    action: |
      {%
      skill.monitor_power_on()
      %}
  - intent: MonitorOff
    action: |
      {%
      skill.monitor_power_off()
      %}
  - intent: MonitorSelectInput
    action: |
      {%
      skill.monitor_select_input(intent.monitorInputNumber)
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
