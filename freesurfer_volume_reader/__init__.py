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
import typing


class VolumeFile(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def absolute_path(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        raise NotImplementedError()
