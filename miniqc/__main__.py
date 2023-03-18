import json
import os
import re
import typing as ty
from enum import Enum
from math import prod
from pathlib import Path

import nibabel as nb
import typer


class AnalysisLevel(Enum):
    run = 'run'
    session = 'session'
    participant = 'participant'
    dataset = 'dataset'


app = typer.Typer()


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
            if re.search(r'\.nii(.gz)?$', file):
                path = root_path / file
                try:
                    try:
                        img = nb.Nifti1Image.from_filename(path)
                    except Exception:
                        img = nb.Nifti2Image.from_filename(path)
                    expected_size = int(
                        img.header['vox_offset']
                        + (img.header['bitpix'] // 8) * prod(img.shape)
                    )

                    # Nudge type checker
                    assert isinstance(img.dataobj, nb.arrayproxy.ArrayProxy)
                    with img.dataobj._get_fileobj() as fobj:
                        fobj.seek(expected_size)

                except Exception as e:
                    if allow_dangling_links and isinstance(
                        e, FileNotFoundError
                    ):
                        continue
                    errors.append(
                        (
                            str(path.relative_to(bids_dir)),
                            type(e).__name__,
                            str(e),
                        )
                    )
    print(json.dumps(errors, indent=2))
    typer.Exit(len(errors))


if __name__ == '__main__':
    app()
