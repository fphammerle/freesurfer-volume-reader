"""
Read hippocampal subfield volumes computed by ASHS

https://sites.google.com/site/hipposubfields/home

>>> from freesurfer_volume_reader.ashs import HippocampalSubfieldsVolumeFile
>>>
>>> volume_file = HippocampalSubfieldsVolumeFile('ashs/final/bert_right_corr_nogray_volumes.txt')
>>> print(volume_file.subject, volume_file.hemisphere, volume_file.correction)
"""

import os
import re

import freesurfer_volume_reader

# pylint: disable=too-few-public-methods
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
