import os
import re

import pytest

from freesurfer_volume_reader.freesurfer import FreesurferHippocampalVolumeFile

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
        FreesurferHippocampalVolumeFile.find(root_dir_path=root_dir_path))


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
    assert expected_file_paths == set(FreesurferHippocampalVolumeFile.find(
        root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)))
