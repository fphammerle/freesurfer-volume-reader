freesurfer-volume-reader
========================

.. image:: https://travis-ci.org/fphammerle/freesurfer-volume-reader.svg?branch=master
   :target: https://travis-ci.org/fphammerle/freesurfer-volume-reader
.. image:: https://coveralls.io/repos/github/fphammerle/freesurfer-volume-reader/badge.svg?branch=master
   :target: https://coveralls.io/github/fphammerle/freesurfer-volume-reader?branch=master
.. image:: https://img.shields.io/pypi/v/freesurfer-volume-reader.svg
   :target: https://pypi.org/project/freesurfer-volume-reader/#history
.. image:: https://img.shields.io/pypi/pyversions/freesurfer-volume-reader.svg
   :target: https://pypi.org/project/freesurfer-volume-reader/
.. image:: https://zenodo.org/badge/183625692.svg
   :target: https://zenodo.org/badge/latestdoi/183625692

Python script & library to read hippocampal subfield volumes computed by
Freesurfer & ASHS

-  Freesurfer
   https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
-  ASHS https://sites.google.com/site/hipposubfields/home

Install
-------

.. code:: sh

   pip3 install --user freesurfer-volume-reader
   freesurfer-volume-reader --help

Releases follow the `semantic versioning <https://semver.org/>`__
scheme.

Usage
-----

Freesurfer
~~~~~~~~~~

.. code:: sh

   export SUBJECTS_DIR=/my/freesurfer/subjects
   freesurfer-volume-reader

or

.. code:: sh

   freesurfer-volume-reader /my/freesurfer/subjects
   freesurfer-volume-reader /my/freesurfer/subjects /other/freesurfer/subjects

or

.. code:: python

   from freesurfer_volume_reader import freesurfer

   for volume_file in freesurfer.HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects'):
       print(volume_file.subject, volume_file.hemisphere, volume_file.analysis_id)
       print(volume_file.read_volumes_mm3())
       print(volume_file.read_volumes_dataframe())

ASHS
~~~~

.. code:: sh

   export SUBJECTS_DIR=/my/ashs/subjects
   freesurfer-volume-reader --source-types ashs

or

.. code:: sh

   freesurfer-volume-reader --source-types ashs -- /my/ashs/subjects
   freesurfer-volume-reader --source-types ashs -- /my/ashs/subjects /other/ashs/subjects

or

.. code:: python

   from freesurfer_volume_reader import ashs

   for volume_file in ashs.HippocampalSubfieldsVolumeFile.find('/my/ashs/subjects'):
       print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
       print(volume_file.read_volumes_mm3())
       print(volume_file.read_volumes_dataframe())

Intracranial Volume
^^^^^^^^^^^^^^^^^^^

.. code:: python

   from freesurfer_volume_reader import ashs

   for volume_file in ashs.IntracranialVolumeFile.find('/my/ashs/subjects'):
       print(volume_file.subject)
       print(volume_file.read_volume_mm3())
       print(volume_file.read_volume_series())

Freesurfer & ASHS
~~~~~~~~~~~~~~~~~

.. code:: sh

   freesurfer-volume-reader --source-types ashs freesurfer-hipposf -- /my/subjects
   freesurfer-volume-reader --source-types ashs freesurfer-hipposf -- /my/ashs/subjects /my/freesurfer/subjects /other/subjects

Tests
-----

.. code:: sh

   pip3 install --user pipenv
   git clone https://github.com/fphammerle/freesurfer-volume-reader.git
   cd freesurfer-volume-reader
   pipenv run pylint freesurfer_volume_reader
   pipenv run pytest
