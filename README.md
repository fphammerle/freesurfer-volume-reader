# freesurfer-volume-reader

[![Build Status](https://travis-ci.org/fphammerle/freesurfer-volume-reader.svg?branch=master)](https://travis-ci.org/fphammerle/freesurfer-volume-reader)

Python script & library to
read hippocampal subfield volumes computed by Freesurfer

https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields

## Install

```sh
pip3 install --user freesurfer-volume-reader
freesurfer-volume-reader --help
```

## Usage

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

```python
from freesurfer_volume_reader import ashs

for volume_file in ashs.HippocampalSubfieldsVolumeFile.find('/my/ashs/subjects'):
    print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
    print(volume_file.read_volumes_mm3())
    print(volume_file.read_volumes_dataframe())
```

## Tests

```sh
pip3 install --user pipenv
git clone https://github.com/fphammerle/freesurfer-volume-reader.git
cd freesurfer-volume-reader
pipenv run pylint freesurfer_volume_reader
pipenv run pytest
```
