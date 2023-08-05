ced
===

A lightweight, cross-platform, no-dependency configuration editor.

Install
=======

::

    pip install ced

For convenience, you may also directly download the `ced` script::

    curl https://raw.githubusercontent.com/regisb/ced/master/ced/ced > ced
    chmod u+x ced

This is useful if you don't want to install pip in your environment.

Usage
=====

::

  $ ced -h
  usage: ced [-h] [-o OUTPUT] [-d DELIMITER] [-s] [-V VALUE] src

  A lightweight, cross-platform, no-dependency configuration editor.

  positional arguments:
    src                   path to source file

  optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                          path to destination file; if unset, print to stdout
    -d DELIMITER, --delimiter DELIMITER
                          placeholder delimiter
    -s, --safe            do not raise error on missing placeholder values
    -V VALUE, --value VALUE
                          explicitely set a value: formated as 'var=value'
