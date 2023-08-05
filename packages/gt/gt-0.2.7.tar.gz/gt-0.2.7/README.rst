Goals
=====

To provide a simple tool for quickly creating private git repos 'in the
cloud' wherever that may be.

Installation
============

Requires python 3.

``pip3 install gt`` should do the trick, or else
``python setup.py install`` from source.

Usage
=====

Create **~/.gtrc** and populate it with sections of the following form

::

    [<source name>]
    type=<git source>
    <param1>=<val1>
    <param2>=<val2>

where ``<git source>`` indicates the source type.

Supported sources at the time of writing include: - gitlab (the service)
- ssh (An ssh-able Unix box containing a directory full of repos)

Examples
========

~/.gtrc
-------

::

    [ s1 ]
    type=ssh
    host=dionysus
    user=rvaiya
    project_dir=/storage/projects

    [ gl ]
    type=gitlab
    api_token=a734d981ddda8

CLI Usage
---------

::

    # gt -l

    s1/project1
    s1/project2
    gl/projecta
    gl/projectb

    # gt -c s1/project3

    Successfully created s1/project3
    git remote add origin ssh://rvaiya@dionysus:/storage/projects/project3

    # gt -d gl/projecta

    Successfully deleted gl/projecta
    
    # gt --clone gl/projecta
    
    Cloning into 'projecta'...
    remote: Counting objects: 20, done.
    remote: Compressing objects: 100% (17/17), done.
    remote: Total 20 (delta 2), reused 0 (delta 0)
    Receiving objects: 100% (20/20), 22.00 KiB | 0 bytes/s, done.
    Resolving deltas: 100% (2/2), done.
    Checking connectivity... done.


Bugs/Limitations
================

The tool is designed to handle as many git sources as possible and so
only supports primitive operations (i.e add/remove/delete). Since it is
primarily intended for personal use it does not support sophisticated
project or permission management features which are commonly found on
proprietary collaboration platforms like github.

There will be bugs.

Extensibility
=============

Adding a source should be as simple as creating a python file in
gt/sources and defining a class with the following methods:

-  list()
-  delete(name)
-  create(name)

The class name serves as the source type and its constructor's parameter
names are drawn from the relevant section of the config file when
instantiating the object.

It is worth noting that the project began life as a bash script and was
partly rewritten as an exercise in python by the author. As such things
may not be optimally 'pythonic' :). If you bother to read the code and
invariably feel the need to abuse the person who wrote it, know that
such sentiments will be happily received at r.vaiya@gmail.com.
