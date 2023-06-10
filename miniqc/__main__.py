import json
import os
import re
import typing as ty
from enum import Enum
from pathlib import Path

import nibabel as nb
import typer

from . import nifti
from .types import CheckList, FailedCheck

# Add to this list as file types are added
SupportedType: ty.TypeAlias = ty.Union[nb.Nifti1Image,]

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
                            result, message = check(fileobj)
                            if not result:
                                raise FailedCheck(message or check.__doc__)
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
    raise typer.Exit(code=len(errors) > 0)


if __name__ == '__main__':
    app()
