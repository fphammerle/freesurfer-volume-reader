"""
Read hippocampal subfield volumes computed by Freesurfer and/or ASHS
and export collected data as CSV.
"""

import argparse
import os
import re

import pandas

from freesurfer_volume_reader import ashs, freesurfer, parse_version_string, \
                                     remove_group_names_from_regex

VOLUME_FILE_FINDERS = {
    'ashs': ashs.HippocampalSubfieldsVolumeFile,
    # https://github.com/freesurfer/freesurfer/tree/release_6_0_0/HippoSF
    'freesurfer-hipposf': freesurfer.HippocampalSubfieldsVolumeFile,
}


def main():
    argparser = argparse.ArgumentParser(description=__doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argparser.add_argument('--source-types', nargs='+', default=['freesurfer-hipposf'],
                           choices=VOLUME_FILE_FINDERS.keys(),
                           help='default: [freesurfer-hipposf]')
    for source_type, file_class in VOLUME_FILE_FINDERS.items():
        argparser.add_argument('--{}-filename-regex'.format(source_type),
                               dest='filename_regex.{}'.format(source_type),
                               metavar='REGULAR_EXPRESSION', type=re.compile,
                               default=remove_group_names_from_regex(file_class.FILENAME_PATTERN),
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
    filename_regexs = {k[len('filename_regex.'):]: v for k, v in vars(args).items()
                       if k.startswith('filename_regex.')}
    volume_frames = []
    for source_type in args.source_types:
        finder = VOLUME_FILE_FINDERS[source_type].find
        for root_dir_path in args.root_dir_paths:
            for volume_file in finder(root_dir_path=root_dir_path,
                                      filename_regex=filename_regexs[source_type]):
                volume_frame = volume_file.read_volumes_dataframe()
                volume_frame['source_type'] = source_type
                volume_frame['source_path'] = volume_file.absolute_path
                volume_frames.append(volume_frame)
    if parse_version_string(pandas.__version__) < (0, 23):
        united_volume_frame = pandas.concat(volume_frames, ignore_index=True)
    else:
        # pylint: disable=unexpected-keyword-arg
        united_volume_frame = pandas.concat(volume_frames, ignore_index=True, sort=False)
    print(united_volume_frame.to_csv(index=False))

if __name__ == '__main__':
    main()
