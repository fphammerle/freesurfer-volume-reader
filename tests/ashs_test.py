# pylint: disable=missing-module-docstring

import os
import re

import pandas
import pytest

from freesurfer_volume_reader.ashs import (
    IntracranialVolumeFile,
    HippocampalSubfieldsVolumeFile,
)

from conftest import SUBJECTS_DIR, assert_volume_frames_equal


@pytest.mark.parametrize(
    ("volume_file_path", "expected_subject"),
    [
        ("bert_icv.txt", "bert"),
        ("final/bert_icv.txt", "bert"),
        ("ashs/subjects/bert/final/bert_icv.txt", "bert"),
        (
            "ashs/subjects/alice/final/long_subject_name_42_icv.txt",
            "long_subject_name_42",
        ),
    ],
)
def test_intracranial_volume_file_init(volume_file_path, expected_subject):
    volume_file = IntracranialVolumeFile(path=volume_file_path)
    assert os.path.abspath(volume_file_path) == volume_file.absolute_path
    assert expected_subject == volume_file.subject


@pytest.mark.parametrize(
    "volume_file_path", ["_icv.txt", "bert_ICV.txt", "bert_icv.csv", "bert_ICV.txt.zip"]
)
def test_intracranial_volume_file_init_invalid_filename(volume_file_path):
    with pytest.raises(Exception):
        IntracranialVolumeFile(path=volume_file_path)


