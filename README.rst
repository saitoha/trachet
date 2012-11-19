trachet
=======

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
    -b, --break                 "break" the program at the startup time
    --version                   show version


* Sequense Tracing

  If you specified TTY device by -o option,
  you can look I/O sequence tracing on realtime.


* Step by Step debugging

 - <F6> 
   Toggle trace state ON/OFF.

 - <F7>
   Toggle break state ON/OFF.

 - <F8>
   Step to next char or control sequence.

 - <F9>
   Step to next ESC or CSI sequence.


Example
-------

    $ trachet -o/dev/pts/4 bash
 
Dependency
----------

 - TFF - Terminal Filter Framework
   https://github.com/saitoha/tff

Reference
---------

 - vt100.net http://vt100.net/

