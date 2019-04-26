import argparse
import os
import re
import typing

import pandas

# https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields
HIPPOCAMPAL_VOLUME_FILENAME_PATTERN = r'^(?P<h>[lr])h\.hippoSfVolumes' \
                                      r'(?P<T1>-T1)?(-(?P<analysis_id>.+?))?\.v10.txt$'
HIPPOCAMPAL_VOLUME_FILENAME_REGEX = re.compile(HIPPOCAMPAL_VOLUME_FILENAME_PATTERN)
DEFAULT_HIPPOCAMPAL_VOLUME_FIND_FILENAME_PATTERN = re.sub(r'\?P<.+?>', '',
                                                          HIPPOCAMPAL_VOLUME_FILENAME_PATTERN)

VOLUME_FILENAME_HEMISPHERE_MAP = {'l': 'left', 'r': 'right'}


def find_hippocampal_volume_files(root_dir_path: str,
                                  filename_regex: typing.Pattern = HIPPOCAMPAL_VOLUME_FILENAME_REGEX
                                  ) -> typing.Iterator[str]:
    for dirpath, _, filenames in os.walk(root_dir_path):
        for filename in filter(filename_regex.search, filenames):
            yield os.path.join(dirpath, filename)


def read_hippocampal_volumes(volume_file_path: str) -> dict:
    subfield_volumes = {}
    with open(volume_file_path, 'r') as volume_file:
        for line in volume_file.read().rstrip().split('\n'):
            # https://github.com/freesurfer/freesurfer/blob/release_6_0_0/HippoSF/src/segmentSubjectT1T2_autoEstimateAlveusML.m#L1946
            subfield_name, subfield_volume_str = line.split(' ')
            subfield_volumes[subfield_name] = float(subfield_volume_str)
    return subfield_volumes


def parse_hippocampal_volume_file_path(volume_file_path: str) -> dict:
    subject_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(volume_file_path)))
    filename_match = HIPPOCAMPAL_VOLUME_FILENAME_REGEX.match(os.path.basename(volume_file_path))
    assert filename_match, volume_file_path
    filename_groups = filename_match.groupdict()
    assert filename_groups['T1'] or filename_groups['analysis_id'], volume_file_path
    return {
        'subject': os.path.basename(subject_dir_path),
        'hemisphere': VOLUME_FILENAME_HEMISPHERE_MAP[filename_groups['h']],
        'T1_input': filename_groups['T1'] is not None,
        'analysis_id': filename_groups['analysis_id'],
    }


def read_hippocampal_volume_file_dataframe(volume_file_path: str) -> pandas.DataFrame:
    volumes_frame = pandas.DataFrame(
        read_hippocampal_volumes(volume_file_path).items(),
        columns=['subfield', 'volume'])
    for key, value in parse_hippocampal_volume_file_path(volume_file_path).items():
        volumes_frame[key] = value
    # volumes_frame['hemisphere'] = volumes_frame['hemisphere'].astype('category')
    return volumes_frame


def main():
    argparser = argparse.ArgumentParser(
        description='Read hippocampal subfield volumes computed by Freesurfer'
                    '\nhttps://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfields')
    argparser.add_argument('--filename-regex', dest='filename_pattern',
                           default=DEFAULT_HIPPOCAMPAL_VOLUME_FIND_FILENAME_PATTERN,
                           help='default: %(default)s')
    argparser.add_argument('--output-format', choices=['csv'], default='csv',
                           help='default: %(default)s')
    subjects_dir_path = os.environ.get('SUBJECTS_DIR', None)
    argparser.add_argument('root_dir_path',
                           nargs='?' if subjects_dir_path  else 1,
                           default=[subjects_dir_path],
                           help='default: $SUBJECTS_DIR ({})'.format(subjects_dir_path))
    args = argparser.parse_args()
    volume_file_paths = find_hippocampal_volume_files(
        root_dir_path=args.root_dir_path[0],
        filename_regex=re.compile(args.filename_pattern))
    volume_frames = []
    for volume_file_path in volume_file_paths:
        volume_frame = read_hippocampal_volume_file_dataframe(volume_file_path)
        volume_frame['source_path'] = os.path.abspath(volume_file_path)
        volume_frames.append(volume_frame)
    united_volume_frame = pandas.concat(volume_frames, ignore_index=True)
    print(united_volume_frame.to_csv(index=False))

if __name__ == '__main__':
    main()
