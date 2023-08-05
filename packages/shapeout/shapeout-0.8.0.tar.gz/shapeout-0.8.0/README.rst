|ShapeOut|
==========

|PyPI Version| |Build Status Win| |Coverage Status|


ShapeOut is a graphical user interface for the analysis
and visualization of RT-DC data sets. For more informaion please visit
http://zellmechanik.com/.


Manual and User Guide
---------------------
The manual and user guide can be found at http://www.zellmechanik.com/download.


Installation
------------
Installers for ShapeOut are available at the `release page <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/releases>`__.


Citing ShapeOut
---------------
Please cite ShapeOut either in-line

::

  (...) using the analysis software ShapeOut version X.X.X (available at
  https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut).

or in a bibliography

::
  
  Paul Müller and others (2015), ShapeOut version X.X.X: Analysis software
  for real-time deformability cytometry [Software]. Available at
  https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut.

and replace ``X.X.X`` with the version of ShapeOut that you used.


Information for developers
--------------------------

Running from source
~~~~~~~~~~~~~~~~~~~
The easiest way to run ShapeOut from source is to use
`Anaconda <http://continuum.io/downloads>`__. 

- **Windows**: Sketchy installation instructions are 
  `here <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/tree/master/freeze_appveyor>`__ and 
  `here <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/blob/master/appveyor.yml>`__.

- **Debian**: Run `this script <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/blob/master/develop/activate_linux.sh>`__
  which will create a Python virtual environment.

- **MacOS**: ShapeOut should work with Anaconda (see Windows above).
  It is also possible to install all dependencies with MacPorts:

  ::
  
    sudo port install python27 py27-ipython py27-scipy py27-matplotlib
    sudo port install opencv +python27
    sudo port install py27-wxpython-3.0 py27-statsmodels py27-kiwisolver py27-chaco py27-pip py27-simplejson py27-sip py27-macholib
    sudo pip-2.7 install nptdms
    sudo pip-2.7 install pyper


  Then select python27 (macports) as standard python interpreter:

  ::
  
    sudo port select --set python python27
    sudo port select --set pip pip27

  Check-out `dclab <https://github.com/ZELLMECHANIK-DRESDEN/dclab>`__ and
  append the following command to ``~/.bash_profile``
  
  ::
  
    #!/bin/bash
    export PYTHONPATH="${PYTHONPATH}:/path/to/dclab"

  start ShapeOut with

  ::
  
    python shapeout/ShapeOut.py

  This can be put into a .command file placed on the Desktop.



Contributing
~~~~~~~~~~~~
The main branch for developing ShapeOut is ``develop``. Small changes that do not
break anything can be submitted to this branch.
If you want to do big changes, please (fork ShapeOut and) create a separate branch,
e.g. ``my_new_feature_dev``, and create a pull-request to ``develop`` once you are done making
your changes.
Please make sure to edit the 
`Changelog <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/blob/master/CHANGELOG>`__. 

**Very important:** Please always try to use 

::

	git pull --rebase

instead of

::

	git pull
	
to prevent confusions in the commit history.

Tests
~~~~~
ShapeOut is tested using pytest. If you have the time, please write test
methods for your code and put them in the ``tests`` directory. You may
run the tests manually by issuing:

::

    python setup.py test
	

Test binaries
~~~~~~~~~~~~~
After each commit to the ShapeOut repository, a binary installer is created
by `Appveyor <https://ci.appveyor.com/project/paulmueller/ShapeOut>`__. Click
on a build and navigate to ``ARTIFACTS`` (upper right corner right under
the running time of the build). From there you can download the executable
Windows installer.


Creating releases
~~~~~~~~~~~~~~~~~
Please **do not** create releases when you want to test if something you
did works in the final Windows binary. Use the method described above to
do so. Releases should be created when improvements were made,
bugs were resolved, or new features were introduced.

Procedure
_________
1. Make sure that the `changelog (develop) <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/blob/develop/CHANGELOG>`__
   is updated and that the `version (develop) <https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/blob/develop/shapeout/_version.py>`__
   is incremented.

2. Create a pull request from develop into master using the web interface or simply run

   ::

       git checkout master  
       git pull origin develop  
       git push  
	
3. Create the release at https://github.com/ZELLMECHANIK-DRESDEN/ShapeOut/releases.  
   Make sure that the tag of the release follows the version format of ShapeOut
   (e.g. `0.5.3`) and also name the release correctly (e.g. `ShapeOut 0.5.3`).
   Also, copy and paste the change log of the new version into the comments of the release.
   The first line of the release comments should contain the download counts shield like so:
   
   ::
   
       ![](https://img.shields.io/github/downloads/ZELLMECHANIK-DRESDEN/ShapeOut/0.5.3/total.svg)
   
   The rest should contain the change log.  
   Make sure to check `This is a pre-release` box.
   
4. Once the release is created, `Appveyor <https://ci.appveyor.com/project/paulmueller/ShapeOut>`__
   will perform the build process and upload the installation files directly to the release. 
   If the binary works, edit the release and uncheck the `This is a pre-release` box.

5. Make sure that all the changes you might have performed on the `master` branch are brought back
   to ``develop``.
   
   ::

       git checkout develop  
       git pull origin master  
       git pull --tags origin master
       git push     


.. |ShapeOut| image:: https://raw.github.com/ZELLMECHANIK-DRESDEN/ShapeOut/master/shapeout/img/shapeout_logotype_h50.png
.. |PyPI Version| image:: http://img.shields.io/pypi/v/ShapeOut.svg
   :target: https://pypi.python.org/pypi/dclab
.. |Build Status Win| image:: https://img.shields.io/appveyor/ci/paulmueller/ShapeOut/master.svg?label=build_win
   :target: https://ci.appveyor.com/project/paulmueller/ShapeOut
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/ZELLMECHANIK-DRESDEN/ShapeOut/master.svg
   :target: https://codecov.io/gh/ZELLMECHANIK-DRESDEN/ShapeOut