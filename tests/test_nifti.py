from pathlib import Path

import nibabel as nb
import pytest

from miniqc.nifti import fullsize, load


def test_load_type(good_nifti: Path, good_nifti2: Path) -> None:
    # nifti.load should always return a Nifti1Image, which is a base class
    # of Nifti2Image
    img = load(good_nifti)
    assert isinstance(img, nb.Nifti1Image)

    img = load(good_nifti2)
    assert isinstance(img, nb.Nifti2Image)
    assert isinstance(img, nb.Nifti1Image)


def test_load_fail(example_dataset: Path) -> None:
    # Images that are missing or lacking a NIfTI header will fail
    with pytest.raises(FileNotFoundError):
        load(example_dataset / 'does_not_exist.nii')
    with pytest.raises(nb.filebasedimages.ImageFileError):
        load(example_dataset / 'dataset_description.json')


def test_fullsize(
    good_nifti: Path, truncated_nifti: Path, good_nifti2: Path
) -> None:
    # fullsize returns results if load succeeds
    good, message = fullsize(load(good_nifti))
    assert good
    good, message = fullsize(load(truncated_nifti))
    assert not good
    good, message = fullsize(load(good_nifti2))
    assert good
