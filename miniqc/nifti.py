import os
import re
from math import prod

import nibabel as nb

from .types import CheckList, CheckResult


def load(path: os.PathLike) -> nb.Nifti1Image:
    """Load NIfTI-1 or NIfTI-2 (including CIFTI-2) images"""
    try:
        return nb.Nifti1Image.from_filename(path)
    except Exception:
        return nb.Nifti2Image.from_filename(path)


def fullsize(img: nb.Nifti1Image) -> CheckResult:
    """Verify NIfTI image has expected length from header"""
    dataobj = img.dataobj
    # Nudge type checker
    assert isinstance(dataobj, nb.arrayproxy.ArrayProxy)

    expected = dataobj.offset + dataobj.dtype.itemsize * prod(dataobj.shape)

    with dataobj._get_fileobj() as fobj:
        actual = fobj.seek(expected + 1)
        return CheckResult(
            (actual == expected, f'Expected {expected} bytes; found {actual}')
        )


CHECKS = CheckList(
    loader=load,
    checks=[
        fullsize,
    ],
)
