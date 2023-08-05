Prude
=====

`prude` is a generic code annalyser to check ```language``` error. The ```language``` check is the english.


.. image:: https://badge.fury.io/py/prude.png
    :target: https://pypi.python.org/pypi/prude

Release (master)
----------------

.. image:: https://travis-ci.org/HeeroYui/prude.svg?branch=master
    :target: https://travis-ci.org/HeeroYui/prude


Developement (dev)
------------------

.. image:: https://travis-ci.org/HeeroYui/prude.svg?branch=dev
    :target: https://travis-ci.org/HeeroYui/prude

Instructions
------------

This is a tool to annalyse C, C++ file and determine if it have some english word that does not exist.


Prude is under a FREE license that can be found in the COPYING file.
Any contribution is more than welcome ;)

git repository
--------------

http://github.com/HeeroYui/prude/

Installation
------------

Requirements: ``Python >= 2.7`` and ``pip``

Just run:

  pip install prude

Install pip on debian/ubuntu:

  sudo apt-get install pip

Install pip on ARCH-linux:

  sudo pacman -S pip

Install pip on MacOs:

  sudo easy_install pip

developpement for prude:

  git clone http://github.com/HeeroYui/prude/
  cd prude
  ./setup.py develop --user

Documentation
-------------

Usage
******

Go to your coding directory and execute:

  prude yourFileToParce.cpp
  # OR (multiple files)
  prude yourFileToParce.cpp other_file.py and.txt
  # simply the path
  prude .

You can use some options:

  --color/-C to have beautifull color check
  --recursive/-r Parse all under directories

Create exceptions:
******************

prude parse all upper folder to find all file ".prude_*" and add it in the list of exceptions error.

The search end when find the file ".prude".

you can have:

  root_path
    --> .prude
    --> .prude_lua
    --> .prude_tinyxml
    --> module
          --> submodule
                --> .prude_local
                --> .prude_local2
                --> my_file_cpp.cpp
          --> sub_second
                --> file_c.c

The check of the file ```my_file_cpp.cpp``` use all the .prude* file and the file ```file_c.c``` only use the file on the root_path

A prude file is contituated like:

  * ```#``` Comment the line
  * ```+``` Use the end of the line to check the exact match of the string (ex: +MY_VariableStupidName)
  * direct element is use to comare each word in lower case to exclude error on it (ex: destructor)
  * ```!``` Command to apply at the configuration.
    - ```!NO_CAPITAL_LETTER``` ==> disable the check of the word in capital letter
    - ```!CAPITAL_LETTER``` ==> enable the check of the word in capital letter (default)

Some tricky things (removed because it is errored at the declaration and no more need in library using it):

  * The namespace call are disable (ex namespace::prout)
  * The parameter access are disable (ex: variable.hello() or variable->hello())
  * The "#include ..." and the "# include ..."

Now you can play.

Note: in the http://github.com/HeeroYui/prude/common/ you have some common C library that declare stupid thing in global...

License (APACHE v2.0)
---------------------

Copyright prude Edouard DUPIN

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

