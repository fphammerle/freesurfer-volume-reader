import os
import re
import typing

# pylint: disable=too-few-public-methods
class HippocampalSubfieldsVolumeFile:

    # https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
    FILENAME_PATTERN = r'^(?P<h>[lr])h\.hippoSfVolumes' \
                       r'(?P<T1>-T1)?(-(?P<analysis_id>.+?))?\.v10.txt$'
    FILENAME_REGEX = re.compile(FILENAME_PATTERN)

    FILENAME_HEMISPHERE_PREFIX_MAP = {'l': 'left', 'r': 'right'}

    def __init__(self, path: str):
        self._absolute_path = os.path.abspath(path)
        subject_dir_path = os.path.dirname(os.path.dirname(self._absolute_path))
        self.subject = os.path.basename(subject_dir_path)
        filename_match = self.FILENAME_REGEX.match(os.path.basename(path))
        assert filename_match, self._absolute_path
        filename_groups = filename_match.groupdict()
        assert filename_groups['T1'] or filename_groups['analysis_id'], self._absolute_path
        self.hemisphere = self.FILENAME_HEMISPHERE_PREFIX_MAP[filename_groups['h']]
        self.t1_input = filename_groups['T1'] is not None
        self.analysis_id = filename_groups['analysis_id']

    @property
    def absolute_path(self):
        return self._absolute_path

    @classmethod
    def find(cls, root_dir_path: str,
             filename_regex: typing.Pattern = FILENAME_REGEX) -> typing.Iterator[str]:
        for dirpath, _, filenames in os.walk(root_dir_path):
            for filename in filter(filename_regex.search, filenames):
                yield cls(path=os.path.join(dirpath, filename))
