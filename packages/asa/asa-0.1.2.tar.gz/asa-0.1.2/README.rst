ASA Python
===================

|pyversion| |version| |license|

Japanese Argument Structure Analyzer (ASA) client for Python.

For details about ASA, See http://www.cl.cs.okayama-u.ac.jp/study/project/asa/ (Written in Japanese)

Contributions are welcome!


Installation
==============

::

 pip install asa

Example
===========

.. code:: python

 from asa import ASA

 # Initialize a ASA instance
 asa = ASA(path-to-asa, encoding='utf8')

 # Let's analyze a sample sentence
 asa.parse('彼は村長だ')
 # =>
 [{'category': '人',
   'frame': '1-copula',
   'link': 1,
   'main': '彼',
   'part': 'は',
   'tense': 'PRESENT',
   'type': 'elem',
   'wakati': ['彼\tカレ\t彼\t名詞,代名詞,一般\t\t\tO', 'は\tハ\tは\t助詞,係助詞\t\t\tO']},
  {'category': '人',
   'frame': '0-elem',
   'link': -1,
   'main': '村長',
   'mood': 'INDICATIVE',
   'part': 'だ',
   'polarity': 'AFFIRMATIVE',
   'sentelem': 'PREDICATE',
   'tense': 'PRESENT',
   'type': 'copula',
   'voice': 'ACTIVE',
   'wakati': ['村長\tソンチョウ\t村長\t名詞,一般\t\t\tO', 'だ\tダ\tだ\t助動詞\t特殊・ダ\t基本形\tO']}]


LICENSE
=========

MIT License


Copyright
=============

ASA Python
(c) 2017- Yukino Ikegami. All Rights Reserved.

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/asa.svg

.. |version| image:: https://img.shields.io/pypi/v/asa.svg
    :target: http://pypi.python.org/pypi/asa/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/asa.svg
    :target: http://pypi.python.org/pypi/asa/
    :alt: license
