sixelterm
=========

Install
-------

via github ::

    $ git clone https://github.com/saitoha/trachet.git
    $ cd trachet
    $ python setup.py install

or via pip ::

    $ pip install trachet


Usage
-----

::

    $ trachet [options] command

* Options::

    -h, --help                  show this help message and exit
    -o OUTPUT, --output=OUTPUT  Specify output device or file
    --version                   show version

* Sequense Tracing

  If you specified TTY device to -o option,
  you can look I/O sequence tracing on realtime.

* Step by Step debugging

 - <F5> 
   Stop step-by-step debugging.

 - <F6>
   Start step-by-step debugging.

 - <F7>
   Step.

 - <F8>
   Step to next escape sequence (not control char).

Example
-------

    $ trachet -o/dev/pts/4 bash
    

Reference
---------

 - vt100.net http://vt100.net/

