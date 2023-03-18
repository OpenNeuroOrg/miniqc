import json
import os
import re
import typing as ty
from dataclasses import dataclass
from enum import Enum
from math import prod
from pathlib import Path

import nibabel as nb
import typer

T = ty.TypeVar('T')


@dataclass
class CheckList(ty.Generic[T]):
    """Object that pairs a file loader with boolean checks on the loaded file"""

    loader: ty.Callable[[os.PathLike], T]
    checks: list[ty.Callable[[T], bool]]


def nifti_load(path: os.PathLike) -> nb.Nifti1Image:
    """Load NIfTI-1 or NIfTI-2 (including CIFTI-2) images"""
    try:
        return nb.Nifti1Image.from_filename(path)
    except Exception:
        return nb.Nifti2Image.from_filename(path)


def nifti_fullsize(img: nb.Nifti1Image) -> bool:
    """Verify NIfTI image is seekable to expected length"""
    expected_size = int(
        img.header['vox_offset']
        + (img.header['bitpix'] // 8) * prod(img.shape)
    )

    # Nudge type checker
    assert isinstance(img.dataobj, nb.arrayproxy.ArrayProxy)
    with img.dataobj._get_fileobj() as fobj:
        fobj.seek(expected_size)

    return True


# Regex patterns paired with checklists to verify on file
# To avoid multiple reads, only the first matching check is applied to each
# file
CHECKS: list[tuple[re.Pattern[str], CheckList]] = [
    (
        re.compile(r'\.nii(.gz)?$'),
        CheckList(loader=nifti_load, checks=[nifti_fullsize]),
    ),
]

app = typer.Typer()


class AnalysisLevel(Enum):
    run = 'run'
    session = 'session'
    participant = 'participant'
    dataset = 'dataset'


@app.command()
def main(
    bids_dir: Path,
    output_dir: ty.Optional[Path] = typer.Argument(None),
    analysis_level: ty.Optional[AnalysisLevel] = typer.Argument(None),
    allow_dangling_links: bool = typer.Option(
        False,
        '--allow-dangling-links',
        '-l',
        help='Ignore symlinks with missing targets',
    ),
):
    errors = []
    for root, dirs, files in os.walk(bids_dir):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        root_path = Path(root)
        for file in files:
            for pattern, checklist in CHECKS:
                if re.search(pattern, file):
                    path = root_path / file
                    try:
                        fileobj = checklist.loader(path)
                        for check in checklist.checks:
                            if not check(fileobj):
                                raise ValueError(check.__doc__)
                    except Exception as e:
                        if not allow_dangling_links or not isinstance(
                            e, FileNotFoundError
                        ):
                            errors.append(
                                (
                                    str(path.relative_to(bids_dir)),
                                    type(e).__name__,
                                    str(e),
                                )
                            )
                    break
    print(json.dumps(errors, indent=2))
    typer.Exit(len(errors))


if __name__ == '__main__':
    app()
