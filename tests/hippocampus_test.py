import io
import os
import typing
import unittest.mock

import pandas
import pandas.util.testing
import pytest

import freesurfer_volume_reader
import freesurfer_volume_reader.freesurfer

SUBJECTS_DIR = os.path.join(os.path.dirname(__file__), 'subjects')


@pytest.mark.parametrize(('source_pattern', 'expected_pattern'), [
    (r'^(?P<h>[lr])h\.hippoSfVolumes', r'^([lr])h\.hippoSfVolumes'),
    (r'(?P<a>a(?P<b>b))', r'(a(b))'),
])
def test_remove_group_names_from_regex(source_pattern, expected_pattern):
    assert expected_pattern == freesurfer_volume_reader.remove_group_names_from_regex(
        regex_pattern=source_pattern,
    )


def assert_main_volume_frame_equals(capsys, assert_volume_frames_equal,
                                    argv: list, expected_frame: pandas.DataFrame,
                                    subjects_dir: typing.Optional[str] = None):
    if subjects_dir:
        os.environ['SUBJECTS_DIR'] = subjects_dir
    elif 'SUBJECTS_DIR' in os.environ:
        del os.environ['SUBJECTS_DIR']
    with unittest.mock.patch('sys.argv', [''] + argv):
        freesurfer_volume_reader.main()
    out, _ = capsys.readouterr()
    assert_volume_frames_equal(
        left=expected_frame,
        # pandas.DataFrame.drop(columns=[...], ...) >= pandas0.21.0
        right=pandas.read_csv(io.StringIO(out)).drop(columns=['source_path']),
    )


@pytest.mark.parametrize(('root_dir_paths', 'expected_csv_path'), [
    ([os.path.join(SUBJECTS_DIR, 'alice')],
     os.path.join(SUBJECTS_DIR, 'alice', 'hippocampal-volumes.csv')),
    ([os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
    ([os.path.join(SUBJECTS_DIR, 'alice'),
      os.path.join(SUBJECTS_DIR, 'bert')],
     os.path.join(SUBJECTS_DIR, 'all-hippocampal-volumes.csv')),
])
def test_main_root_dir_param(capsys, assert_volume_frames_equal,
                             root_dir_paths: list, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=root_dir_paths,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
        assert_volume_frames_equal=assert_volume_frames_equal,
    )


@pytest.mark.parametrize(('root_dir_path', 'expected_csv_path'), [
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
])
def test_main_root_dir_env(capsys, assert_volume_frames_equal,
                           root_dir_path, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=[],
        subjects_dir=root_dir_path,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
        assert_volume_frames_equal=assert_volume_frames_equal,
    )


@pytest.mark.timeout(8)
@pytest.mark.parametrize(('root_dir_path', 'subjects_dir', 'expected_csv_path'), [
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'alice'),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.abspath(os.sep),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
])
def test_main_root_dir_overwrite_env(capsys, assert_volume_frames_equal,
                                     root_dir_path, subjects_dir, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=[root_dir_path],
        subjects_dir=subjects_dir,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
        assert_volume_frames_equal=assert_volume_frames_equal,
    )


def test_main_root_dir_filename_regex(capsys, assert_volume_frames_equal):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv'))
    assert_main_volume_frame_equals(
        argv=['--filename-regex', r'^.*-T1-T2\.v10\.txt$',
              os.path.join(SUBJECTS_DIR, 'bert')],
        expected_frame=expected_volume_frame[expected_volume_frame['analysis_id'] == 'T2'].copy(),
        capsys=capsys,
        assert_volume_frames_equal=assert_volume_frames_equal,
    )
