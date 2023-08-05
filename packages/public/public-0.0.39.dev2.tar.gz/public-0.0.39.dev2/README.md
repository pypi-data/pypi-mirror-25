<!--
README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)
-->
<p align="center">
    <b>@public decorator, public(*objects) function - add objects names to __all__</b>
</p>

[![python](https://img.shields.io/badge/Language-Python-blue.svg?style=plastic)]()
[![PyPI](https://img.shields.io/pypi/pyversions/public.svg)](https://pypi.org/pypi/public)
[![PyPI](https://img.shields.io/pypi/v/public.svg)](https://pypi.org/pypi/public)
<!-- line break -->
[![](https://codeclimate.com/github/russianidiot/public.py/badges/gpa.svg)](https://codeclimate.com/github/russianidiot/public.py)
[![](https://landscape.io/github/russianidiot/public.py/master/landscape.svg?style=flat)](https://landscape.io/github/russianidiot/public.py)
[![](https://scrutinizer-ci.com/g/russianidiot/public.py/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/russianidiot/public.py/)
[![](https://api.codacy.com/project/badge/Grade/6692c8b8d1194b3db696b456b683ad94)](https://www.codacy.com/app/russianidiot/public-py)
<!-- line break -->
[![](https://api.shippable.com/projects/57068cbb2a8192902e1bbbd6/badge?branch=master)](https://app.shippable.com/projects/57068cbb2a8192902e1bbbd6)
[![](https://app.wercker.com/status/f9a3b6fa3f83012adafea514154b8b37/s/master)](https://app.wercker.com/russianidiot/public.py)
[![](https://scrutinizer-ci.com/g/russianidiot/public.py/badges/build.png?b=master)](https://scrutinizer-ci.com/g/russianidiot/public.py/)
[![](https://semaphoreci.com/api/v1/russianidiot/public-py/branches/master/badge.svg)](https://semaphoreci.com/russianidiot/public-py)
[![](https://api.travis-ci.org/russianidiot/public.py.svg?branch=master)](https://travis-ci.org/russianidiot/public.py/)


### Install

`[sudo] pip install public`

### Usage

```python
>>> from public import public

>>> @public # decorator

>>> public(*objects) # function
```

### Examples

```python
>>> @public
	def func(): pass

>>> @public
	class CLS: pass

>>> print(__all__)
['CLS',func']

# public(*objects) function
>>> public("name")
>>> public("name1","name2")

>>> print(__all__)
['name','name1','name2']
```
