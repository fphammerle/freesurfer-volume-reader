# pylint: disable=missing-module-docstring

import pytest

from freesurfer_volume_reader import (
    SubfieldVolumeFile,
    VolumeFile,
    __version__,
    parse_version_string,
    remove_group_names_from_regex,
)


def test_module_version():
    assert len(__version__) >= len("0.1.0")


@pytest.mark.filterwarnings("ignore:function `parse_version_string` is deprecated")
@pytest.mark.parametrize(
    ("version_string", "expected_tuple"),
    [
        ("0.24.2", (0, 24, 2)),
        ("0.21.0", (0, 21, 0)),
        ("0.2.2.dev28+g526f05c.d20190504", (0, 2, 2, "dev28+g526f05c", "d20190504")),
    ],
)
def test_parse_version_string(version_string, expected_tuple):
    assert expected_tuple == parse_version_string(version_string)


@pytest.mark.filterwarnings("ignore:function `parse_version_string` is deprecated")
def test_parse_version_string_comparison():
    assert parse_version_string("0.24.2") == (0, 24, 2)
    assert parse_version_string("0.24.2") < (0, 25)
    assert parse_version_string("0.24.2") < (0, 24, 3)
    assert parse_version_string("0.24.2") <= (0, 24, 2)
    assert parse_version_string("0.24.2") >= (0, 24, 2)
    assert parse_version_string("0.24.2") > (0, 24, 1)
    assert parse_version_string("0.24.2") > (0, 24)
    assert parse_version_string("0.2.2.dev28+g526f05c.d20190504") > (0, 2, 2)
    assert parse_version_string("0.2.2.dev28+g526f05c.d20190504") < (0, 2, 3)


@pytest.mark.parametrize(
    ("source_pattern", "expected_pattern"),
    [
        (r"^(?P<h>[lr])h\.hippoSfVolumes", r"^([lr])h\.hippoSfVolumes"),
        (r"(?P<a>a(?P<b>b))", r"(a(b))"),
    ],
)
def test_remove_group_names_from_regex(source_pattern, expected_pattern):
    assert expected_pattern == remove_group_names_from_regex(
        regex_pattern=source_pattern
    )


def test_volume_file_abstract():
    with pytest.raises(
        TypeError,
        match=r"^Can't instantiate abstract class VolumeFile with abstract methods? __init__$",
    ):
        VolumeFile(path="/tmp/test")  # pylint: disable=abstract-class-instantiated


class DummyVolumeFile(VolumeFile):

    # pylint: disable=useless-super-delegation

    def __init__(self, path: str) -> None:
        super().__init__(path=path)


class DummySubfieldVolumeFile(SubfieldVolumeFile):

    # pylint: disable=useless-super-delegation

    def __init__(self, path: str) -> None:
        super().__init__(path=path)

    def read_volumes_mm3(self):
        return super().read_volumes_mm3()

    def read_volumes_dataframe(self):
        return super().read_volumes_dataframe()


def test_subfield_volume_file_abstractmethod():
    volume_file = DummySubfieldVolumeFile(path="subfield-dummy")
    with pytest.raises(NotImplementedError):
        volume_file.read_volumes_mm3()
    with pytest.raises(NotImplementedError):
        volume_file.read_volumes_dataframe()
