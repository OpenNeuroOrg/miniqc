import os
from math import prod

import nibabel as nb

from .types import CheckList, CheckResult


def load(path: os.PathLike[str]) -> nb.Nifti1Image:
    """Load NIfTI-1 or NIfTI-2 (including CIFTI-2) images"""
    try:
        return nb.Nifti1Image.from_filename(path)
    except Exception:
        return nb.Nifti2Image.from_filename(path)


def fullsize(img: nb.Nifti1Image) -> CheckResult:
    """Verify NIfTI image has expected length from header"""
    dataobj: nb.arrayproxy.ArrayProxy = img.dataobj  # type: ignore

    expected: int = dataobj.offset + dataobj.dtype.itemsize * prod(dataobj.shape)

    with dataobj._get_fileobj() as fobj:
        # Seek beyond end returns end position
        actual: int = fobj.seek(expected + 1)
    return CheckResult(
        (actual == expected, f'Expected {expected} bytes; found {actual}')
    )


CHECKS = CheckList(
    loader=load,
    checks=[
        fullsize,
    ],
)
