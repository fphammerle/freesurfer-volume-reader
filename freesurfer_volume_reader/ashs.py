"""
Read hippocampal subfield volumes computed by ASHS

https://sites.google.com/site/hipposubfields/home

>>> from freesurfer_volume_reader.ashs import HippocampalSubfieldsVolumeFile
>>>
>>> for volume_file in HippocampalSubfieldsVolumeFile('/my/ashs/subjects'):
>>>     print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
>>>     print(volume_file.read_volumes_mm3())
>>>     print(volume_file.read_volumes_dataframe())

>>> from freesurfer_volume_reader.ashs import IntracranialVolumeFile
>>>
>>> for volume_file in IntracranialVolumeFile('/my/ashs/subjects'):
>>>     print(volume_file.subject)
>>>     print(volume_file.read_volume_mm3())
>>>     print(volume_file.read_volume_series())
"""

import os
import re
import typing

import pandas

import freesurfer_volume_reader


class IntracranialVolumeFile(freesurfer_volume_reader.VolumeFile):

    FILENAME_REGEX = re.compile(r"^(?P<s>\w+)_icv.txt$")

    def __init__(self, path: str):
        self._absolute_path = os.path.abspath(path)
        filename_match = self.FILENAME_REGEX.match(os.path.basename(path))
        assert filename_match, self._absolute_path
        self.subject = filename_match.groupdict()["s"]
        super().__init__(path=path)

    @property
    def absolute_path(self):
        return self._absolute_path

    def read_volume_mm3(self) -> float:
        with open(self.absolute_path, "r") as volume_file:
            subject, icv = volume_file.read().rstrip().split(" ")
            assert subject == self.subject, (subject, self.subject)
            return float(icv)

    def read_volume_series(self) -> pandas.Series:
        return pandas.Series(
            data=[self.read_volume_mm3()],
            name="intercranial_volume_mm^3",
            index=pandas.Index(data=[self.subject], name="subject"),
        )


class HippocampalSubfieldsVolumeFile(freesurfer_volume_reader.SubfieldVolumeFile):

    # https://sites.google.com/site/hipposubfields/tutorial#TOC-Viewing-ASHS-Segmentation-Results
    FILENAME_PATTERN = (
        r"^(?P<s>\w+)_(?P<h>left|right)"
        r"_(heur|corr_(?P<c>nogray|usegray))_volumes.txt$"
    )
    FILENAME_REGEX = re.compile(FILENAME_PATTERN)

    def __init__(self, path: str):
        self._absolute_path = os.path.abspath(path)
        filename_match = self.FILENAME_REGEX.match(os.path.basename(path))
        assert filename_match, self._absolute_path
        filename_groups = filename_match.groupdict()
        self.subject = filename_groups["s"]
        self.hemisphere = filename_groups["h"]
        self.correction = filename_groups["c"]
        super().__init__(path=path)

    @property
    def absolute_path(self):
        return self._absolute_path

    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        subfield_volumes = {}
        with open(self.absolute_path, "r") as volume_file:
            for line in volume_file.read().rstrip().split("\n"):
                # > echo $ASHS_SUBJID $side $SUB $NBODY $VSUB >> $FNBODYVOL
                # https://github.com/pyushkevich/ashs/blob/515ff7c2f50928adabc4e64bded9a7e76fc750b1/bin/ashs_extractstats_qsub.sh#L94
                (
                    subject,
                    hemisphere,
                    subfield_name,
                    slices_number_str,
                    volume_mm3_str,
                ) = line.split(" ")
                assert self.subject == subject
                assert self.hemisphere == hemisphere
                assert int(slices_number_str) >= 0
                subfield_volumes[subfield_name] = float(volume_mm3_str)
        return subfield_volumes

    def read_volumes_dataframe(self) -> pandas.DataFrame:
        volumes_frame = self._read_volume_series().reset_index()
        volumes_frame["subject"] = self.subject
        volumes_frame["hemisphere"] = self.hemisphere
        volumes_frame["correction"] = self.correction
        return volumes_frame
