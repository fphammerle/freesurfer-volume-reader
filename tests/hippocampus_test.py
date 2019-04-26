import io
import os
import re
import unittest.mock

import pandas.util.testing
import pytest

import freesurfer_volume_reader

SUBJECTS_DIR = os.path.join(os.path.dirname(__file__), 'subjects')


@pytest.mark.parametrize(('root_dir_path', 'expected_file_paths'), [
    (SUBJECTS_DIR,
     {os.path.join(SUBJECTS_DIR, 'alice', 'mri', 'lh.hippoSfVolumes-T1.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1-T2.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1.v10.txt')}),
    (os.path.join(SUBJECTS_DIR, 'bert'),
     {os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1-T2.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1.v10.txt')}),
    (os.path.join(SUBJECTS_DIR, 'bert', 'mri'),
     {os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1-T2.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1.v10.txt')}),
])
def test_find_hippocampal_volume_files(root_dir_path, expected_file_paths):
    assert expected_file_paths == set(
        freesurfer_volume_reader.find_hippocampal_volume_files(root_dir_path=root_dir_path))


@pytest.mark.parametrize(('root_dir_path', 'filename_pattern', 'expected_file_paths'), [
    (SUBJECTS_DIR,
     r'hippoSfVolumes-T1\.v10',
     {os.path.join(SUBJECTS_DIR, 'alice', 'mri', 'lh.hippoSfVolumes-T1.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1.v10.txt')}),
    (os.path.join(SUBJECTS_DIR, 'bert'),
     r'hippoSfVolumes-T1-T2',
     {os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1-T2.v10.txt')}),
])
def test_find_hippocampal_volume_files_pattern(root_dir_path, filename_pattern,
                                               expected_file_paths):
    assert expected_file_paths == set(freesurfer_volume_reader.find_hippocampal_volume_files(
        root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)))


@pytest.mark.parametrize(('volume_file_path', 'expected_volumes'), [
    (os.path.join(SUBJECTS_DIR, 'bert/mri/lh.hippoSfVolumes-T1.v10.txt'),
     {'Hippocampal_tail': 123.456789,
      'subiculum': 234.567891,
      'CA1': 34.567891,
      'hippocampal-fissure': 345.678912,
      'presubiculum': 456.789123,
      'parasubiculum':  45.678912,
      'molecular_layer_HP': 56.789123,
      'GC-ML-DG': 567.891234,
      'CA3': 678.912345,
      'CA4': 789.123456,
      'fimbria': 89.123456,
      'HATA': 91.234567,
      'Whole_hippocampus': 1234.567899}),
])
def test_read_hippocampal_volumes(volume_file_path, expected_volumes):
    assert expected_volumes == freesurfer_volume_reader.read_hippocampal_volumes(
        volume_file_path)


def test_read_hippocampal_volumes_not_found():
    with pytest.raises(FileNotFoundError):
        freesurfer_volume_reader.read_hippocampal_volumes(
            os.path.join(SUBJECTS_DIR, 'non-existing', 'lh.hippoSfVolumes-T1.v10.txt'))


@pytest.mark.parametrize(('volume_file_path', 'expected_attrs'), [
    ('bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': True, 'analysis_id': None}),
    ('bert/mri/lh.hippoSfVolumes-T1-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': True, 'analysis_id': 'T2'}),
    ('bert/mri/lh.hippoSfVolumes-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': False, 'analysis_id': 'T2'}),
    ('bert/mri/lh.hippoSfVolumes-T1-T2-high-res.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': True, 'analysis_id': 'T2-high-res'}),
    ('bert/mri/lh.hippoSfVolumes-T2-high-res.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': False, 'analysis_id': 'T2-high-res'}),
    ('bert/mri/lh.hippoSfVolumes-PD.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': False, 'analysis_id': 'PD'}),
    ('bert/mri/rh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'T1_input': True, 'analysis_id': None}),
    ('bert/mri/rh.hippoSfVolumes-T1-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'T1_input': True, 'analysis_id': 'T2'}),
    ('freesurfer/subjects/bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': True, 'analysis_id': None}),
    ('../../bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'T1_input': True, 'analysis_id': None}),
])
def test_parse_hippocampal_volume_file_path(volume_file_path, expected_attrs):
    assert expected_attrs == freesurfer_volume_reader.parse_hippocampal_volume_file_path(
        volume_file_path=volume_file_path)


@pytest.mark.parametrize('volume_file_path', [
    'bert/mri/lh.hippoSfLabels-T1.v10.mgz',
    'bert/mri/lh.hippoSfVolumes-T1.v9.txt',
    'bert/mri/lh.hippoSfVolumes.v10.txt',
    'bert/mri/mh.hippoSfVolumes-T1.v10.txt',
])
def test_parse_hippocampal_volume_file_path_invalid(volume_file_path):
    with pytest.raises(Exception):
        freesurfer_volume_reader.parse_hippocampal_volume_file_path(
            volume_file_path=volume_file_path)


@pytest.mark.parametrize(('volume_file_path', 'expected_dataframe'), [
    (os.path.join(SUBJECTS_DIR, 'alice', 'mri', 'lh.hippoSfVolumes-T1.v10.txt'),
     pandas.DataFrame({
         'subfield': ['Hippocampal_tail', 'subiculum', 'CA1', 'hippocampal-fissure',
                      'presubiculum', 'parasubiculum', 'molecular_layer_HP', 'GC-ML-DG',
                      'CA3', 'CA4', 'fimbria', 'HATA', 'Whole_hippocampus'],
         'volume': [173.456789, 734.567891, 34.567891, 345.678917, 456.789173, 45.678917,
                    56.789173, 567.891734, 678.917345, 789.173456, 89.173456, 91.734567,
                    1734.567899],
         'subject': 'alice',
         'hemisphere': 'left',
         'T1_input': True,
         'analysis_id': None,
     })),
])
def test_read_hippocampal_volume_file_dataframe(volume_file_path, expected_dataframe):
    pandas.util.testing.assert_frame_equal(
        left=expected_dataframe,
        right=freesurfer_volume_reader.read_hippocampal_volume_file_dataframe(
            volume_file_path=volume_file_path),
    )


@pytest.mark.parametrize(('root_dir_path', 'expected_csv_path'), [
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
])
def test_main_root_dir_param(capsys, root_dir_path, expected_csv_path):
    with unittest.mock.patch('sys.argv', ['', root_dir_path]):
        freesurfer_volume_reader.main()
    out, _ = capsys.readouterr()
    pandas.util.testing.assert_frame_equal(
        left=pandas.read_csv(expected_csv_path),
        right=pandas.read_csv(io.StringIO(out)).drop(columns=['source_path']),
    )


@pytest.mark.parametrize(('root_dir_path', 'expected_csv_path'), [
    (os.path.join(SUBJECTS_DIR, 'bert'),
     os.path.join(SUBJECTS_DIR, 'bert', 'hippocampal-volumes.csv')),
])
def test_main_root_dir_env(capsys, root_dir_path, expected_csv_path):
    os.environ['SUBJECTS_DIR'] = root_dir_path
    with unittest.mock.patch('sys.argv', ['']):
        freesurfer_volume_reader.main()
    out, _ = capsys.readouterr()
    pandas.util.testing.assert_frame_equal(
        left=pandas.read_csv(expected_csv_path),
        right=pandas.read_csv(io.StringIO(out)).drop(columns=['source_path']),
    )
