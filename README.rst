trachet
=======

What is This?
-------------

    trachet = tracer(sniffer service) + ratchet(step-by-step debugging service)

    This Program runs as a terminal filter process, between Terminals and Applications.
    It provides step-by-step debugging and formatted sequence tracing service.
    You can look terminal I/O sequence on realtime, and it enables you to do step-by-step execution.

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

- Run default shell and send formatted I/O sequence to a terminal device(/dev/pts/4)::

    $ trachet -o/dev/pts/4


- Run vim and send formatted I/O sequence to a terminal device(/dev/pts/4)::

    $ trachet -o/dev/pts/4 vim 


- Run emacs and send formatted I/O sequence to a terminal device(/dev/pts/4), and "break" emacs on startup time::

    $ trachet -b -o/dev/pts/4 "emacs -nw" 



Tutorial
--------

    Comming soon...


How It Works
------------

- PTY and Terminal/Application::

       +-------------------------------------------+                           
       |                 Terminal                  |                           
       +--------+----------------------------------+                           
                |                                   
       +--------|----------------------------------+
       | +------+-------+        +---------------+ |
       | |    Master    +--------+     Slave     | |
       | +--------------+        +-------+-------+ |
       +---------------------------------|---------+
                                         |          
       +---------------------------------+---------+ 
       |               Application                 |
       +-------------------------------------------+



- With Trachet... ::

     +----------------------------------------------------------+   +------------------------+
     |                                                          |   |                        |
     |                Debug Targetted Terminal                  |   |  Other Device or File  |
     |                                                          |   |                        |
     +----------------------------------------------------------+   +------------------------+
                          |     ^                                                ^
                          |     |   [ PTY 1 ]                                    |
                    +-----|-----|-------------------------------+                |
                    |     v     |                               |                |
                    | +---------+----+       +----------------+ |                |
                    | |    Master    |-------|      Slave     | |                |
                    | +--------------+       +--+-------------+ |                |
                    |                           |       ^       |                |
                    +---------------------------|-------|-------+                |
                                            < input >   |                        |
                               + ---------------+       |                    < trace >
                               |                    < output >                   |
                               | [ Trachet Process ]    |                        |
     +-------------------------|------------------------|---------------+        |
     |                         |         TFF            |               |        |
     |             +-----------|------------------------|------------+  |        |
     | < control > |  +--------+--------+    +----------+---------+  |  |        |
     |      +----->|  | InputHandler    |    |    OutputHandler   |  |  |        |
     |      |      |  +--+-----+----+---+    +---+------+---------+  |  |        |
     |      |      +-----|-----|----|------------|------|------------+  |        |
     |      |            |     |    |            |      |               |        |
     |      |            v     |    |            |      |               |        |
     | +----+---------------+  |  +-+------------+-+    |               |        |
     | |  ActionController  |  |  |     Tracer     |-----------------------------+
     | +--------------------+  |  +----------------+    |               |
     +-------------------------|------------------------|---------------+
                               |                        |
                               |   +--------------------+
                               |   |                           
                               |   | [ PTY 2 ]                 
                    +----------v---|----------------------------+
                    |              |                            |
                    | +------------+-+        +---------------+ |
                    | |    Master    +--------+     Slave     | |
                    | +--------------+        +----+----------+ |
                    |                              |      ^     |
                    +------------------------------|------|-----+
                                                   v      |
     +----------------------------------------------------+-------------+
     |                                                                  |
     |                         Target Application                       |
     |                                                                  |
     +------------------------------------------------------------------+
 
Dependency
----------

 - TFF - Terminal Filter Framework
   https://github.com/saitoha/tff

Reference
---------

 - vt100.net http://vt100.net/

