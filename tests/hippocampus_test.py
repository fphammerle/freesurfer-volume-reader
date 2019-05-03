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


@pytest.mark.parametrize(('volume_file_path', 'expected_volumes'), [
    (os.path.join(SUBJECTS_DIR, 'bert/mri/lh.hippoSfVolumes-T1.v10.txt'),
     {'Hippocampal_tail': 123.456789,
      'subiculum': 234.567891,
      'CA1': 34.567891,
      'hippocampal-fissure': 345.678912,
      'presubiculum': 456.789123,
      'parasubiculum': 45.678912,
      'molecular_layer_HP': 56.789123,
      'GC-ML-DG': 567.891234,
      'CA3': 678.912345,
      'CA4': 789.123456,
      'fimbria': 89.123456,
      'HATA': 91.234567,
      'Whole_hippocampus': 1234.567899}),
])
def test_read_hippocampal_volumes_mm3(volume_file_path, expected_volumes):
    assert expected_volumes == freesurfer_volume_reader.read_hippocampal_volumes_mm3(
        volume_file_path)


def test_read_hippocampal_volumes_mm3_not_found():
    with pytest.raises(FileNotFoundError):
        freesurfer_volume_reader.read_hippocampal_volumes_mm3(
            os.path.join(SUBJECTS_DIR, 'non-existing', 'lh.hippoSfVolumes-T1.v10.txt'))


@pytest.mark.parametrize(('volume_file_path', 'expected_dataframe'), [
    (os.path.join(SUBJECTS_DIR, 'alice', 'mri', 'lh.hippoSfVolumes-T1.v10.txt'),
     pandas.DataFrame({
         'subfield': ['Hippocampal_tail', 'subiculum', 'CA1', 'hippocampal-fissure',
                      'presubiculum', 'parasubiculum', 'molecular_layer_HP', 'GC-ML-DG',
                      'CA3', 'CA4', 'fimbria', 'HATA', 'Whole_hippocampus'],
         'volume_mm^3': [173.456789, 734.567891, 34.567891, 345.678917, 456.789173, 45.678917,
                         56.789173, 567.891734, 678.917345, 789.173456, 89.173456, 91.734567,
                         1734.567899],
         'subject': 'alice',
         'hemisphere': 'left',
         'T1_input': True,
         'analysis_id': None,
     })),
])
def test_read_hippocampal_volume_file_dataframe(volume_file_path, expected_dataframe):
    volume_file = freesurfer_volume_reader.freesurfer.HippocampalSubfieldsVolumeFile(
        path=volume_file_path)
    assert_volume_frames_equal(
        left=expected_dataframe,
        right=freesurfer_volume_reader.read_hippocampal_volume_file_dataframe(
            volume_file=volume_file),
    )


def assert_volume_frames_equal(left: pandas.DataFrame, right: pandas.DataFrame):
    sort_by = ['volume_mm^3', 'analysis_id']
    left.sort_values(sort_by, inplace=True)
    right.sort_values(sort_by, inplace=True)
    left.reset_index(inplace=True, drop=True)
    right.reset_index(inplace=True, drop=True)
    pandas.util.testing.assert_frame_equal(
        left=left,
        right=right,
        # ignore the order of index & columns
        check_like=True,
    )


def assert_main_volume_frame_equals(capsys, argv: list, expected_frame: pandas.DataFrame,
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
def test_main_root_dir_param(capsys, root_dir_paths: list, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=root_dir_paths,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


@pytest.mark.parametrize(('root_dir_path', 'expected_csv_path'), [
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
])
def test_main_root_dir_env(capsys, root_dir_path, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=[],
        subjects_dir=root_dir_path,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
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
def test_main_root_dir_overwrite_env(capsys, root_dir_path, subjects_dir, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=[root_dir_path],
        subjects_dir=subjects_dir,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv'))
    assert_main_volume_frame_equals(
        argv=['--filename-regex', r'^.*-T1-T2\.v10\.txt$',
              os.path.join(SUBJECTS_DIR, 'bert')],
        expected_frame=expected_volume_frame[expected_volume_frame['analysis_id'] == 'T2'].copy(),
        capsys=capsys,
    )
