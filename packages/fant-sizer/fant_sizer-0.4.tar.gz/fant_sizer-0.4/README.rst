.. image:: https://travis-ci.org/ripiuk/fant_sizer.svg?branch=master
    :target: https://travis-ci.org/ripiuk/fant_sizer

============
Usage:
============

- After installation, you can run this package directly in command line. Launching it without arguments starts it in interactive mode:

================
Sample output:
================
::

    Path: /home/sany/PycharmProjects
    Number of files: 6657
    № |     B     |  MB   | Path
    1 | 368078630 | 368.1 | /home/sany/PycharmProjects/xml_to_csv/Harrods_Google_Feed_USD_US.xml
    2 | 195476333 | 195.5 | /home/sany/PycharmProjects/xml_to_csv/test.csv
    3 | 188825866 | 188.8 | /home/sany/PycharmProjects/just/test.csv
    4 |  40412990 |  40.4 | /home/sany/PycharmProjects/BuildingMachine/_sparsetools.cpython-36m-x86_64-linux-gnu.so
    5 |  38513408 |  38.5 | /home/sany/PycharmProjects/BuildingMachine/.libs/libopenblasp-r0-39a31c03.2.18.so

- Besides that, you can start it with arguments:

    -h, --help  show this help message and exit
    -p PATH     the path to parent dir
    -n NUMBER   how much files will be shown
    -m, --min   sort by min size

=============
Sample output
=============
::

    $ fant_sizer -p /home/sany/PycharmProjects/some_dir -n 40 -m

    Path: /home/sany/PycharmProjects/some_dir
    Number of files: 45
     № |  B   | MB  | Path
     1 |    0 | 0.0 | /home/sany/PycharmProjects/some_dir/setup.cfg
     2 |    6 | 0.0 | /home/sany/PycharmProjects/some_dir/.gitignore
     3 |   10 | 0.0 | /home/sany/PycharmProjects/some_dir/runtime.txt
     4 |   23 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/HEAD
     5 |   24 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/COMMIT_EDITMSG
     6 |   41 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/refs/heads/master
     7 |   73 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/description
     8 |   92 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/config
     9 |  180 | 0.0 | /home/sany/PycharmProjects/some_dir/.idea/vcs.xml
    10 |  189 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/hooks/post-update.sample
    11 |  208 | 0.0 | /home/sany/PycharmProjects/some_dir/.idea/misc.xml
    12 |  240 | 0.0 | /home/sany/PycharmProjects/some_dir/.git/info/exclude
    13 |  280 | 0.0 | /home/sany/PycharmProjects/some_dir/.idea/modules.xml

============
Download
============
::

  python3.6 -m pip install fant_sizer

