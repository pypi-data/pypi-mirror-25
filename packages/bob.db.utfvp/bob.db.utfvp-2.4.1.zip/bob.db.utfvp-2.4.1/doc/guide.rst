.. vim: set fileencoding=utf-8 :
.. Thu 18 Aug 2016 18:03:09 CEST

==============
 User's Guide
==============

This package contains the access API and descriptions for the `UTFVP Fingervein
database`_. It only contains the Bob_ accessor methods to use the DB directly
from python, with our certified protocols. The actual raw data for the `UTFVP
Fingervein database`_ should be downloaded from the original URL.


The Database Interface
----------------------

The :py:class:`bob.db.utfvp.Database` complies with the standard Bob database
itnerface.

.. todo::
   Explain the particularities of the :py:class:`bob.db.utfvp.Database`.


.. _bob: https://www.idiap.ch/software/bob
.. _utfvp fingervein database: http://www.sas.el.utwente.nl/home/datasets
