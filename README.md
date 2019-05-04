# freesurfer-volume-reader

[![Build Status](https://travis-ci.org/fphammerle/freesurfer-volume-reader.svg?branch=master)](https://travis-ci.org/fphammerle/freesurfer-volume-reader)
[![Coverage Status](https://coveralls.io/repos/github/fphammerle/freesurfer-volume-reader/badge.svg?branch=master)](https://coveralls.io/github/fphammerle/freesurfer-volume-reader?branch=master)

Python script & library to
read hippocampal subfield volumes computed by Freesurfer & ASHS

* Freesurfer https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
* ASHS https://sites.google.com/site/hipposubfields/home

## Install

```sh
pip3 install --user freesurfer-volume-reader
freesurfer-volume-reader --help
```

## Usage

### Freesurfer

```sh
export SUBJECTS_DIR=/my/freesurfer/subjects
freesurfer-volume-reader
```

or

```sh
freesurfer-volume-reader /my/freesurfer/subjects
freesurfer-volume-reader /my/freesurfer/subjects /other/freesurfer/subjects
```

or

```python
from freesurfer_volume_reader import freesurfer

for volume_file in freesurfer.HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects'):
    print(volume_file.subject, volume_file.hemisphere, volume_file.analysis_id)
    print(volume_file.read_volumes_mm3())
    print(volume_file.read_volumes_dataframe())
```

### ASHS

```sh
export SUBJECTS_DIR=/my/ashs/subjects
freesurfer-volume-reader --source-types ashs
```

or

```sh
freesurfer-volume-reader --source-types ashs -- /my/ashs/subjects
freesurfer-volume-reader --source-types ashs -- /my/ashs/subjects /other/ashs/subjects
```

or

```python
from freesurfer_volume_reader import ashs

for volume_file in ashs.HippocampalSubfieldsVolumeFile.find('/my/ashs/subjects'):
    print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
    print(volume_file.read_volumes_mm3())
    print(volume_file.read_volumes_dataframe())
```

### Freesurfer & ASHS

```sh
freesurfer-volume-reader --source-types ashs freesurfer-hipposf -- /my/subjects
freesurfer-volume-reader --source-types ashs freesurfer-hipposf -- /my/ashs/subjects /my/freesurfer/subjects /other/subjects
```

## Tests

```sh
pip3 install --user pipenv
git clone https://github.com/fphammerle/freesurfer-volume-reader.git
cd freesurfer-volume-reader
pipenv run pylint freesurfer_volume_reader
pipenv run pytest
```
