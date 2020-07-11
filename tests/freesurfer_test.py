# pylint: disable=missing-module-docstring

import os
import re

import pandas
import pytest

from freesurfer_volume_reader.freesurfer import HippocampalSubfieldsVolumeFile

from conftest import SUBJECTS_DIR, assert_volume_frames_equal


@pytest.mark.parametrize(
    ("volume_file_path", "expected_attrs"),
    [
        (
            "bert/mri/lh.hippoSfVolumes-T1.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": True,
                "analysis_id": None,
            },
        ),
        (
            "bert/mri/lh.hippoSfVolumes-T1-T2.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": True,
                "analysis_id": "T2",
            },
        ),
        (
            "bert/mri/lh.hippoSfVolumes-T2.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": False,
                "analysis_id": "T2",
            },
        ),
        (
            "bert/mri/lh.hippoSfVolumes-T1-T2-high-res.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": True,
                "analysis_id": "T2-high-res",
            },
        ),
        (
            "bert/mri/lh.hippoSfVolumes-T2-high-res.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": False,
                "analysis_id": "T2-high-res",
            },
        ),
        (
            "bert/mri/lh.hippoSfVolumes-PD.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": False,
                "analysis_id": "PD",
            },
        ),
        (
            "bert/mri/rh.hippoSfVolumes-T1.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "right",
                "t1_input": True,
                "analysis_id": None,
            },
        ),
        (
            "bert/mri/rh.hippoSfVolumes-T1-T2.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "right",
                "t1_input": True,
                "analysis_id": "T2",
            },
        ),
        (
            "freesurfer/subjects/bert/mri/lh.hippoSfVolumes-T1.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": True,
                "analysis_id": None,
            },
        ),
        (
            "../../bert/mri/lh.hippoSfVolumes-T1.v10.txt",
            {
                "subject": "bert",
                "hemisphere": "left",
                "t1_input": True,
                "analysis_id": None,
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_init(volume_file_path, expected_attrs):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert os.path.basename(volume_file_path) == os.path.basename(
        volume_file.absolute_path
    )
    for attr, value in expected_attrs.items():
        assert value == getattr(volume_file, attr)


@pytest.mark.parametrize(
    "volume_file_path",
    [
        "bert/mri/lh.hippoSfLabels-T1.v10.mgz",
        "bert/mri/lh.hippoSfVolumes-T1.v9.txt",
        "bert/mri/lh.hippoSfVolumes.v10.txt",
        "bert/mri/mh.hippoSfVolumes-T1.v10.txt",
        "bert_left_corr_nogray_volumes.txt",
    ],
)
def test_hippocampal_subfields_volume_file_init_invalid_path(volume_file_path):
    with pytest.raises(Exception):
        HippocampalSubfieldsVolumeFile(path=volume_file_path)


@pytest.mark.parametrize(
    ("volume_file_path", "expected_volumes"),
    [
        (
            os.path.join(SUBJECTS_DIR, "bert/mri/lh.hippoSfVolumes-T1.v10.txt"),
            {
                "Hippocampal_tail": 123.456789,
                "subiculum": 234.567891,
                "CA1": 34.567891,
                "hippocampal-fissure": 345.678912,
                "presubiculum": 456.789123,
                "parasubiculum": 45.678912,
                "molecular_layer_HP": 56.789123,
                "GC-ML-DG": 567.891234,
                "CA3": 678.912345,
                "CA4": 789.123456,
                "fimbria": 89.123456,
                "HATA": 91.234567,
                "Whole_hippocampus": 1234.567899,
            },
        )
    ],
)
def test_hippocampal_subfields_volume_file_read_volumes_mm3(
    volume_file_path, expected_volumes
):
    volume_file = HippocampalSubfieldsVolumeFile(path=volume_file_path)
    assert volume_file.t1_input
    assert expected_volumes == volume_file.read_volumes_mm3()


def test_hippocampal_subfields_volume_file_read_volumes_mm3_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(SUBJECTS_DIR, "non-existing", "lh.hippoSfVolumes-T1.v10.txt")
    )
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_mm3()


@pytest.mark.parametrize(
    ("volume_file_path", "expected_dataframe"),
    [
        (
            os.path.join(SUBJECTS_DIR, "alice", "mri", "lh.hippoSfVolumes-T1.v10.txt"),
            pandas.DataFrame(
                {
                    "subfield": [
                        "Hippocampal_tail",
                        "subiculum",
                        "CA1",
                        "hippocampal-fissure",
                        "presubiculum",
                        "parasubiculum",
                        "molecular_layer_HP",
                        "GC-ML-DG",
                        "CA3",
                        "CA4",
                        "fimbria",
                        "HATA",
                        "Whole_hippocampus",
                    ],
                    "volume_mm^3": [
                        173.456789,
                        734.567891,
                        34.567891,
                        345.678917,
                        456.789173,
                        45.678917,
                        56.789173,
                        567.891734,
                        678.917345,
                        789.173456,
                        89.173456,
                        91.734567,
                        1734.567899,
                    ],
                    "subject": "alice",
                    "hemisphere": "left",
                    "T1_input": True,
                    "analysis_id": None,
                }
            ),
        )
    ],
)
def test_hippocampal_subfields_volume_file_read_volumes_dataframe(
    volume_file_path: str, expected_dataframe: pandas.DataFrame
):
    assert_volume_frames_equal(
        left=expected_dataframe,
        right=HippocampalSubfieldsVolumeFile(
            path=volume_file_path
        ).read_volumes_dataframe(),
    )


def test_hippocampal_subfields_volume_file_read_volumes_dataframe_not_found():
    volume_file = HippocampalSubfieldsVolumeFile(
        path=os.path.join(SUBJECTS_DIR, "non-existing", "lh.hippoSfVolumes-T1.v10.txt")
    )
    with pytest.raises(FileNotFoundError):
        volume_file.read_volumes_dataframe()


@pytest.mark.parametrize(
    ("root_dir_path", "expected_file_paths"),
    [
        (
            SUBJECTS_DIR,
            {
                os.path.join(
                    SUBJECTS_DIR, "alice", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1-T2.v10.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
            },
        ),
        (
            os.path.join(SUBJECTS_DIR, "bert"),
            {
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1-T2.v10.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
            },
        ),
        (
            os.path.join(SUBJECTS_DIR, "bert", "mri"),
            {
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1-T2.v10.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_find(root_dir_path, expected_file_paths):
    volume_files = list(
        HippocampalSubfieldsVolumeFile.find(root_dir_path=root_dir_path)
    )
    assert all(
        "hippoSfVolumes" in os.path.basename(f.absolute_path) for f in volume_files
    )
    assert expected_file_paths == set(f.absolute_path for f in volume_files)


@pytest.mark.parametrize(
    ("root_dir_path", "filename_pattern", "expected_file_paths"),
    [
        (
            SUBJECTS_DIR,
            r"hippoSfVolumes-T1\.v10",
            {
                os.path.join(
                    SUBJECTS_DIR, "alice", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1.v10.txt"
                ),
            },
        ),
        (
            os.path.join(SUBJECTS_DIR, "bert"),
            r"hippoSfVolumes-T1-T2",
            {
                os.path.join(
                    SUBJECTS_DIR, "bert", "mri", "lh.hippoSfVolumes-T1-T2.v10.txt"
                )
            },
        ),
    ],
)
def test_hippocampal_subfields_volume_file_find_pattern(
    root_dir_path, filename_pattern, expected_file_paths
):
    assert expected_file_paths == set(
        f.absolute_path
        for f in HippocampalSubfieldsVolumeFile.find(
            root_dir_path=root_dir_path, filename_regex=re.compile(filename_pattern)
        )
    )
