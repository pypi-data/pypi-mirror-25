.. vim: set fileencoding=utf-8 :
.. @author: Marc Ferras <marc.ferras@idiap.ch>
.. @date:   Tue Nov 15 12:28:25 CET 2016


==============
 User's Guide
==============

This package contains the access API and descriptions for the `2012 NIST Speaker Recognition Evaluation`_, which is part of an ongoing series of corpora designed for speaker verification.

This package implements access to the speaker recognition core condition protocols for the NIST SRE 2012 (SRE12). Please note that SRE12 includes data from previous evaluation campaigns such as SRE06, SRE08 and SRE10. This package only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols. You will need to order the actual audio data for SRE06, SRE08, SRE10 and SRE12 from the Linguistic Data Consortium: http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03. Please follow the instructions and the `evaluation plan`_ given by NIST. You will also need the sph2pipe_ tool to be installed on your system and be accessible in your path.

If you use this package and/or its results, please cite the following publication for Bob_:

  .. code-block:: latex

    @inproceedings{Anjos_ACMMM_2012,
      author = {Anjos, Andr\'e and El Shafey, Laurent and Wallace, Roy and G\"unther, Manuel and McCool, Christopher and Marcel, S\'ebastien},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = {oct},
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }


Protocols and groups
~~~~~~~~~~~~~~~~~~~~

The following SRE12 evaluation protocols are supported:

  'core-all', 'core-c1', 'core-c2', 'core-c3', 'core-c4', 'core-c5'

They refer to the core condition of the evaluation along with its 5 subconditions. The file lists for these protocols can be found under ``bob/db/nist_sre12/sre12/protocols`` after having run ``bob/db/nist_sre12/sre12/generate-file-lists.py`` .


The Database Interface
----------------------

The :py:class:`bob.db.nist_sre12.Database` complies with the standard biometric verification database, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`. This package implements the low-level DB interface while a high-level interface for SRE12 is implemented in spear_.

Implementation details
----------------------

   The DB interface implements File, Model, Protocol, ProtocolPurpose, ModelEnrollLink and ModelProbeLink tables, extending the existing SQLiteDatabase implementations in other Bob packages. This is required to cope with the specificities of the NIST SRE.


   - Physical and logical file names:
      Speech databases use multi-channel, typically stereo, files to encode multiple synchronized conversation sides into a single file. A single audio file in SPHERE format is read per conversation, while multiple logical sides are generated for further processing the data for each speaker separately, thus assuming one spekaer per conversation side.

   - Missing client identifiers:
      The NIST SREs do not provide speaker identifiers, i.e. client IDs, for all the speech file sides in the database, typically for probe sides. For evaluation, the protocol specifies what specific (model,file_side) pairs are to be scored. We opted for including two additional tables in the interface, ModelEnrollLink and ModelProbeLink, to store what file sides should be used for enrolling each model and what file sides should be tested against each model. Note that these tables, especially ModelProbeLink, can be populated with millions of rows, slowing down the creation and query of the database. Each file record in the File database corresponds to a file side that has a client_id field associated to it. Both model IDs and client IDs are allowed unknown IDs, M_ID_X and C_ID_X, respectively.

.. _idiap: http://www.idiap.ch
.. _bob: https://www.idiap.ch/software/bob
.. _spear: https://gitlab.idiap.ch/bob/bob.bio.spear
.. _sph2pipe: https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools
.. _2012 NIST Speaker Recognition Evaluation: http://www.nist.gov/itl/iad/mig/sre12.cfm
.. _evaluation plan: https://www.nist.gov/sites/default/files/documents/itl/iad/mig/NIST_SRE12_evalplan-v17-r1.pdf


