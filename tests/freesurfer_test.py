import os
import re

import pytest

from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile

SUBJECTS_DIR = os.path.join(os.path.dirname(__file__), 'subjects')


@pytest.mark.parametrize(('volume_file_path', 'expected_attrs'), [
    ('bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': True, 'analysis_id': None}),
    ('bert/mri/lh.hippoSfVolumes-T1-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': True, 'analysis_id': 'T2'}),
    ('bert/mri/lh.hippoSfVolumes-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': False, 'analysis_id': 'T2'}),
    ('bert/mri/lh.hippoSfVolumes-T1-T2-high-res.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': True, 'analysis_id': 'T2-high-res'}),
    ('bert/mri/lh.hippoSfVolumes-T2-high-res.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': False, 'analysis_id': 'T2-high-res'}),
    ('bert/mri/lh.hippoSfVolumes-PD.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': False, 'analysis_id': 'PD'}),
    ('bert/mri/rh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'right', 't1_input': True, 'analysis_id': None}),
    ('bert/mri/rh.hippoSfVolumes-T1-T2.v10.txt',
     {'subject': 'bert', 'hemisphere': 'right', 't1_input': True, 'analysis_id': 'T2'}),
    ('freesurfer/subjects/bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': True, 'analysis_id': None}),
    ('../../bert/mri/lh.hippoSfVolumes-T1.v10.txt',
     {'subject': 'bert', 'hemisphere': 'left', 't1_input': True, 'analysis_id': None}),
])
def test_hippocampal_subfields_volume_file_init(volume_file_path, expected_attrs):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert os.path.basename(volume_file_path) == os.path.basename(volume_file.absolute_path)
    for attr, value in expected_attrs.items():
        assert value == getattr(volume_file, attr)


@pytest.mark.parametrize('volume_file_path', [
    'bert/mri/lh.hippoSfLabels-T1.v10.mgz',
    'bert/mri/lh.hippoSfVolumes-T1.v9.txt',
    'bert/mri/lh.hippoSfVolumes.v10.txt',
    'bert/mri/mh.hippoSfVolumes-T1.v10.txt',
])
def test_hippocampal_subfields_volume_file_init_invalid(volume_file_path):
    with pytest.raises(Exception):
        HippocampalSubfieldsVolumeFile(path=volume_file_path)


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
def test_hippocampal_subfields_volume_file_find(root_dir_path, expected_file_paths):
    volume_files_iterator = HippocampalSubfieldsVolumeFile.find(root_dir_path=root_dir_path)
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)


@pytest.mark.parametrize(('root_dir_path', 'filename_pattern', 'expected_file_paths'), [
    (SUBJECTS_DIR,
     r'hippoSfVolumes-T1\.v10',
     {os.path.join(SUBJECTS_DIR, 'alice', 'mri', 'lh.hippoSfVolumes-T1.v10.txt'),
      os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1.v10.txt')}),
    (os.path.join(SUBJECTS_DIR, 'bert'),
     r'hippoSfVolumes-T1-T2',
     {os.path.join(SUBJECTS_DIR, 'bert', 'mri', 'lh.hippoSfVolumes-T1-T2.v10.txt')}),
])
def test_hippocampal_subfields_volume_file_find_pattern(root_dir_path, filename_pattern,
                                                        expected_file_paths):
    assert expected_file_paths == set(
        f.absolute_path for f in HippocampalSubfieldsVolumeFile.find(
            root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)))
