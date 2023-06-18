import json
import os
import re
import typing as ty
from enum import Enum
from itertools import chain
from pathlib import Path

import nibabel as nb
import typer
from typing_extensions import TypeAlias

from . import nifti
from .types import CheckList, FailedCheck

# Add to this list as file types are added
SupportedType: TypeAlias = ty.Union[
    nb.Nifti1Image,
]

# Regex patterns paired with checklists to verify on file
# To avoid multiple reads, only the first matching check is applied to each
# file
CHECKS: list[tuple[re.Pattern[str], CheckList[SupportedType]]] = [
    (re.compile(r'\.nii(\.gz)?$'), nifti.CHECKS),
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
) -> None:

    # Allow to be used on individual files
    if not bids_dir.is_dir():
        errors = check_file(bids_dir)
    else:
        errors = []
        for root, dirs, files in os.walk(bids_dir):
            dirs[:] = [d for d in dirs if not d[0] == '.']
            root_path = Path(root)
            errors.extend(
                chain.from_iterable(check_file(root_path / file, bids_dir) for file in files)
            )

    if allow_dangling_links:
        errors = [err for err in errors if err[1] != 'FileNotFoundError']
    print(json.dumps(errors, indent=2))
    raise typer.Exit(code=len(errors) > 0)


def check_file(
    path: Path,
    bids_dir: ty.Optional[Path] = None,
) -> list[tuple[str, str, str]]:
    for pattern, checklist in CHECKS:
        if re.search(pattern, path.name):
            try:
                fileobj = checklist.loader(path)
                for check in checklist.checks:
                    result, message = check(fileobj)
                    if not result:
                        raise FailedCheck(message or check.__doc__)
            except Exception as e:
                if bids_dir is not None:
                    path = path.relative_to(bids_dir)
                return [(str(path), type(e).__name__, str(e))]
    return []


if __name__ == '__main__':
    app()
