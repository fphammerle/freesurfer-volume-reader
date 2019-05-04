import pytest

import freesurfer_volume_reader


class DummyVolumeFile(freesurfer_volume_reader.VolumeFile):

    # pylint: disable=useless-super-delegation

    @property
    def absolute_path(self):
        return super().absolute_path

    def read_volumes_mm3(self):
        return super().read_volumes_mm3()

    def read_volumes_dataframe(self):
        return super().read_volumes_dataframe()


def test_volume_file_abstractmethod():
    volume_file = DummyVolumeFile()
    with pytest.raises(NotImplementedError):
        assert volume_file.absolute_path
    with pytest.raises(NotImplementedError):
        volume_file.read_volumes_mm3()
    with pytest.raises(NotImplementedError):
        volume_file.read_volumes_dataframe()
