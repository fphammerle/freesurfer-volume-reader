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
from freesurfer_volume_reader import find_hippocampal_volume_files, \
                                     read_hippocampal_volume_file_dataframe

for volume_file_path in find_hippocampal_volume_files('/my/freesurfer/subjects'):
    print(read_hippocampal_volume_file_dataframe(volume_file_path))
```

## Tests

```sh
pip3 install --user pipenv
git clone https://github.com/fphammerle/freesurfer-volume-reader.git
cd freesurfer-volume-reader
pipenv run pylint freesurfer_volume_reader
pipenv run pytest
```