@pytest.mark.parametrize(
    ("volume_file_path", "expected_volume"),
    [
        (os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"), 1234560),
        (os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"), 1.23456e06),
        (os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"), 1.23456e06),
        (
            os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"),
            float("1.23456e+06"),
        ),
        (os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt"), 1543200),
    ],
)
def test_intracranial_volume_file_read_volume_mm3(volume_file_path, expected_volume):
    volume_file = IntracranialVolumeFile(path=volume_file_path)
    assert expected_volume == pytest.approx(volume_file.read_volume_mm3())


@pytest.mark.parametrize(
    "volume_file_path", [os.path.join(SUBJECTS_DIR, "noone", "final", "noone_icv.txt")]
)
def test_intracranial_volume_file_read_volume_mm3_not_found(volume_file_path):
    volume_file = IntracranialVolumeFile(path=volume_file_path)
    with pytest.raises(FileNotFoundError):
        volume_file.read_volume_mm3()


@pytest.mark.parametrize(
    ("volume_file_path", "expected_series"),
    [
        (
            os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"),
            pandas.Series(
                data=[1234560.0],
                name="intercranial_volume_mm^3",
                index=pandas.Index(data=["bert"], name="subject"),
            ),
        ),
        (
            os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt"),
            pandas.Series(
                data=[1543200.0],
                name="intercranial_volume_mm^3",
                index=pandas.Index(data=["alice"], name="subject"),
            ),
        ),
    ],
)
def test_intracranial_volume_file_read_volume_series_single(
    volume_file_path, expected_series
):
    volume_file = IntracranialVolumeFile(path=volume_file_path)
    pandas.testing.assert_series_equal(
        left=expected_series,
        right=volume_file.read_volume_series(),
        check_dtype=True,
        check_names=True,
    )


@pytest.mark.parametrize(
    ("volume_file_paths", "expected_series"),
    [
        (
            [
                os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"),
                os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt"),
            ],
            pandas.Series(
                data=[1234560.0, 1543200.0],
                name="intercranial_volume_mm^3",
                index=pandas.Index(data=["bert", "alice"], name="subject"),
            ),
        )
    ],
)
def test_intracranial_volume_file_read_volume_series_concat(
    volume_file_paths, expected_series
):
    volume_series = pandas.concat(
        IntracranialVolumeFile(path=p).read_volume_series() for p in volume_file_paths
    )
    pandas.testing.assert_series_equal(
        left=expected_series, right=volume_series, check_dtype=True, check_names=True
    )


@pytest.mark.parametrize(
    "volume_file_path", [os.path.join(SUBJECTS_DIR, "bert", "final", "BERT_icv.txt")]
)
def test_intracranial_volume_file_read_volume_series_not_found(volume_file_path):
    volume_file = IntracranialVolumeFile(path=volume_file_path)
    with pytest.raises(FileNotFoundError):
        volume_file.read_volume_series()


@pytest.mark.parametrize(
    ("root_dir_path", "expected_file_paths"),
    [
        (
            os.path.join(SUBJECTS_DIR, "bert"),
            {os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt")},
        ),
        (
            os.path.join(SUBJECTS_DIR, "alice"),
            {os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt")},
        ),
        (
            SUBJECTS_DIR,
            {
                os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt"),
                os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"),
            },
        ),
    ],
)
def test_intracranial_volume_file_find(root_dir_path, expected_file_paths):
    volume_files_iterator = IntracranialVolumeFile.find(root_dir_path=root_dir_path)
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)


@pytest.mark.parametrize(
    ("root_dir_path", "filename_pattern", "expected_file_paths"),
    [
        (
            SUBJECTS_DIR,
            r"^\w{4,6}_icv.txt$",
            {
                os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt"),
                os.path.join(SUBJECTS_DIR, "bert", "final", "bert_icv.txt"),
            },
        ),
        (
            SUBJECTS_DIR,
            r"^\w{5,6}_icv.txt$",
            {os.path.join(SUBJECTS_DIR, "alice", "final", "alice_icv.txt")},
        ),
        (SUBJECTS_DIR, r"^\w{7,}_icv.txt$", set()),
    ],
)
def test_intracranial_volume_file_find_pattern(
    root_dir_path, filename_pattern, expected_file_paths
):
    volume_files_iterator = IntracranialVolumeFile.find(
        root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)
    )
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)


@pytest.mark.parametrize(
    ("volume_file_path", "expected_attrs"),
    [
        (
            "ashs/final/bert_left_heur_volumes.txt",
            {"subject": "bert", "hemisphere": "left", "correction": None},
        ),
        (
            "ashs/final/bert_left_corr_nogray_volumes.txt",
            {"subject": "bert", "hemisphere": "left", "correction": "nogray"},
        ),
        (
            "ashs/final/bert_left_corr_usegray_volumes.txt",
            {"subject": "bert", "hemisphere": "left", "correction": "usegray"},
        ),
        (
            "ashs/final/bert_right_heur_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": None},
        ),
        (
            "ashs/final/bert_right_corr_nogray_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": "nogray"},
        ),
        (
            "ashs/final/bert_right_corr_usegray_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": "usegray"},
        ),
        (
            "somewhere/else/bert_right_heur_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": None},
        ),
        (
            "somewhere/else/bert_right_corr_nogray_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": "nogray"},
        ),
        (
            "bert_right_heur_volumes.txt",
            {"subject": "bert", "hemisphere": "right", "correction": None},
        ),
        (
            "/foo/bar/alice_20190503_right_corr_nogray_volumes.txt",
            {
                "subject": "alice_20190503",
                "hemisphere": "right",
                "correction": "nogray",
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_init(volume_file_path, expected_attrs):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert os.path.abspath(volume_file_path) == volume_file.absolute_path
    for attr, value in expected_attrs.items():
        assert value == getattr(volume_file, attr)


@pytest.mark.parametrize(
    "volume_file_path",
    [
        "bert_middle_heur_volumes.txt",
        "bert_right_hear_volumes.txt",
        "bert_right_heur_volumes.nii",
        "bert_left_lfseg_corr_usegray.nii.gz",
    ],
)
def test_hippocampal_subfields_volume_file_init_invalid(volume_file_path):
    with pytest.raises(Exception):
        HippocampalSubfieldsVolumeFile(path=volume_file_path)


@pytest.mark.parametrize(
    ("volume_file_path", "expected_volumes"),
    [
        (
            os.path.join(
                SUBJECTS_DIR, "bert", "final", "bert_left_corr_nogray_volumes.txt"
            ),
            {
                "CA1": 678.901,
                "CA2+3": 123.456,
                "DG": 901.234,
                "ERC": 789.012,
                "PHC": 2345.876,
                "PRC": 2345.678,
                "SUB": 457.789,
            },
        )
    ],
)
def test_hippocampal_subfields_volume_file_read_volumes_mm3(
    volume_file_path, expected_volumes
):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert expected_volumes == volume_file.read_volumes_mm3()


def test_hippocampal_subfields_volume_file_read_volumes_mm3_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(
            SUBJECTS_DIR, "nobert", "final", "bert_left_corr_nogray_volumes.txt"
        )
    )
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_mm3()


@pytest.mark.parametrize(
    ("volume_file_path", "expected_dataframe"),
    [
        (
            os.path.join(SUBJECTS_DIR, "alice", "final", "alice_left_heur_volumes.txt"),
            pandas.DataFrame(
                {
                    "subfield": ["CA1", "CA2+3", "DG", "ERC", "PHC", "PRC", "SUB"],
                    "volume_mm^3": [
                        679.904,
                        124.459,
                        902.237,
                        789.012,
                        2346.879,
                        2346.671,
                        458.782,
                    ],
                    "subject": "alice",
                    "hemisphere": "left",
                    "correction": None,
                }
            ),
        )
    ],
)
def test_hippocampal_subfields_volume_file_read_volumes_dataframe(
    volume_file_path: str, expected_dataframe: pandas.DataFrame
):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert_volume_frames_equal(
        left=expected_dataframe, right=volume_file.read_volumes_dataframe()
    )


def test_hippocampal_subfields_volume_file_read_volumes_dataframe_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(
            SUBJECTS_DIR, "nobert", "final", "bert_left_corr_nogray_volumes.txt"
        )
    )
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_dataframe()


