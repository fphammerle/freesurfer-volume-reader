## Usage

```sh
export SUBJECTS_DIR=/my/freesurfer/subjects
freesurfer-volume-reader
```

or

```sh
freesurfer-volume-reader /my/freesurfer/subjects
```

## Tests

```sh
pip3 install --user pipenv
git clone https://github.com/fphammerle/freesurfer-volume-reader.git
cd freesurfer-volume-reader
pipenv run pylint freesurfer_volume_reader
pipenv run pytest
```
