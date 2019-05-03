import os
import re
import typing


# pylint: disable=too-few-public-methods
class FreesurferHippocampalVolumeFile:

    # https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
    FILENAME_PATTERN = r'^(?P<h>[lr])h\.hippoSfVolumes' \
                       r'(?P<T1>-T1)?(-(?P<analysis_id>.+?))?\.v10.txt$'
    FILENAME_REGEX = re.compile(FILENAME_PATTERN)

    @staticmethod
    def find(root_dir_path: str,
             filename_regex: typing.Pattern = FILENAME_REGEX) -> typing.Iterator[str]:
        for dirpath, _, filenames in os.walk(root_dir_path):
            for filename in filter(filename_regex.search, filenames):
                yield os.path.join(dirpath, filename)
