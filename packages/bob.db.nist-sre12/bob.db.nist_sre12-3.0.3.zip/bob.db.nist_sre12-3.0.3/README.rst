.. vim: set fileencoding=utf-8 :
.. Wed Aug 24 16:40:00 CEST 2016

.. image:: http://img.shields.io/badge/docs-v3.0.3-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.nist_sre12/v3.0.3/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.nist_sre12/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/badges/v3.0.3/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/commits/v3.0.3
.. image:: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/badges/v3.0.3/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/commits/v3.0.3
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nist_sre12
.. image:: http://img.shields.io/pypi/v/bob.db.nist_sre12.svg
   :target: https://pypi.python.org/pypi/bob.db.nist_sre12


=============================================================================
 Speaker Recognition Protocol on the NIST SRE 2012 Database Interface for Bob
=============================================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. This package contains an interface for the evaluation protocol of the `2012 NIST Speaker Recognition Evaluation <http://www.nist.gov/itl/iad/mig/sre12.cfm>`_. This package does not contain the original `NIST SRE databases <http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03>`_, which need to be obtained through the link above.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.db.nist_sre12

You can either download the SQLite DB file

1. To download a copy of an already populated SQLite DB

  ./bin/bob_dbmanage.py nist_sre12 download


2. To generate and populate the NIST SRE 2012 database do the following:

  - Change to sre12 file list directory:

      cd bob/db/nist_sre12/sre12

  - Create file lists and key files for NIST SRE 2012 protocols and conditions

      ./generate-file-lists.py

  - You can check that file lists point to actual files by running

      ./check-all-files-exist.py

    after assigning variable 'prefix' your SRE12 base path

      prefix='DATABASE_DIRECTORY_PREFIX'

  - Populate SQL database

    ./bin/bob_dbmanage.py nist_sre12 create -vv -R


3. To double check the files in the SQLite database point to actual files

  ./bin/bob_dbmanage.py nist_sre12 checkfiles -e .sph -d DATABASE_DIRECTORY_PREFIX


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
