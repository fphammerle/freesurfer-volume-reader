"""
Read hippocampal subfield volumes computed by Freesurfer

https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
https://github.com/freesurfer/freesurfer/tree/release_6_0_0/HippoSF

>>> from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile
>>>
>>> for volume_file in HippocampalSubfieldsVolumeFile.find('/my/freesurfer/subjects'):
>>>     print(volume_file.read_volumes_mm3())
>>>     print(volume_file.read_volumes_dataframe())
"""

import os
import re
import typing

import pandas

import freesurfer_volume_reader


class HippocampalSubfieldsVolumeFile(freesurfer_volume_reader.SubfieldVolumeFile):

    # https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
    FILENAME_PATTERN = (
        r"^(?P<h>[lr])h\.hippoSfVolumes"
        r"(?P<T1>-T1)?(-(?P<analysis_id>.+?))?\.v10.txt$"
    )
    FILENAME_REGEX = re.compile(FILENAME_PATTERN)

    FILENAME_HEMISPHERE_PREFIX_MAP = {"l": "left", "r": "right"}

    def __init__(self, path: str):
        self._absolute_path = os.path.abspath(path)
        subject_dir_path = os.path.dirname(os.path.dirname(self._absolute_path))
        self.subject = os.path.basename(subject_dir_path)
        filename_match = self.FILENAME_REGEX.match(os.path.basename(path))
        assert filename_match, self._absolute_path
        filename_groups = filename_match.groupdict()
        assert (
            filename_groups["T1"] or filename_groups["analysis_id"]
        ), self._absolute_path
        self.hemisphere = self.FILENAME_HEMISPHERE_PREFIX_MAP[filename_groups["h"]]
        self.t1_input = filename_groups["T1"] is not None
        self.analysis_id = filename_groups["analysis_id"]
        super().__init__(path=path)

    @property
    def absolute_path(self):
        return self._absolute_path

    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        subfield_volumes = {}
        with open(self.absolute_path, "r") as volume_file:
            for line in volume_file.read().rstrip().split("\n"):
                # https://github.com/freesurfer/freesurfer/blob/release_6_0_0/HippoSF/src/segmentSubjectT1T2_autoEstimateAlveusML.m#L8
                # https://github.com/freesurfer/freesurfer/blob/release_6_0_0/HippoSF/src/segmentSubjectT1T2_autoEstimateAlveusML.m#L1946
                subfield_name, subfield_volume_mm3_str = line.split(" ")
                subfield_volumes[subfield_name] = float(subfield_volume_mm3_str)
        return subfield_volumes

    def read_volumes_dataframe(self) -> pandas.DataFrame:
        volumes_frame = self._read_volume_series().reset_index()
        volumes_frame["subject"] = self.subject
        volumes_frame["hemisphere"] = self.hemisphere
        # volumes_frame['hemisphere'] = volumes_frame['hemisphere'].astype('category')
        volumes_frame["T1_input"] = self.t1_input
        volumes_frame["analysis_id"] = self.analysis_id
        return volumes_frame
