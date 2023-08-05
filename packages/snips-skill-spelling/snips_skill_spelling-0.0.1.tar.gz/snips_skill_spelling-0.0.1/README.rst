Spelling skill for Snips
======================================

|MIT License|

snips-skill-spelling will spell the requested word

Installation
------------

Usage
-----
Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

pip: snips-skill-spelling
package_name: spellingskill
class_name: SpellingSkill
requires_tts: True
intents:
  - intent: SpellWord
    action: |
      {%
      skill.spell_and_say(intent.wordToSpell)
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
