import os
import re

import pandas
import pytest

from freesurfer_volume_reader.ashs import HippocampalSubfieldsVolumeFile

from conftest import SUBJECTS_DIR, assert_volume_frames_equal


@pytest.mark.parametrize(('volume_file_path', 'expected_attrs'), [
    ('ashs/final/bert_left_heur_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'correction': None}),
    ('ashs/final/bert_left_corr_nogray_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'correction': 'nogray'}),
    ('ashs/final/bert_left_corr_usegray_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'left', 'correction': 'usegray'}),
    ('ashs/final/bert_right_heur_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': None}),
    ('ashs/final/bert_right_corr_nogray_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': 'nogray'}),
    ('ashs/final/bert_right_corr_usegray_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': 'usegray'}),
    ('somewhere/else/bert_right_heur_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': None}),
    ('somewhere/else/bert_right_corr_nogray_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': 'nogray'}),
    ('bert_right_heur_volumes.txt',
     {'subject': 'bert', 'hemisphere': 'right', 'correction': None}),
    ('/foo/bar/alice_20190503_right_corr_nogray_volumes.txt',
     {'subject': 'alice_20190503', 'hemisphere': 'right', 'correction': 'nogray'}),
])
def test_hippocampal_subfields_volume_file_init(volume_file_path, expected_attrs):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert os.path.abspath(volume_file_path) == volume_file.absolute_path
    for attr, value in expected_attrs.items():
        assert value == getattr(volume_file, attr)


@pytest.mark.parametrize('volume_file_path', [
    'bert_middle_heur_volumes.txt',
    'bert_right_hear_volumes.txt',
    'bert_right_heur_volumes.nii',
    'bert_left_lfseg_corr_usegray.nii.gz',
])
def test_hippocampal_subfields_volume_file_init_invalid(volume_file_path):
    with pytest.raises(Exception):
        HippocampalSubfieldsVolumeFile(path=volume_file_path)


@pytest.mark.parametrize(('volume_file_path', 'expected_volumes'), [
    (os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_nogray_volumes.txt'),
     {'CA1': 678.901,
      'CA2+3': 123.456,
      'DG': 901.234,
      'ERC': 789.012,
      'PHC': 2345.876,
      'PRC': 2345.678,
      'SUB': 457.789}),
])
def test_hippocampal_subfields_volume_file_read_volumes_mm3(volume_file_path, expected_volumes):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert expected_volumes == volume_file.read_volumes_mm3()


def test_hippocampal_subfields_volume_file_read_volumes_mm3_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(SUBJECTS_DIR, 'nobert', 'final', 'bert_left_corr_nogray_volumes.txt'))
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_mm3()


@pytest.mark.parametrize(('volume_file_path', 'expected_dataframe'), [
    (os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_heur_volumes.txt'),
     pandas.DataFrame({
         'subfield': ['CA1', 'CA2+3', 'DG', 'ERC', 'PHC', 'PRC', 'SUB'],
         'volume_mm^3': [679.904, 124.459, 902.237, 789.012, 2346.879, 2346.671, 458.782],
         'subject': 'alice',
         'hemisphere': 'left',
         'correction': None,
     })),
])
def test_hippocampal_subfields_volume_file_read_volumes_dataframe(
        volume_file_path: str, expected_dataframe: pandas.DataFrame):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert_volume_frames_equal(left=expected_dataframe,
                               right=volume_file.read_volumes_dataframe())


def test_hippocampal_subfields_volume_file_read_volumes_dataframe_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(SUBJECTS_DIR, 'nobert', 'final', 'bert_left_corr_nogray_volumes.txt'))
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_dataframe()


@pytest.mark.parametrize(('root_dir_path', 'expected_file_paths'), [
    (os.path.join(SUBJECTS_DIR, 'alice'),
     {os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_heur_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_corr_nogray_volumes.txt')}),
    (os.path.join(SUBJECTS_DIR, 'bert'),
     {os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_nogray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_usegray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_heur_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_right_corr_nogray_volumes.txt')}),
    (SUBJECTS_DIR,
     {os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_heur_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_corr_nogray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_nogray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_usegray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_heur_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_right_corr_nogray_volumes.txt')}),
])
def test_hippocampal_subfields_volume_file_find(root_dir_path, expected_file_paths):
    volume_files_iterator = HippocampalSubfieldsVolumeFile.find(root_dir_path=root_dir_path)
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)


@pytest.mark.parametrize(('root_dir_path', 'filename_pattern', 'expected_file_paths'), [
    (SUBJECTS_DIR,
     r'^bert_right_',
     {os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_right_corr_nogray_volumes.txt')}),
    (SUBJECTS_DIR,
     r'_nogray_volumes.txt$',
     {os.path.join(SUBJECTS_DIR, 'alice', 'final', 'alice_left_corr_nogray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_left_corr_nogray_volumes.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'final', 'bert_right_corr_nogray_volumes.txt')}),
])
def test_hippocampal_subfields_volume_file_find_pattern(root_dir_path, filename_pattern,
                                                        expected_file_paths):
    volume_files_iterator = HippocampalSubfieldsVolumeFile.find(
        root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern))
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)
