# pylint: disable=missing-module-docstring

import io
import os
import subprocess
import typing
import unittest.mock

import pandas
import pandas.util.testing
import pytest

import freesurfer_volume_reader
import freesurfer_volume_reader.__main__

from conftest import SUBJECTS_DIR, assert_volume_frames_equal


def assert_main_volume_frame_equals(
    capsys,
    argv: list,
    expected_frame: pandas.DataFrame,
    subjects_dir: typing.Optional[str] = None,
):
    if subjects_dir:
        os.environ["SUBJECTS_DIR"] = subjects_dir
    elif "SUBJECTS_DIR" in os.environ:
        del os.environ["SUBJECTS_DIR"]
    with unittest.mock.patch("sys.argv", [""] + argv):
        assert freesurfer_volume_reader.__main__.main() == 0
    out, _ = capsys.readouterr()
    resulted_frame = pandas.read_csv(io.StringIO(out)).drop(columns=["source_path"])
    if "correction" in resulted_frame:
        resulted_frame["correction"] = resulted_frame["correction"].astype("object")
    assert_volume_frames_equal(
        left=expected_frame,
        # pandas.DataFrame.drop(columns=[...], ...) >= pandas0.21.0
        right=resulted_frame,
    )


@pytest.mark.parametrize(
    ("args", "root_dir_paths", "expected_csv_path"),
    [
        (
            [],
            [os.path.join(SUBJECTS_DIR, "alice")],
            os.path.join(SUBJECTS_DIR, "alice", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            [],
            [os.path.join(SUBJECTS_DIR, "bert")],
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            [],
            [os.path.join(SUBJECTS_DIR, "alice"), os.path.join(SUBJECTS_DIR, "bert")],
            os.path.join(SUBJECTS_DIR, "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            [],
            [SUBJECTS_DIR],
            os.path.join(SUBJECTS_DIR, "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf"],
            [os.path.join(SUBJECTS_DIR, "alice")],
            os.path.join(SUBJECTS_DIR, "alice", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf"],
            [SUBJECTS_DIR],
            os.path.join(SUBJECTS_DIR, "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            [os.path.join(SUBJECTS_DIR, "alice")],
            os.path.join(SUBJECTS_DIR, "alice", "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            [os.path.join(SUBJECTS_DIR, "bert")],
            os.path.join(SUBJECTS_DIR, "bert", "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            [os.path.join(SUBJECTS_DIR, "alice"), os.path.join(SUBJECTS_DIR, "bert")],
            os.path.join(SUBJECTS_DIR, "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            [SUBJECTS_DIR],
            os.path.join(SUBJECTS_DIR, "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs", "freesurfer-hipposf"],
            [os.path.join(SUBJECTS_DIR, "alice")],
            os.path.join(SUBJECTS_DIR, "alice", "all-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf", "ashs"],
            [os.path.join(SUBJECTS_DIR, "alice")],
            os.path.join(SUBJECTS_DIR, "alice", "all-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs", "freesurfer-hipposf"],
            [os.path.join(SUBJECTS_DIR, "alice"), os.path.join(SUBJECTS_DIR, "bert")],
            os.path.join(SUBJECTS_DIR, "all-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs", "freesurfer-hipposf"],
            [SUBJECTS_DIR],
            os.path.join(SUBJECTS_DIR, "all-hippocampal-volumes.csv"),
        ),
    ],
)
def test_main_root_dir_param(capsys, args, root_dir_paths: list, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=args + ["--"] + root_dir_paths,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


@pytest.mark.parametrize(
    ("args", "root_dir_path", "expected_csv_path"),
    [
        (
            [],
            SUBJECTS_DIR,
            os.path.join(SUBJECTS_DIR, "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            [],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf"],
            SUBJECTS_DIR,
            os.path.join(SUBJECTS_DIR, "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf"],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf"],
            os.path.join(SUBJECTS_DIR, "bert", "mri"),
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            SUBJECTS_DIR,
            os.path.join(SUBJECTS_DIR, "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.join(SUBJECTS_DIR, "bert", "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            os.path.join(SUBJECTS_DIR, "bert", "final"),
            os.path.join(SUBJECTS_DIR, "bert", "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            os.path.join(SUBJECTS_DIR, "alice"),
            os.path.join(SUBJECTS_DIR, "alice", "ashs-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs", "freesurfer-hipposf"],
            os.path.join(SUBJECTS_DIR, "alice"),
            os.path.join(SUBJECTS_DIR, "alice", "all-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf", "ashs"],
            os.path.join(SUBJECTS_DIR, "alice"),
            os.path.join(SUBJECTS_DIR, "alice", "all-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "freesurfer-hipposf", "ashs"],
            SUBJECTS_DIR,
            os.path.join(SUBJECTS_DIR, "all-hippocampal-volumes.csv"),
        ),
    ],
)
def test_main_root_dir_env(capsys, args, root_dir_path, expected_csv_path):
    assert_main_volume_frame_equals(
        argv=args,
        subjects_dir=root_dir_path,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


@pytest.mark.timeout(8)
@pytest.mark.parametrize(
    ("args", "root_dir_path", "subjects_dir", "expected_csv_path"),
    [
        (
            [],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.join(SUBJECTS_DIR, "alice"),
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
        (
            ["--source-types", "ashs"],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.join(SUBJECTS_DIR, "alice"),
            os.path.join(SUBJECTS_DIR, "bert", "ashs-hippocampal-volumes.csv"),
        ),
        (
            [],
            os.path.join(SUBJECTS_DIR, "bert"),
            os.path.abspath(os.sep),
            os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv"),
        ),
    ],
)
def test_main_root_dir_overwrite_env(
    capsys, args, root_dir_path, subjects_dir, expected_csv_path
):
    assert_main_volume_frame_equals(
        argv=args + ["--", root_dir_path],
        subjects_dir=subjects_dir,
        expected_frame=pandas.read_csv(expected_csv_path),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex_freesurfer(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, "bert", "freesurfer-hippocampal-volumes.csv")
    )
    assert_main_volume_frame_equals(
        argv=[
            "--freesurfer-hipposf-filename-regex",
            r"^.*-T1-T2\.v10\.txt$",
            os.path.join(SUBJECTS_DIR, "bert"),
        ],
        expected_frame=expected_volume_frame[
            expected_volume_frame["analysis_id"] == "T2"
        ].copy(),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex_ashs(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, "bert", "ashs-hippocampal-volumes.csv")
    )
    assert_main_volume_frame_equals(
        argv=[
            "--ashs-filename-regex",
            r"_nogray_volumes.txt$",
            "--source-types",
            "ashs",
            "--",
            os.path.join(SUBJECTS_DIR, "bert"),
        ],
        expected_frame=expected_volume_frame[
            expected_volume_frame["correction"] == "nogray"
        ].copy(),
        capsys=capsys,
    )


def test_main_root_dir_filename_regex_combined(capsys):
    expected_volume_frame = pandas.read_csv(
        os.path.join(SUBJECTS_DIR, "alice", "all-hippocampal-volumes.csv")
    )
    expected_volume_frame = expected_volume_frame[
        # pylint: disable=singleton-comparison
        (expected_volume_frame["T1_input"] == True)
        | (
            (expected_volume_frame["source_type"] == "ashs")
            & expected_volume_frame["correction"].isnull()
        )
    ]
    assert_main_volume_frame_equals(
        argv=[
            "--ashs-filename-regex",
            r"^alice_left_heur_",
            "--freesurfer-hipposf-filename-regex",
            r"hippoSfVolumes-T1.v10.txt$",
            "--source-types",
            "ashs",
            "freesurfer-hipposf",
            "--",
            os.path.join(SUBJECTS_DIR, "alice"),
        ],
        expected_frame=expected_volume_frame.copy(),
        capsys=capsys,
    )


def test_main_no_files_found(capsys):
    with unittest.mock.patch(
        "sys.argv",
        ["", "--freesurfer-hipposf-filename-regex", r"^21$", "--", SUBJECTS_DIR],
    ):
        assert os.EX_NOINPUT == freesurfer_volume_reader.__main__.main()
    out, err = capsys.readouterr()
    assert not out
    assert err == "Did not find any volume files matching the specified criteria.\n"


def test_main_module_script_no_files_found():
    proc_info = subprocess.run(
        [
            "python",
            "-m",
            "freesurfer_volume_reader",
            "--freesurfer-hipposf-filename-regex",
            r"^21$",
            "--",
            SUBJECTS_DIR,
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert os.EX_NOINPUT == proc_info.returncode
    assert not proc_info.stdout
    assert "not find any volume files" in proc_info.stderr.rstrip().decode()


def test_script_no_files_found():
    proc_info = subprocess.run(
        [
            "freesurfer-volume-reader",
            "--freesurfer-hipposf-filename-regex",
            r"^21$",
            "--",
            SUBJECTS_DIR,
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert os.EX_NOINPUT == proc_info.returncode
    assert not proc_info.stdout
    assert "not find any volume files" in proc_info.stderr.rstrip().decode()


def test_main_module_script_help():
    subprocess.run(["python", "-m", "freesurfer_volume_reader", "--help"], check=True)


def test_main_module_script_version():
    proc_info = subprocess.run(
        ["python", "-m", "freesurfer_volume_reader", "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc_info.stdout.rstrip() == freesurfer_volume_reader.__version__.encode()
    assert not proc_info.stderr
