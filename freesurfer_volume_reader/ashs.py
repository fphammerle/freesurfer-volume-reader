"""
Read hippocampal subfield volumes computed by ASHS

https://sites.google.com/site/hipposubfields/home

>>> from freesurfer_volume_reader.ashs import HippocampalSubfieldsVolumeFile
>>>
>>> volume_file = HippocampalSubfieldsVolumeFile('ashs/final/bert_right_corr_nogray_volumes.txt')
>>> print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
>>> print(volume_file.read_volumes_mm3())
"""

import os
import re
import typing

import freesurfer_volume_reader

class HippocampalSubfieldsVolumeFile(freesurfer_volume_reader.VolumeFile):

    # https://sites.google.com/site/hipposubfields/tutorial#TOC-Viewing-ASHS-Segmentation-Results
    FILENAME_PATTERN = r'^(?P<s>\w+)_(?P<h>left|right)' \
                       r'_(heur|corr_(?P<c>nogray|usegray))_volumes.txt$'
    FILENAME_REGEX = re.compile(FILENAME_PATTERN)

    def __init__(self, path: str):
        self._absolute_path = os.path.abspath(path)
        filename_match = self.FILENAME_REGEX.match(os.path.basename(path))
        assert filename_match, self._absolute_path
        filename_groups = filename_match.groupdict()
        self.subject = filename_groups['s']
        self.hemisphere = filename_groups['h']
        self.correction = filename_groups['c']

    @property
    def absolute_path(self):
        return self._absolute_path

    def read_volumes_mm3(self) -> typing.Dict[str, float]:
        subfield_volumes = {}
        with open(self.absolute_path, 'r') as volume_file:
            for line in volume_file.read().rstrip().split('\n'):
                # > echo $ASHS_SUBJID $side $SUB $NBODY $VSUB >> $FNBODYVOL
                # https://github.com/pyushkevich/ashs/blob/515ff7c2f50928adabc4e64bded9a7e76fc750b1/bin/ashs_extractstats_qsub.sh#L94
                subject, hemisphere, subfield_name, slices_number_str, volume_mm3_str \
                    = line.split(' ')
                assert self.subject == subject
                assert self.hemisphere == hemisphere
                assert int(slices_number_str) >= 0
                subfield_volumes[subfield_name] = float(volume_mm3_str)
        return subfield_volumes
