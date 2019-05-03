"""
Read hippocampal subfield volumes computed by Freesurfer

https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
"""

import argparse
import os
import re
import typing

import pandas

from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile


def remove_group_names_from_regex(regex_pattern: str) -> str:
    return re.sub(r'\?P<.+?>', '', regex_pattern)


def read_hippocampal_volume_file_dataframe(volume_file: HippocampalSubfieldsVolumeFile,
                                           ) -> pandas.DataFrame:
    volumes_frame = pandas.DataFrame([
        {'subfield': s, 'volume_mm^3': v}
        for s, v in volume_file.read_volumes_mm3().items()
    ])
    volumes_frame['subject'] = volume_file.subject
    volumes_frame['hemisphere'] = volume_file.hemisphere
    # volumes_frame['hemisphere'] = volumes_frame['hemisphere'].astype('category')
    volumes_frame['T1_input'] = volume_file.t1_input
    volumes_frame['analysis_id'] = volume_file.analysis_id
    return volumes_frame


def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--filename-regex', type=re.compile,
                           default=remove_group_names_from_regex(
                               HippocampalSubfieldsVolumeFile.FILENAME_PATTERN),
                           help='default: %(default)s')
    argparser.add_argument('--output-format', choices=['csv'], default='csv',
                           help='default: %(default)s')
    subjects_dir_path = os.environ.get('SUBJECTS_DIR', None)
    argparser.add_argument('root_dir_paths',
                           metavar='ROOT_DIR',
                           nargs='*' if subjects_dir_path else '+',
                           default=[subjects_dir_path],
                           help='default: $SUBJECTS_DIR ({})'.format(subjects_dir_path))
    args = argparser.parse_args()
    volume_files = [f for d in args.root_dir_paths
                    for f in HippocampalSubfieldsVolumeFile.find(
                        root_dir_path=d, filename_regex=args.filename_regex)]
    volume_frames = []
    for volume_file in volume_files:
        volume_frame = read_hippocampal_volume_file_dataframe(volume_file)
        volume_frame['source_path'] = volume_file.absolute_path
        volume_frames.append(volume_frame)
    united_volume_frame = pandas.concat(volume_frames, ignore_index=True)
    print(united_volume_frame.to_csv(index=False))

if __name__ == '__main__':
    main()
