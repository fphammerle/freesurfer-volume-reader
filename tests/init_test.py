import pytest

from freesurfer_volume_reader import parse_version_string, remove_group_names_from_regex


@pytest.mark.parametrize(('version_string', 'expected_tuple'), [
    ('0.24.2', (0, 24, 2)),
    ('0.21.0', (0, 21, 0)),
    ('0.2.2.dev28+g526f05c.d20190504', (0, 2, 2, 'dev28+g526f05c', 'd20190504')),
])
def test_parse_version_string(version_string, expected_tuple):
    assert expected_tuple == parse_version_string(version_string)


def test_parse_version_string_comparison():
    assert parse_version_string('0.24.2') == (0, 24, 2)
    assert parse_version_string('0.24.2') < (0, 25)
    assert parse_version_string('0.24.2') < (0, 24, 3)
    assert parse_version_string('0.24.2') <= (0, 24, 2)
    assert parse_version_string('0.24.2') >= (0, 24, 2)
    assert parse_version_string('0.24.2') > (0, 24, 1)
    assert parse_version_string('0.24.2') > (0, 24)
    assert parse_version_string('0.2.2.dev28+g526f05c.d20190504') > (0, 2, 2)
    assert parse_version_string('0.2.2.dev28+g526f05c.d20190504') < (0, 2, 3)


@pytest.mark.parametrize(('source_pattern', 'expected_pattern'), [
    (r'^(?P<h>[lr])h\.hippoSfVolumes', r'^([lr])h\.hippoSfVolumes'),
    (r'(?P<a>a(?P<b>b))', r'(a(b))'),
])
def test_remove_group_names_from_regex(source_pattern, expected_pattern):
    assert expected_pattern == remove_group_names_from_regex(regex_pattern=source_pattern)
