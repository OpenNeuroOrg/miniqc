from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def example_dataset():
    return Path(__file__).parent / 'data' / 'bids_dataset'


@pytest.fixture(scope='session')
def good_nifti(example_dataset):
    return example_dataset / 'sub-01' / 'anat' / 'sub-01_acq-good_T1w.nii.gz'


@pytest.fixture(scope='session')
def truncated_nifti(example_dataset):
    return (
        example_dataset / 'sub-01' / 'anat' / 'sub-01_acq-truncated_T2w.nii.gz'
    )


@pytest.fixture(scope='session')
def good_nifti2(example_dataset):
    return example_dataset / 'sub-01' / 'anat' / 'sub-01_acq-nii2_T1w.nii.gz'
