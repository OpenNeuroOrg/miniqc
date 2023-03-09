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
):
    errors = []
    for root, dirs, files in os.walk(bids_dir):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        root_path = Path(root)
        for file in files:
            if re.search(r'\.nii(.gz)?$', file):
                path = root_path / file
                try:
                    img = nb.load(path)
                    if isinstance(img, nb.Nifti1Image):
                        hdr: nb.Nifti1Header = img.header  # type: ignore
                    elif isinstance(img, nb.Cifti2Image):
                        hdr: nb.Nifti2Header = img.nifti_header  # type: ignore
                    expected_size = int(
                        hdr['vox_offset']
                        + (hdr['bitpix'] // 8) * prod(img.shape)
                    )
                    with img.dataobj._get_fileobj() as fobj:
                        fobj.seek(expected_size)
                except Exception as e:
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
