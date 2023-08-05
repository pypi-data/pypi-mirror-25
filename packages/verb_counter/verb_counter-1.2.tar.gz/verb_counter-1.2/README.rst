Verbs in func names counter
===========================

| This script calculate verbs count in func names in ``.py`` files.
| Script check all folders recursively. Default folder names for
  search:\
| *django, flask, pyramid, reddit, requests, sqlalchemy.*\
| You can add your folders to check list.

How to install
==============

| Run ``pip3 install verb-counter``
| Run on CLI for update nltk if it need:\

::

    $ python3
    >> import nltk
    >> nltk.download('all')

How to use
==========

| If you want check default folders:\
| ``$ verbs``
| If you want add your project folders, print it space-separated:
| ``$ verbs -p myproject1 myproject2``
| If you want check all funcs names:
| ``verbs -a``

Usage example:
==============

We have some folders structure with ``dclint.py``:

::

    ├── dclint.py
    ├── django
    │   ├── css
    │   ├── bootstrap.min.css
    │   ├── my_app.py
    │
    ├── flask
    │   ├── favicon.ico
    │   ├── polls.py
    │   ├── garbage_files
    │   │   ├──bootstrap.min.js
    │   │   ├──html5shiv.min.js
    │   │   ├──thrash.py
    │
    ├── myproject
    │   ├──ie-emulation-modes-warning.js
    │   ├──old_version.py
    │   ├──new_file.py

| In all folders - 5 ``.py`` files.\
| All files have funcs like this (for example):

::

    def get_all_names(names):
        for name in names:
            print('name: {name}'.format(name=name))

::

    def give_money(user, money):
        print('{user} now have {money} $'.format(user=user,
         money=money))

::

    def check_exist(folder):
        if os.path.exist(folder):
            return True

And another funcs.

| Folders ``flask`` and ``django`` already in check list, but we need
  add ``myproject``.\
| Run check:\
| ``$ verbs -p myproject``\
| Result:

::

    dirpath: ./myproject:
    total ".py" files count: 1
    verb "get" count: 1
    ------------
    dirpath: ./django:
    total ".py" files count: 3
    verb "get" count: 3
    verb "give" count: 2
    ------------
    dirpath: ./flask:
    total ".py" files count: 1
    verb "get" count: 1
    ------------
    total verbs: 4
    unique verbs: 2
    "get" in 3 projects
    "give" in 1 projects

License
=======

MIT license