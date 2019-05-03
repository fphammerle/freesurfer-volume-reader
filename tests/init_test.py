import pytest

import freesurfer_volume_reader


@pytest.mark.parametrize(('source_pattern', 'expected_pattern'), [
    (r'^(?P<h>[lr])h\.hippoSfVolumes', r'^([lr])h\.hippoSfVolumes'),
    (r'(?P<a>a(?P<b>b))', r'(a(b))'),
])
def test_remove_group_names_from_regex(source_pattern, expected_pattern):
    assert expected_pattern == freesurfer_volume_reader.remove_group_names_from_regex(
        regex_pattern=source_pattern,
    )
