"""
Read hippocampal subfield volumes computed by Freesurfer

https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields

>>> from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile
>>>
>>> for volume_file in HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects'):
>>>     print(volume_file.read_volumes_mm3())
>>>     print(volume_file.read_volumes_dataframe())
"""

import abc
import os
import typing


class VolumeFile(metaclass=abc.ABCMeta):

    FILENAME_REGEX = NotImplemented

    @property
    @abc.abstractmethod
    def absolute_path(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        raise NotImplementedError()

    @classmethod
    def find(cls, root_dir_path: str,
             filename_regex: typing.Optional[typing.Pattern] = None) -> typing.Iterator[str]:
        if not filename_regex:
            filename_regex = cls.FILENAME_REGEX
        for dirpath, _, filenames in os.walk(root_dir_path):
            for filename in filter(filename_regex.search, filenames):
                yield cls(path=os.path.join(dirpath, filename))
