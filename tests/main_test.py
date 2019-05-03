import io
import os
import typing
import unittest.mock

import pandas
import pandas.util.testing
import pytest

import freesurfer_volume_reader.__main__

from conftest import SUBJECTS_DIR, assert_volume_frames_equal


def assert_main_volume_frame_equals(capsys, argv: list, expected_frame: pandas.DataFrame,
                                    subjects_dir: typing.Optional[str] = None):
    if subjects_dir:
        os.environ['SUBJECTS_DIR'] = subjects_dir
    elif 'SUBJECTS_DIR' in os.environ:
        del os.environ['SUBJECTS_DIR']
    with unittest.mock.patch('sys.argv', [''] + argv):
        freesurfer_volume_reader.__main__.main()
    out, _ = capsys.readouterr()
    assert_volume_frames_equal(
        left=expected_frame,
        # pandas.DataFrame.drop(columns=[...], ...) >= pandas0.21.0
        right=pandas.read_csv(io.StringIO(out)).drop(columns=['source_path']),
    )


@pytest.mark.parametrize(('args', 'root_dir_paths', 'expected_csv_path'), [
    ([],
     [os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'freesurfer-hippocampal-volumes.csv')),
    ([],
     [os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
    ([],
     [os.path.join(SUBJECTS_DIR, 'alice'),
      os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'freesurfer-hippocampal-volumes.csv')),
    ([],
     [SUBJECTS_DIR],
     os.path.join(SUBJECTS_DIR, 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer'],
     [os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer'],
     [SUBJECTS_DIR],
     os.path.join(SUBJECTS_DIR, 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     [os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     [os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'bert', 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     [os.path.join(SUBJECTS_DIR, 'alice'),
      os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     [SUBJECTS_DIR],
     os.path.join(SUBJECTS_DIR, 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs', 'freesurfer'],
     [os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'all-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer', 'ashs'],
     [os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'all-hippocampal-volumes.csv')),
    (['--source-types', 'ashs', 'freesurfer'],
     [os.path.join(SUBJECTS_DIR, 'alice'),
      os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'all-hippocampal-volumes.csv')),
    (['--source-types', 'ashs', 'freesurfer'],
     [SUBJECTS_DIR],
     os.path.join(SUBJECTS_DIR, 'all-hippocampal-volumes.csv')),
])
def test_main_root_dir_param(capsys, args, root_dir_paths: list, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=args + ['--'] + root_dir_paths,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


@pytest.mark.parametrize(('args', 'root_dir_path', 'expected_csv_path'), [
    ([],
     SUBJECTS_DIR,
     os.path.join(SUBJECTS_DIR, 'freesurfer-hippocampal-volumes.csv')),
    ([],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer'],
     SUBJECTS_DIR,
     os.path.join(SUBJECTS_DIR, 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer'],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer'],
     os.path.join(SUBJECTS_DIR, 'bert', 'mri'),
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     SUBJECTS_DIR,
     os.path.join(SUBJECTS_DIR, 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     os.path.join(SUBJECTS_DIR, 'bert', 'final'),
     os.path.join(SUBJECTS_DIR, 'bert', 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'alice', 'ashs-hippocampal-volumes.csv')),
    (['--source-types', 'ashs', 'freesurfer'],
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'alice', 'all-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer', 'ashs'],
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'alice', 'all-hippocampal-volumes.csv')),
    (['--source-types', 'freesurfer', 'ashs'],
     SUBJECTS_DIR,
     os.path.join(SUBJECTS_DIR, 'all-hippocampal-volumes.csv')),
])
def test_main_root_dir_env(capsys, args, root_dir_path, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=args,
        subjects_dir=root_dir_path,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


@pytest.mark.timeout(8)
@pytest.mark.parametrize(('args', 'root_dir_path', 'subjects_dir', 'expected_csv_path'), [
    ([],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
    (['--source-types', 'ashs'],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'bert', 'ashs-hippocampal-volumes.csv')),
    ([],
     os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.abspath(os.sep),
     os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv')),
])
def test_main_root_dir_overwrite_env(capsys, args, root_dir_path, subjects_dir, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=args + ['--', root_dir_path],
        subjects_dir=subjects_dir,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex_freesurfer(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, 'bert', 'freesurfer-hippocampal-volumes.csv'))
    assert_main_volume_frame_equals(
        argv=['--freesurfer-filename-regex', r'^.*-T1-T2\.v10\.txt$',
              os.path.join(SUBJECTS_DIR, 'bert')],
        expected_frame=expected_volume_frame[expected_volume_frame['analysis_id'] == 'T2'].copy(),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex_ashs(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, 'bert', 'ashs-hippocampal-volumes.csv'))
    assert_main_volume_frame_equals(
        argv=['--ashs-filename-regex', r'_nogray_volumes.txt$',
              '--source-types', 'ashs', '--',
              os.path.join(SUBJECTS_DIR, 'bert')],
        expected_frame=expected_volume_frame[expected_volume_frame['correction']
                                             == 'nogray'].copy(),
        capsys=capsys,
    )
