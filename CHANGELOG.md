# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- return type hint of `parse_version_string()` & `VolumeFile.find()`

## [2.1.0] - 2020-07-11
### Added
- support `pandas` `v1.*`

## [2.0.0] - 2019-08-08
### Changed
- python library: split class `SubfieldVolumeFile` from `VolumeFile`

### Added
- python library: class `ashs.IntracranialVolumeFile`
- examples:
  - added ASHS
  - added comparison FreeSurfer vs. ASHS

### Fixed
* install: no longer require runtime dependencies to run `setup.py`

## [1.0.0] - 2019-05-05
### Changed
- console entry point `freesurfer-volume-reader`:
  - exit with code `EX_NOINPUT`/`66` in case no matching volume files were found
    (previously: exception with exit code `1`)
  - renamed param `--filename-regex` to `--freesurfer-hipposf-filename-regex`
- python library:
  - renamed `read_hippocampal_volume_file_dataframe()`
    to `freesurfer.HippocampalSubfieldsVolumeFile.read_volumes_dataframe()`
  - renamed `read_hippocampal_volumes_mm3()`
    to `freesurfer.HippocampalSubfieldsVolumeFile.read_volumes_mm3()`
  - renamed `parse_hippocampal_volume_file_path()`
    to `freesurfer.HippocampalSubfieldsVolumeFile.__init__()`
  - renamed `find_hippocampal_volume_files()`
    to `freesurfer.FreesurferHippocampalVolumeFile.find()`

### Added
- console entry point `freesurfer-volume-reader`:
  - flag `--version` to show version
  - param `--source-types` to optionally enable collection of ASHS `*volumes.txt` files
    (default: freesurfer only)
  - param `--ashs-filename-regex`
- python library: added class `ashs.HippocampalSubfieldsVolumeFile`
  to find & read ASHS *volumes.txt files

## [0.2.1] - 2019-04-28
### Fixed
- added pandas version constraint (required for `pandas.DataFrame.drop`)

## [0.2.0] - 2019-04-28
### Added
- accept multiple args for positional param `root_dir_paths`

### Fixed
- invalid root path when `$SUBJECTS_DIR` is set and root dir path is provided as positional arg

## [0.1.1] - 2019-04-27
### Fixed
- test `read_hippocampal_volume_file_dataframe` on python3.5

## [0.1.0] - 2019-04-26
### Added
- script `freesurfer-volume-reader`:
  - recursively collect Freesurfer's hippocampal subfield volume files
  - output in CSV-format
- python module `freesurfer_volume_reader`

[Unreleased]: https://github.com/fphammerle/freesurfer-volume-reader/compare/2.1.0...HEAD
[2.1.0]: https://github.com/fphammerle/freesurfer-volume-reader/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/fphammerle/freesurfer-volume-reader/compare/1.0.0...2.0.0
[1.0.0]: https://github.com/fphammerle/freesurfer-volume-reader/compare/0.2.1...1.0.0
[0.2.1]: https://github.com/fphammerle/freesurfer-volume-reader/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/fphammerle/freesurfer-volume-reader/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/fphammerle/freesurfer-volume-reader/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/fphammerle/freesurfer-volume-reader/tree/0.1.0