@pytest.mark.parametrize(
    ("root_dir_path", "expected_file_paths"),
    [
        (
            os.path.join(SUBJECTS_DIR, "alice"),
            {
                os.path.join(
                    SUBJECTS_DIR, "alice", "final", "alice_left_heur_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "alice", "final", "alice_left_corr_nogray_volumes.txt"
                ),
            },
        ),
        (
            os.path.join(SUBJECTS_DIR, "bert"),
            {
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_corr_nogray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_corr_usegray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_heur_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_right_corr_nogray_volumes.txt"
                ),
            },
        ),
        (
            SUBJECTS_DIR,
            {
                os.path.join(
                    SUBJECTS_DIR, "alice", "final", "alice_left_heur_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "alice", "final", "alice_left_corr_nogray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_corr_nogray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_corr_usegray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_heur_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_right_corr_nogray_volumes.txt"
                ),
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_find(root_dir_path, expected_file_paths):
    volume_files_iterator = HippocampalSubfieldsVolumeFile.find(
        root_dir_path=root_dir_path
    )
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)


@pytest.mark.parametrize(
    ("root_dir_path", "filename_pattern", "expected_file_paths"),
    [
        (
            SUBJECTS_DIR,
            r"^bert_right_",
            {
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_right_corr_nogray_volumes.txt"
                )
            },
        ),
        (
            SUBJECTS_DIR,
            r"_nogray_volumes.txt$",
            {
                os.path.join(
                    SUBJECTS_DIR, "alice", "final", "alice_left_corr_nogray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_left_corr_nogray_volumes.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "final", "bert_right_corr_nogray_volumes.txt"
                ),
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_find_pattern(
    root_dir_path, filename_pattern, expected_file_paths
):
    volume_files_iterator = HippocampalSubfieldsVolumeFile.find(
        root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)
    )
    assert expected_file_paths == set(f.absolute_path for f in volume_files_iterator)
