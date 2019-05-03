import os

import pytest

from freesurfer_volume_reader.ashs import HippocampalSubfieldsVolumeFile


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
    assert os.path.basename(volume_file_path) == os.path.basename(volume_file.absolute_path)
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
