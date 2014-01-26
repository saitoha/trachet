trachet
=======

What is This?
-------------

    trachet = tracer + ratchet(step-by-step debugging service)

    This Program runs as a terminal filter process, between Terminals and Applications.
    It provides step-by-step debugging and formatted sequence tracing service.
    You can look terminal I/O sequence on realtime, and it enables you to do step-by-step execution.

    http://saitoha.github.io/trachet/

.. image:: http://zuse.jp/misc/trachet1.png
   :width: 640

Install
-------

via github ::

    $ git clone --recursive https://github.com/saitoha/trachet.git
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
    -o OUTPUT, --output=OUTPUT  specify output device or file
    -b, --break                 "break" the program at the startup time
    -m, --monochrome            don't use color in output terminal"
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



QuickStart
----------

- STEP1

    First, You need to prepare two terminal windows,
    debugged terminal and output terminal.

    .. image:: http://zuse.jp/misc/trachet_qs1.png
       :width: 640

- STEP2

    At the output terminal, type "tty" command. ::

        $ tty 
        /dev/ttys002

    Now you get output terminal's TTY device name(=/dev/ttys002).

    .. image:: http://zuse.jp/misc/trachet_qs2.png

- STEP3

    At the debugged terminal, launch trachet.

    .. image:: http://zuse.jp/misc/trachet_qs3.png
       :width: 640

    Run default shell and send formatted I/O sequences to output terminal ::

        $ trachet -o/dev/ttys002

    Run default shell and write non-colored formatted I/O sequences to a text file. ::

        $ trachet -o log.txt

    Run vim and send formatted I/O sequences to output terminal. ::

        $ trachet -o/dev/ttys002 vim 

    Run emacs and send formatted I/O sequences to output terminal,
    and "break" emacs on startup time ::

        $ trachet -b -o/dev/ttys002 emacs -nw

    Replay output log created by script(1) step by step. ::

        $ trachet -b -o/dev/ttys002 cat ~/typescript -

How It Works
------------

- PTY and Normal Terminal/Application::

       +---------------------------------------------+
       |                  Terminal                   |
       +---------+-----------------------------------+
                 |
       +---------|-----------------------------------+
       |  +------+-------+        +---------------+  |
       |  |    Master    |========|     Slave     |  |
       |  +--------------+        +-------+-------+  |
       +----------------------------------|----------+
                                          |
       +----------------------------------+----------+
       |                Application                  |
       +---------------------------------------------+


- TFF (Terminal Filter Framework)::


                        Scanner                    Event Driven Parser         Event Dispatcher
                        +-----+                         +-----+                     +-----+
      << I/O Stream >>  |     | << CodePoint Stream >>  |     | << Event Stream >>  |     |      << I/O Stream >>
    ------------------->|     |------------------------>|     |-------------------->|     |---||-------------------->
      (Raw Sequences)   |     |    (Unicode Points)     |     |   (Function Call)   |     |       (Raw Sequences)
                        +-----+                         +-----+                     +--+--+
                                                   ISO-2022 ISO-6429                   |
                                                   Compatible Parsing                  |
                                                                                       v
                                                                                    +-----+
                                                                     Event Observer |     |      << I/O Stream >>
                                                                      (I/O Handler) |     |---||-------------------->
                                                                                    |     |       (Raw Sequences)
                                                                                    +-----+
- With Trachet... ::

     +----------------------------------------------------------+   +------------------------+
     |                                                          |   |                        |
     |                        Terminal                          |   |  Other Device or File  |
     |                                                          |   |                        |
     +----------------------------------------------------------+   +------------------------+
                          |                       ^                              ^
                          |                       |                              |
                      < input >               < output >                         |
                          |                       |                              |
                          |      +----------------+                              |
                          |      |                      [ PTY 1 ]                |
                   +------|------|-------------------------------+               |
                   |      v      |                               |               |
                   |  +----------+---+       +----------------+  |               |
                   |  |    Master    |=======|      Slave     |  |               |
                   |  +--------------+       +--+-------------+  |               |
                   |                            |        ^       |               |
                   +----------------------------|--------|-------+               |
                                                |        |                       |
                                            < input >    |                       |
                                                |        |                   < trace >
                                +---------------+    < output >                  |
                                |                        |                       |
        [ Trachet Process ]     |                        |                       |
     +--------------------------|------------------------|---------------+       |
     |                          |                        |               |       |
     |              +-----------|-------<< TFF >>--------|------------+  |       |
     |              |           v                        |            |  |       |
     |  < control > |  +-----------------+     +---------+---------+  |  |       |
     |       +----->|  |  InputHandler   |     |   OutputHandler   |  |  |       |
     |       |      |  +--+-----+----+---+     +--+----------------+  |  |       |
     |       |      |     |     |    |            |      ^            |  |       |
     |       |      +-----|-----|----|------------|------|------------+  |       |
     |       |            |     |    |            |      |               |       |
     |       |            |     |    |            |      |               |       |
     |       |            v     |    v            v      |               |       |
     |  +----+---------------+  |  +----------------+    |               |       |
     |  |  ActionController  |  |  |     Tracer     |----------------------------+
     |  +--------------------+  |  +----------------+    |               |
     |                          |                        |               |
     +--------------------------|------------------------|---------------+
                                |                        |
                            < input >                < output >
                                |                        |
                                |       +----------------+
                                |       |
                                |       | [ PTY 2 ]
                        +-------|-------|-----------------------------+
                        |       v       |                             |
                        |  +------------+--+       +---------------+  |
                        |  |    Master     |=======|     Slave     |  |
                        |  +---------------+       +----+----------+  |
                        |                               |      ^      |
                        +-------------------------------|------|------+
                                                        |      |
                                   +--------------------+      |
                                   |                           |
                               < input >                   < output >
                                   |                           |
                                   v                           |
     +---------------------------------------------------------+-----------------------------+
     |                                                                                       |
     |                                  Target Application                                   |
     |                                                                                       |
     +---------------------------------------------------------------------------------------+


Dependency
----------

 - TFF - Terminal Filter Framework
   https://github.com/saitoha/tff

Reference
---------

 - vt100.net
   http://vt100.net/
 
 - Private Control Functions used by DEC
   http://vt100.net/emu/ctrlfunc_dec.html

 - Xterm Control Sequences
   http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
 
 - TeraTerm / Supported Control Functions
   http://ttssh2.sourceforge.jp/manual/en/about/ctrlseq.html
 
 - MinTTY / Mintty-specific control sequences
   http://code.google.com/p/mintty/wiki/CtrlSeqs
 
 - RLogin / Supported control codes
   http://nanno.dip.jp/softlib/man/rlogin/ctrlcode.html
 

License
---------

 GNU GENERAL PUBLIC LICENSE Version 3

