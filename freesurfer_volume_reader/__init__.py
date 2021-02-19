"""
Read hippocampal subfield volumes computed by Freesurfer and/or ASHS

https://sites.google.com/site/hipposubfields/home
https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields

>>> from freesurfer_volume_reader import ashs, freesurfer
>>>
>>> for volume_file in itertools.chain(
>>>         ashs.HippocampalSubfieldsVolumeFile.find('/my/ashs/subjects'),
>>>         freesurfer.HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects')):
>>>     print(volume_file.absolute_path)
>>>     print(volume_file.subject, volume_file.hemisphere)
>>>     print(volume_file.read_volumes_mm3())
>>>     print(volume_file.read_volumes_dataframe())
"""

import abc
import os
import re
import typing

import pandas

try:
    from freesurfer_volume_reader.version import __version__
except ImportError:  # pragma: no cover
    __version__ = None


def parse_version_string(
    version_string: str,
) -> typing.Tuple[typing.Union[int, str], ...]:
    return tuple(int(p) if p.isdigit() else p for p in version_string.split("."))


def remove_group_names_from_regex(regex_pattern: str) -> str:
    return re.sub(r"\?P<.+?>", "", regex_pattern)


class VolumeFile(metaclass=abc.ABCMeta):

    FILENAME_REGEX = NotImplemented  # type: typing.Pattern[str]

    @abc.abstractmethod
    def __init__(self, path: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def absolute_path(self):
        raise NotImplementedError()

    @classmethod
    def find(
        cls, root_dir_path: str, filename_regex: typing.Optional[typing.Pattern] = None
    ) -> typing.Iterator["VolumeFile"]:
        if filename_regex is None:
            filename_regex = cls.FILENAME_REGEX
        for dirpath, _, filenames in os.walk(root_dir_path):
            for filename in filter(filename_regex.search, filenames):
                yield cls(path=os.path.join(dirpath, filename))


class SubfieldVolumeFile(VolumeFile):
    @abc.abstractmethod
    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_volumes_dataframe(self) -> pandas.DataFrame:
        raise NotImplementedError()

    def _read_volume_series(self) -> pandas.Series:
        subfield_volumes = self.read_volumes_mm3()
        return pandas.Series(
            data=list(subfield_volumes.values()),
            name="volume_mm^3",
            index=pandas.Index(data=subfield_volumes.keys(), name="subfield"),
        )
