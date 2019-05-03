import os

import pandas
import pytest

SUBJECTS_DIR = os.path.join(os.path.dirname(__file__), 'subjects')


def _assert_volume_frames_equal(left: pandas.DataFrame, right: pandas.DataFrame):
    sort_by = ['volume_mm^3', 'analysis_id']
    left.sort_values(sort_by, inplace=True)
    right.sort_values(sort_by, inplace=True)
    left.reset_index(inplace=True, drop=True)
    right.reset_index(inplace=True, drop=True)
    pandas.util.testing.assert_frame_equal(
        left=left,
        right=right,
        # ignore the order of index & columns
        check_like=True,
    )


@pytest.fixture(scope='module')
def assert_volume_frames_equal():
    return _assert_volume_frames_equal
